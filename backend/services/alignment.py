import cv2
import numpy as np


def align_images(image_a: np.ndarray, image_b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    gray_a = cv2.cvtColor(image_a, cv2.COLOR_RGB2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_RGB2GRAY)

    orb = cv2.ORB_create(500)
    keypoints_a, descriptors_a = orb.detectAndCompute(gray_a, None)
    keypoints_b, descriptors_b = orb.detectAndCompute(gray_b, None)

    if descriptors_a is None or descriptors_b is None or len(keypoints_a) < 4 or len(keypoints_b) < 4:
        return image_b, np.eye(3, dtype=np.float32)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = matcher.knnMatch(descriptors_a, descriptors_b, k=2)

    good_matches = []
    for match_a, match_b in matches:
        if match_a.distance < 0.75 * match_b.distance:
            good_matches.append(match_a)

    if len(good_matches) < 6:
        return image_b, np.eye(3, dtype=np.float32)

    source_points = np.float32([keypoints_a[match.queryIdx].pt for match in good_matches]).reshape(-1, 1, 2)
    target_points = np.float32([keypoints_b[match.trainIdx].pt for match in good_matches]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(target_points, source_points, cv2.RANSAC, 5.0)
    if homography is None:
        return image_b, np.eye(3, dtype=np.float32)

    height, width = image_a.shape[:2]
    aligned = cv2.warpPerspective(image_b, homography, (width, height))

    try:
        _, refined_homography = cv2.findTransformECC(
            cv2.cvtColor(image_b, cv2.COLOR_RGB2GRAY),
            gray_a,
            np.eye(3, 3, dtype=np.float32),
            cv2.MOTION_HOMOGRAPHY,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1e-6),
        )
        if refined_homography is not None:
            homography = refined_homography
            aligned = cv2.warpPerspective(image_b, homography, (width, height))
    except cv2.error:
        pass

    return aligned, homography
