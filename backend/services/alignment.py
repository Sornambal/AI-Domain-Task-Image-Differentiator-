import cv2
import numpy as np


def get_content_bbox(image: np.ndarray) -> tuple[int, int, int, int]:
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image.copy()
    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0, 0, image.shape[1], image.shape[0]
    all_pts = np.vstack(contours)
    return cv2.boundingRect(all_pts)


def align_images(image_a: np.ndarray, image_b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xa, ya, wa, ha = get_content_bbox(image_a)
    xb, yb, wb, hb = get_content_bbox(image_b)
    
    if wa > 0 and ha > 0 and wb > 0 and hb > 0:
        scale_x = wa / wb
        scale_y = ha / hb
        if abs(scale_x - 1.0) > 0.005 or abs(scale_y - 1.0) > 0.005:
            print(f"DEBUG: Pre-scaling Image B by ({scale_x:.4f}, {scale_y:.4f}) to match content bounds.")
            new_w = int(image_b.shape[1] * scale_x)
            new_h = int(image_b.shape[0] * scale_y)
            image_b = cv2.resize(image_b, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    gray_a = cv2.cvtColor(image_a, cv2.COLOR_RGB2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_RGB2GRAY)

    sift = cv2.SIFT_create()
    keypoints_a, descriptors_a = sift.detectAndCompute(gray_a, None)
    keypoints_b, descriptors_b = sift.detectAndCompute(gray_b, None)

    if descriptors_a is None or descriptors_b is None or len(keypoints_a) < 4 or len(keypoints_b) < 4:
        return image_b, np.eye(3, dtype=np.float32)

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    matches = matcher.knnMatch(descriptors_a, descriptors_b, k=2)

    good_matches = []
    for match_a, match_b in matches:
        if match_a.distance < 0.75 * match_b.distance:
            good_matches.append(match_a)

    if len(good_matches) < 6:
        return image_b, np.eye(3, dtype=np.float32)

    source_points = np.float32([keypoints_a[match.queryIdx].pt for match in good_matches]).reshape(-1, 1, 2)
    target_points = np.float32([keypoints_b[match.trainIdx].pt for match in good_matches]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(target_points, source_points, cv2.RANSAC, 3.0)
    if homography is None:
        return image_b, np.eye(3, dtype=np.float32)

    h_top_left = homography[0:2, 0:2]
    _, S, _ = np.linalg.svd(h_top_left)
    if any(abs(s - 1.0) > 0.005 for s in S):
        print(f"DEBUG: Residual scale mismatch detected in homography! Singular values: {S}")

    height, width = image_a.shape[:2]
    aligned = cv2.warpPerspective(image_b, homography, (width, height))

    try:
        gray_aligned = cv2.cvtColor(aligned, cv2.COLOR_RGB2GRAY)
        warp_matrix = np.eye(3, 3, dtype=np.float32)
        cc, ecc_warp = cv2.findTransformECC(
            gray_aligned,
            gray_a,
            warp_matrix,
            cv2.MOTION_HOMOGRAPHY,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1e-6),
        )
        # Compose: apply ECC's small correction on top of the coarse alignment
        refined_homography = ecc_warp @ homography
        refined_aligned = cv2.warpPerspective(image_b, refined_homography, (width, height))
        
        # Only accept if it's a genuine improvement — compare mean absolute pixel difference
        a_channels = image_a[:, :, :3] if image_a.ndim == 3 else image_a
        coarse_diff = np.mean(cv2.absdiff(aligned, a_channels))
        refined_diff = np.mean(cv2.absdiff(refined_aligned, a_channels))
        
        if refined_diff < coarse_diff:
            homography = refined_homography
            aligned = refined_aligned
    except cv2.error:
        pass  # keep the coarse ORB+RANSAC alignment if ECC fails to converge

    return aligned, homography
