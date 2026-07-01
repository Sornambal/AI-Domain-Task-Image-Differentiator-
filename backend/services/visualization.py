from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def create_visualizations(image_a: np.ndarray, image_b: np.ndarray, aligned_b: np.ndarray, regions: list[dict], output_dir: str | Path) -> tuple[str, str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    diff_overlay = image_a.copy()
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        cv2.rectangle(diff_overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)

    heatmap = np.zeros_like(image_a, dtype=np.uint8)
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        cv2.rectangle(heatmap, (x1, y1), (x2, y2), (255, 255, 255), -1)

    composite = np.hstack([image_a, aligned_b])

    diff_path = output_dir / "diff_visualization.png"
    heatmap_path = output_dir / "heatmap.png"
    composite_path = output_dir / "side_by_side.png"

    Image.fromarray(diff_overlay).save(diff_path)
    Image.fromarray(heatmap).save(heatmap_path)
    Image.fromarray(composite).save(composite_path)

    return str(diff_path), str(heatmap_path), str(composite_path)
