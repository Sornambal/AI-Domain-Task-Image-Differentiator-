import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import cv2
import fitz
import numpy as np
from PIL import Image

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".dxf", ".dwg"}


def validate_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS


def convert_to_standardized_png(input_path: str | os.PathLike, output_path: str | os.PathLike, source_filename: Optional[str] = None) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ext = input_path.suffix.lower()
    if ext in {".png", ".jpg", ".jpeg"}:
        with Image.open(input_path) as img:
            if img.mode in {"RGBA", "LA", "P"}:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(output_path, format="PNG")
        return output_path

    if ext == ".pdf":
        doc = fitz.open(input_path)
        page = doc.load_page(0)
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(output_path)
        doc.close()
        return output_path

    if ext == ".dxf":
        try:
            import ezdxf
            from ezdxf.addons.drawing import Frontend, RenderContext
            from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:
            raise RuntimeError("ezdxf/matplotlib is required for DXF conversion") from exc

        doc = ezdxf.readfile(str(input_path))
        msp = doc.modelspace()
        fig = plt.figure(figsize=(8, 8), dpi=200)
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        backend = MatplotlibBackend(ax)
        frontend = Frontend(ctx)
        frontend.draw_layout(msp, backend)
        fig.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        return output_path

    if ext == ".dwg":
        converter = os.getenv("DWG_CONVERTER_PATH") or shutil.which("odaFileConverter") or shutil.which("dwg2dxf") or shutil.which("librecad")
        if not converter:
            raise RuntimeError("DWG conversion requires an external converter such as ODA File Converter")

        temp_dxf = output_path.with_suffix(".dxf")
        subprocess.run([converter, str(input_path), str(temp_dxf)], check=True, capture_output=True, text=True)
        return convert_to_standardized_png(temp_dxf, output_path)

    raise ValueError(f"Unsupported file type: {ext}")


def load_image_as_numpy(path: str | os.PathLike) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Unable to read image from {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
