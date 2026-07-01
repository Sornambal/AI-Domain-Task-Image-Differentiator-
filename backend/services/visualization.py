from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def create_visualizations(image_a: np.ndarray, image_b: np.ndarray, aligned_b: np.ndarray, regions: list[dict], output_dir: str | Path) -> tuple[str, str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    diff_overlay = image_a.copy()
    for idx, region in enumerate(regions, 1):
        x1, y1, x2, y2 = region["bbox"]
        w, h = region.get("width", x2 - x1), region.get("height", y2 - y1)
        
        # Calculate faux 3D depth offset
        dx = max(5, int(w * 0.1))
        dy = max(5, int(h * 0.1))
        
        # Front face (Red)
        cv2.rectangle(diff_overlay, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # Back face (Green)
        cv2.rectangle(diff_overlay, (x1 + dx, y1 - dy), (x2 + dx, y2 - dy), (0, 255, 0), 2)
        # Connecting lines (Red)
        cv2.line(diff_overlay, (x1, y1), (x1 + dx, y1 - dy), (255, 0, 0), 1)
        cv2.line(diff_overlay, (x2, y1), (x2 + dx, y1 - dy), (255, 0, 0), 1)
        cv2.line(diff_overlay, (x1, y2), (x1 + dx, y2 - dy), (255, 0, 0), 1)
        cv2.line(diff_overlay, (x2, y2), (x2 + dx, y2 - dy), (255, 0, 0), 1)
        
        label = f"#{idx} [{w}x{h}]"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        thickness = 2
        (text_w, text_h), _ = cv2.getTextSize(label, font, font_scale, thickness)
        
        text_y = y1 - dy - 5 if y1 - dy - 5 > text_h else y1 - dy + text_h + 5
        
        # Draw background for text to make it readable
        cv2.rectangle(diff_overlay, (x1 + dx, text_y - text_h - 2), (x1 + dx + text_w, text_y + 2), (255, 255, 255), -1)
        cv2.putText(diff_overlay, label, (x1 + dx, text_y), font, font_scale, (255, 0, 0), thickness)

    # Professional Heatmap Generation
    diff = cv2.absdiff(image_a, aligned_b)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    
    # Smooth the differences to create a soft, glowing gradient rather than harsh pixels
    blurred_diff = cv2.GaussianBlur(gray_diff, (21, 21), 0)
    
    # Scale intensity so even small defects are visible in the heatmap
    heatmap_intensity = cv2.convertScaleAbs(blurred_diff, alpha=4.0, beta=0)
    
    # Apply a modern, professional colormap (TURBO is perceptually uniform and premium)
    heatmap_color = cv2.applyColorMap(heatmap_intensity, cv2.COLORMAP_TURBO)
    
    # Create a dimmed, grayscale version of the original image to serve as the background
    base_gray = cv2.cvtColor(image_a, cv2.COLOR_RGB2GRAY)
    base_bgr = cv2.cvtColor(base_gray, cv2.COLOR_GRAY2BGR)
    dark_bg = cv2.convertScaleAbs(base_bgr, alpha=0.3, beta=0)
    
    # Create an alpha mask based on the intensity of the difference
    # This makes the heatmap transparent where there is no difference, revealing the background
    alpha = heatmap_intensity.astype(float) / 255.0
    alpha = np.clip(alpha * 2.0, 0, 1) # Boost opacity of the hotspots
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
