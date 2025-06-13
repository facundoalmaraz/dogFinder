import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# ✅ Configuración
DATASET_PATH = "dataset/Images"
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 0.001

# ✅ Transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    )
])

# ✅ Dataset
dataset = datasets.ImageFolder(DATASET_PATH, transform=transform)
class_names = dataset.classes
print(f"Clases detectadas: {class_names}")

# ✅ Dataloader
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# ✅ Modelo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=True)

# Congelar capas anteriores (opcional)
for param in model.parameters():
    param.requires_grad = False

# Reemplazar la capa final
num_classes = len(class_names)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

# ✅ Pérdida y optimizador
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

# ✅ Entrenamiento
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    accuracy = 100 * correct / total
    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {total_loss:.4f} - Accuracy: {accuracy:.2f}%")

# ✅ Guardar el modelo
torch.save(model.state_dict(), "resnet50_finetuned.pth")
print("Modelo guardado como resnet50_finetuned.pth")
