import os
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from services.alignment import align_images
from services.diff_engine import detect_differences
from services.format_converter import convert_to_standardized_png, load_image_as_numpy
from services.summary_generator import generate_summary
from services.visualization import create_visualizations
from utils.file_validation import validate_upload_file

router = APIRouter(prefix="/api", tags=["compare"])

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/compare", status_code=200)
def compare_images(request: Request, image_a: UploadFile = File(...), image_b: UploadFile = File(...)):
    try:
        validate_upload_file(image_a.file, image_a.filename or "")
        validate_upload_file(image_b.file, image_b.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    input_a = UPLOAD_DIR / f"{Path(image_a.filename or 'image_a').stem}_a" 
    input_b = UPLOAD_DIR / f"{Path(image_b.filename or 'image_b').stem}_b"

    image_a_path = input_a.with_suffix(".png")
    image_b_path = input_b.with_suffix(".png")

    image_a_bytes = image_a.file.read()
    image_b_bytes = image_b.file.read()
    image_a_path.write_bytes(image_a_bytes)
    image_b_path.write_bytes(image_b_bytes)

    try:
        converted_a = convert_to_standardized_png(image_a_path, image_a_path.with_name(image_a_path.stem + "_converted.png"))
        converted_b = convert_to_standardized_png(image_b_path, image_b_path.with_name(image_b_path.stem + "_converted.png"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {exc}") from exc

    image_a_array = load_image_as_numpy(converted_a)
    image_b_array = load_image_as_numpy(converted_b)

    aligned_b, _ = align_images(image_a_array, image_b_array)
    stats = detect_differences(image_a_array, aligned_b)
    summary = generate_summary(stats)

    diff_path, heatmap_path, composite_path = create_visualizations(image_a_array, image_b_array, aligned_b, stats["regions"], UPLOAD_DIR)

    base_url = str(request.base_url).rstrip("/")
    return {
        "original_a_url": f"{base_url}/uploads/{converted_a.name}",
        "original_b_url": f"{base_url}/uploads/{converted_b.name}",
        "diff_visualization_url": f"{base_url}/uploads/{Path(diff_path).name}",
        "heatmap_url": f"{base_url}/uploads/{Path(heatmap_path).name}",
        "statistics": stats,
        "ai_summary": summary,
    }
