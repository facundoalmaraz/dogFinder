import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np


IMAGE_DIR = "dataset/Images"
EMBEDDING_DIR = "embeddings_custom"
MODEL_PATH = "resnet50_finetuned.pth"
NUM_CLASSES = 3

os.makedirs(EMBEDDING_DIR, exist_ok=True)


model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, 120)
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


for class_folder in os.listdir(IMAGE_DIR):
    class_path = os.path.join(IMAGE_DIR, class_folder)
    if not os.path.isdir(class_path):
        continue

    for filename in os.listdir(class_path):
        file_path = os.path.join(class_path, filename)
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            embedding = get_embedding(file_path)
            output_name = f"{class_folder}_{filename.split('.')[0]}.npy"
            output_path = os.path.join(EMBEDDING_DIR, output_name)
            image_id = filename.split(".")[0]

            np.save(output_path, {
                "id": image_id,
                "embedding": embedding,
                "path": file_path,
                "class": class_folder
            })
            print(f"[OK] Embedding generado: {output_name}")
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
