# AI-Based CAD Drawing Difference Detection

This project provides a full-stack web application for comparing two CAD drawings. Users upload two files (PNG/JPG/PDF/DXF/DWG), and the backend aligns and compares them, then returns colored diff overlays, statistics, and an AI-generated summary.

## Features
- Accepts raster images, PDFs, and vector CAD files
- Converts uploads into a standardized PNG pipeline
- Aligns the comparison image onto the reference image using ORB + homography + ECC refinement
- Detects changed regions and returns bounding boxes and area statistics
- Uses the Groq API to generate a plain-language summary
- Exposes a React + Tailwind front end for upload and display

## Project structure
- backend/: FastAPI API, comparison services, file validation, and schemas
- frontend/: React/Vite app with Tailwind styling
- sample_images/: place test images here

## Local development

### 1. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set GROQ_API_KEY=your_key_here
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
set VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

Then open http://localhost:5173.

## Render deployment
### Backend
- Create a web service from the repository root
- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
- Set GROQ_API_KEY in the Render dashboard

### Frontend
- Create a static site from the frontend folder
- Build command: npm run build
- Publish directory: dist
- Set VITE_API_BASE_URL to the deployed backend URL

## DWG support note
DWG parsing is not implemented directly in Python because the format is closed and not reliably parseable with an open-source pure-Python library. The backend includes a conversion path that tries to invoke an external converter such as ODA File Converter. On Render, this is best supported with a Docker-based backend service. If a DWG converter is unavailable, the app can still process PNG/JPG/PDF/DXF uploads successfully.

## Sample images
Place test files in sample_images/ such as:
- reference.png and comparison.png
- a technical drawing PDF
- a simple DXF file
