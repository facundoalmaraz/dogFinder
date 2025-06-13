from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ⬅️ nuevo
from scripts.combined_fuzzy import process_image_and_criteria
import shutil
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta 'dataset' como pública
app.mount("/dataset", StaticFiles(directory="dataset"), name="dataset")  # ⬅️ nuevo

# Carpeta para subir imágenes temporales
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/compare")
async def compare(
    image: UploadFile = File(...),
    size: str = Form(...),
    age: int = Form(...),
    zone: str = Form(...),
    color: str = Form(...),
    hasCollar: bool = Form(...)
):
    path = os.path.join(UPLOAD_FOLDER, image.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    result = process_image_and_criteria(
        path, size, age, zone, color, hasCollar
    )
    return result
