from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def draw_marker(image, number, x, y, color, radius=14):
    center = (int(x), int(y))
    cv2.circle(image, center, radius, color, thickness=-1)
    cv2.circle(image, center, radius, (255, 255, 255), thickness=2)
    text = str(number)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    (tw, th), _ = cv2.getTextSize(text, font, font_scale, 2)
    text_pos = (center[0] - tw // 2, center[1] + th // 2)
    cv2.putText(image, text, text_pos, font, font_scale, (255, 255, 255), 2, cv2.LINE_AA)

def create_visualizations(image_a: np.ndarray, image_b: np.ndarray, aligned_b: np.ndarray, regions: list[dict], output_dir: str | Path) -> tuple[str, str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    LABEL_MIN_SPACING_PX = 40
    MAX_LABELED_REGIONS = 20
    drawn_labels = []

    diff_overlay = image_a.copy()
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        w, h = region.get("width", x2 - x1), region.get("height", y2 - y1)
        number = region.get("number", 1)
        region_type = region.get("type", "modified")

        if region_type == "added":
            box_color = (0, 200, 0)
        elif region_type == "removed":
            box_color = (0, 0, 255)
        else:
            box_color = (0, 140, 255) # Orange (BGR)

        cv2.rectangle(diff_overlay, (x1, y1), (x2, y2), box_color, 2)

        if number <= MAX_LABELED_REGIONS:
            marker_x, marker_y = x1, y1
            
            # Simple overlap resolution
            for (lx, ly) in drawn_labels:
                if ((marker_x - lx) ** 2 + (marker_y - ly) ** 2) ** 0.5 < LABEL_MIN_SPACING_PX:
                    marker_x += int(LABEL_MIN_SPACING_PX * 0.8)
                    marker_y -= int(LABEL_MIN_SPACING_PX * 0.8)
            
            draw_marker(diff_overlay, number, marker_x, marker_y, box_color)
            drawn_labels.append((marker_x, marker_y))

    # Professional Heatmap Generation
    diff = cv2.absdiff(image_a, aligned_b)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    
    # Smooth the differences to create a soft, glowing gradient rather than harsh pixels
    blurred_diff = cv2.GaussianBlur(gray_diff, (21, 21), 0)
    
    HEATMAP_ALPHA_SCALE = 1.5
    HEATMAP_NOISE_FLOOR = 20
    HEATMAP_ALPHA_BOOST = 1.2
    
    # Scale intensity so even small defects are visible in the heatmap
    heatmap_intensity = cv2.convertScaleAbs(blurred_diff, alpha=HEATMAP_ALPHA_SCALE, beta=0)
    
    # Zero out near-noise-floor values so minor jitter doesn't appear as a hotspot
    heatmap_intensity[heatmap_intensity < HEATMAP_NOISE_FLOOR] = 0
    
    # Apply a modern, professional colormap (TURBO is perceptually uniform and premium)
    heatmap_color = cv2.applyColorMap(heatmap_intensity, cv2.COLORMAP_TURBO)
    
    # Create a dimmed, grayscale version of the original image to serve as the background
    base_gray = cv2.cvtColor(image_a, cv2.COLOR_RGB2GRAY)
    base_bgr = cv2.cvtColor(base_gray, cv2.COLOR_GRAY2BGR)
    dark_bg = cv2.convertScaleAbs(base_bgr, alpha=0.3, beta=0)
    
    # Create an alpha mask based on the intensity of the difference
    # This makes the heatmap transparent where there is no difference, revealing the background
    alpha = heatmap_intensity.astype(float) / 255.0
    alpha = np.clip(alpha * HEATMAP_ALPHA_BOOST, 0, 1) # Boost opacity of the hotspots
    alpha = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)
    
    # Blend the glowing heatmap over the darkened CAD drawing
    blended = (heatmap_color.astype(float) * alpha + dark_bg.astype(float) * (1 - alpha)).astype(np.uint8)
    
    # Convert BGR (OpenCV format) back to RGB for PIL
    heatmap = cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)

    composite = np.hstack([image_a, aligned_b])

    diff_path = output_dir / "diff_visualization.png"
    heatmap_path = output_dir / "heatmap.png"
    composite_path = output_dir / "side_by_side.png"

    Image.fromarray(diff_overlay).save(diff_path)
    Image.fromarray(heatmap).save(heatmap_path)
    Image.fromarray(composite).save(composite_path)

    return str(diff_path), str(heatmap_path), str(composite_path)
