import os
import json
import random

EMBEDDINGS_DIR = "embeddings_custom"
OUTPUT_JSON = "dogs_metadata.json"

sizes = ["pequeño", "mediano", "grande"]
colors = ["blanco", "negro", "marrón", "gris", "manchado", "dorado"]
zones = ["norte", "sur", "este", "oeste", "centro"]

def generate_metadata():
    dogs = []

    for file in os.listdir(EMBEDDINGS_DIR):
        if not file.endswith(".npy"):
            continue

        try:
            filename = os.path.splitext(file)[0]
            parts = filename.split("_")
            id_full = f"{parts[-2]}_{parts[-1]}"
            id_part = parts[-1]
        except Exception as e:
            print(f"[❌] Error al procesar {file}: {e}")
            continue

        dog = {
            "id": id_full,
            "name": f"Perro_{id_part}",
            "size": random.choice(sizes),
            "color": random.choice(colors),
            "age": random.randint(1, 15),
            "zone": random.choice(zones),
            "hasCollar": random.choice([True, False])
        }

        dogs.append(dog)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(dogs, f, indent=2, ensure_ascii=False)

    print(f"✅ Archivo generado con {len(dogs)} perros → {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_metadata()
