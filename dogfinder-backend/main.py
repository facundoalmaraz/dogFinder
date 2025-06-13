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
    allow_origins=["http://localhost:3000", "https://3xdwdjjr-3000.brs.devtunnels.ms"],
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


from scripts.auto_traits import infer_traits_from_class, extract_dominant_color
from scripts.cnn_compare import compare_image_to_embeddings

@app.post("/auto-analyze")
async def auto_analyze(image: UploadFile = File(...)):
    path = os.path.join(UPLOAD_FOLDER, image.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    top_matches = compare_image_to_embeddings(path)
    top1 = top_matches[0]

    traits = infer_traits_from_class(top1["id"])
    color = extract_dominant_color(path)

    return {
        "cnn_class_id": top1["id"],
        "class_name": top1["class"],
        "size": traits["size"],
        "age": traits["age"],
        "color": color,
        "hasCollar": False  # se puede mejorar con visión
    }
