import cv2
import numpy as np
from skimage.metrics import structural_similarity



def _classify_region(image_a: np.ndarray, image_b: np.ndarray, bbox: tuple[int, int, int, int]) -> str:
    x, y, w, h = bbox
    crop_a = image_a[y : y + h, x : x + w]
    crop_b = image_b[y : y + h, x : x + w]

    if crop_a.size == 0 or crop_b.size == 0:
        return "modified"

    edges_a = cv2.Canny(crop_a, 50, 150)
    edges_b = cv2.Canny(crop_b, 50, 150)
    density_a = np.mean(edges_a > 0)
    density_b = np.mean(edges_b > 0)

    if density_b > density_a + 0.05:
        return "added"
    if density_a > density_b + 0.05:
        return "removed"
    return "modified"




def _location_bucket(x: int, y: int, width: int, height: int) -> str:
    center_x = x + width / 2
    center_y = y + height / 2
    mid_x = width / 2
    mid_y = height / 2

    if center_y < mid_y / 2:
        vertical = "top"
    elif center_y > height - mid_y / 2:
        vertical = "bottom"
    else:
        vertical = "center"

    if center_x < width / 3:
        horizontal = "left"
    elif center_x > width - width / 3:
        horizontal = "right"
    else:
        horizontal = "center"

    return f"{vertical}-{horizontal}".replace("center-center", "center")


def detect_differences(image_a: np.ndarray, image_b: np.ndarray, sensitivity: int = 50) -> dict:
    if image_a.shape != image_b.shape:
        target_shape = (max(image_a.shape[0], image_b.shape[0]), max(image_a.shape[1], image_b.shape[1]))
        padded_a = np.zeros((target_shape[0], target_shape[1], 3), dtype=np.uint8)
        padded_b = np.zeros((target_shape[0], target_shape[1], 3), dtype=np.uint8)
        padded_a[: image_a.shape[0], : image_a.shape[1]] = image_a
        padded_b[: image_b.shape[0], : image_b.shape[1]] = image_b
        image_a, image_b = padded_a, padded_b

    gray_a = cv2.cvtColor(image_a, cv2.COLOR_RGB2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_RGB2GRAY)

    score, ssim_map = structural_similarity(gray_a, gray_b, full=True, win_size=7, data_range=255)
    diff_map = 1.0 - ssim_map          # convert similarity → dissimilarity, range ~0 (identical) to ~2 (max different)
    diff_map = np.clip(diff_map, 0, 1)  # clamp to a sane 0–1 range before scaling
    diff_map = (diff_map * 255).astype(np.uint8)

    threshold_val = max(5, 255 - int(sensitivity * 2.5))
    _, mask = cv2.threshold(diff_map, threshold_val, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    merge_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
    dilated = cv2.dilate(mask, merge_kernel, iterations=2)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, merge_kernel, iterations=2)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_pixels = image_a.shape[0] * image_a.shape[1]
    min_area_percent = 0.05 - (sensitivity / 100) * 0.045
    min_area = max(50, int(total_pixels * (min_area_percent / 100)))

    boxes = []
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < min_area:
            continue
        boxes.append((x, y, w, h))

    regions = []
    for x, y, w, h in boxes:
        area_px = int(w * h)
        centroid = (int(x + w / 2), int(y + h / 2))
        location = _location_bucket(x, y, image_a.shape[1], image_a.shape[0])
        region_type = _classify_region(image_a, image_b, (x, y, w, h))
        regions.append(
            {
                "bbox": [x, y, x + w, y + h],
                "width": w,
                "height": h,
                "area_px": area_px,
                "centroid": [centroid[0], centroid[1]],
                "location": location,
                "type": region_type,
            }
        )

    regions.sort(key=lambda r: r["area_px"], reverse=True)

    percent_area_changed = round((sum(region["area_px"] for region in regions) / total_pixels) * 100, 2) if total_pixels else 0.0
    return {"num_changed_regions": len(regions), "percent_area_changed": percent_area_changed, "regions": regions}
