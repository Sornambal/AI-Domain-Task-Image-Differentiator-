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


def _merge_boxes(boxes: list[tuple[int, int, int, int]], iou_threshold: float = 0.2) -> list[tuple[int, int, int, int]]:
    if not boxes:
        return []

    merged = []
    for box in boxes:
        x, y, w, h = box
        current = [x, y, x + w, y + h]
        if not merged:
            merged.append(current)
            continue

        found = False
        for index, candidate in enumerate(merged):
            cx1, cy1, cx2, cy2 = candidate
            ix1 = max(x, cx1)
            iy1 = max(y, cy1)
            ix2 = min(x + w, cx2)
            iy2 = min(y + h, cy2)
            inter_area = max(0, ix2 - ix1) * max(0, iy2 - iy1)
            box_area = w * h
            candidate_area = max(0, cx2 - cx1) * max(0, cy2 - cy1)
            union_area = box_area + candidate_area - inter_area
            if union_area > 0 and inter_area / union_area >= iou_threshold:
                merged[index] = [min(cx1, x), min(cy1, y), max(cx2, x + w), max(cy2, y + h)]
                found = True
                break
        if not found:
            merged.append(current)

    return [(x1, y1, x2 - x1, y2 - y1) for x1, y1, x2, y2 in merged]


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

    score, diff_map = structural_similarity(gray_a, gray_b, full=True, win_size=7, data_range=255)
    diff_map = np.abs(diff_map)
    diff_map = (diff_map * 255).astype(np.uint8)

    _, mask = cv2.threshold(diff_map, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    dilated = cv2.dilate(mask, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = max(10, 200 - (sensitivity * 2))

    boxes = []
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < min_area:
            continue
        boxes.append((x, y, w, h))

    merged_boxes = _merge_boxes(boxes)
    regions = []
    for x, y, w, h in merged_boxes:
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

    total_pixels = image_a.shape[0] * image_a.shape[1]
    percent_area_changed = round((sum(region["area_px"] for region in regions) / total_pixels) * 100, 2) if total_pixels else 0.0
    return {"num_changed_regions": len(regions), "percent_area_changed": percent_area_changed, "regions": regions}
