import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.compare import router as compare_router

app = FastAPI(title="CAD Drawing Comparator")

default_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
allowed_origins = os.getenv("CORS_ORIGINS")
if allowed_origins:
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
else:
    allowed_origins = default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compare_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health")
def health_check():
    return {"status": "ok"}
