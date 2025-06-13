import sys
import json
from cnn_compare import compare_image_to_embeddings

# ✅ Leer argumentos desde Node.js (Next.js API)
# python combined_fuzzy.py imagen.jpg tamaño edad zona color collar
args = sys.argv
if len(args) != 7:
    print(json.dumps({ "error": "Argumentos incompletos" }))
    sys.exit(1)

image_path, size, age, zone, color, has_collar = args[1:]

# 🐍 Simulación: análisis visual
cnn_result = compare_image_to_embeddings(image_path)
similarity = cnn_result["similarity"]

# 🧠 Clasificación difusa
def fuzzy_similarity(sim):
    if sim >= 0.9:
        return "alta"
    elif sim >= 0.75:
        return "media"
    else:
        return "baja"

similarity_grade = fuzzy_similarity(similarity)

# ⚙️ Simulación del sistema fuzzy real
# (acá deberías integrar tu lógica actual si querés)
fuzzy_result = {
    "dogId": cnn_result["id"],
    "similarity": round(similarity, 4),
    "similarityGrade": similarity_grade,
    "formData": {
        "size": size,
        "age": age,
        "zone": zone,
        "color": color,
        "hasCollar": has_collar == "true"
    },
    "explanation": f"Similitud visual {similarity_grade}. Zona y tamaño similares.",
    "probability": 0.83 if similarity_grade == "alta" else 0.6
}

# 🟢 Salida para Next.js
print(json.dumps(fuzzy_result))
sys.exit(0)
