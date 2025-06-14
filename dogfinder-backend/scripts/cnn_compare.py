import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = "resnet50_finetuned.pth"
EMBEDDINGS_DIR = "embeddings_custom"
NUM_CLASSES = 120

def get_embedding_model():
    model = models.resnet50(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()

    print("🔎 Capa final del modelo:")
    print(model.fc)

    return torch.nn.Sequential(*list(model.children())[:-1])


def extract_embedding(image_path, model):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        )
    ])
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        return model(tensor).squeeze().numpy()

def compare_image_to_embeddings(image_path):
    model = get_embedding_model()
    query_embedding = extract_embedding(image_path, model).reshape(1, -1)

    matches = []

    for file in os.listdir(EMBEDDINGS_DIR):
        if not file.endswith(".npy"):
            continue

        data = np.load(os.path.join(EMBEDDINGS_DIR, file), allow_pickle=True).item()
        stored_embedding = data["embedding"].reshape(1, -1)
        sim = cosine_similarity(query_embedding, stored_embedding)[0][0]

        filename = os.path.splitext(file)[0]
        parts = filename.split("_")
        id_auto = f"{parts[-2]}_{parts[-1]}" if len(parts) >= 2 else filename

        match = {
            "id": data.get("id", id_auto),
            "similarity": float(sim),
            "path": data.get("path", "dataset/default.jpg"),
            "class": data.get("class", "Desconocida")
        }

        print(f"🧪 ID del archivo {file}: {match['id']}")
        matches.append(match)

    matches.sort(key=lambda x: x["similarity"], reverse=True)
    return matches[:5]