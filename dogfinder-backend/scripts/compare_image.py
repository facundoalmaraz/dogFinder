import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# --- Configuración ---
MODEL_PATH = "resnet50_finetuned.pth"
EMBEDDINGS_DIR = "embeddings_custom"
IMAGE_PATH = "imagen_usuario.jpg"  # colocá tu imagen a comparar en la raíz del proyecto
NUM_RESULTS = 5
NUM_CLASSES = 120  # cantidad de razas del dataset

# --- Cargar modelo entrenado y extraer embeddings ---
model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()
embedding_model = torch.nn.Sequential(*list(model.children())[:-1])

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    )
])

def get_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        embedding = embedding_model(tensor).squeeze().numpy()
    return embedding


query_embedding = get_embedding(IMAGE_PATH).reshape(1, -1)


results = []

for file in os.listdir(EMBEDDINGS_DIR):
    if file.endswith(".npy"):
        data = np.load(os.path.join(EMBEDDINGS_DIR, file), allow_pickle=True).item()
        stored_embedding = data["embedding"].reshape(1, -1)
        sim = cosine_similarity(query_embedding, stored_embedding)[0][0]
        results.append((sim, data["path"]))


top_results = results[:NUM_RESULTS]

print("\n🐶 Imágenes más parecidas:\n")
for i, (sim, path) in enumerate(top_results):
    print(f"{i+1}. {path} — Similitud: {sim:.4f}")


fig, axs = plt.subplots(1, NUM_RESULTS, figsize=(15, 5))
for i, (_, path) in enumerate(top_results):
    img = Image.open(path)
    axs[i].imshow(img)
    axs[i].axis("off")
    axs[i].set_title(f"{i+1}")
plt.suptitle("Resultados más parecidos")
plt.tight_layout()
plt.show()
