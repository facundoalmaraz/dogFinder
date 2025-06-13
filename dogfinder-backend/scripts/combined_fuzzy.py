import numpy as np
from scripts.cnn_compare import compare_image_to_embeddings
from scripts.fuzzy_logic import run_fuzzy_algorithm, load_dog_metadata

def process_image_and_criteria(image_path, size, age, zone, color, has_collar):
    # Paso 1: Comparación visual (CNN)
    top_matches = compare_image_to_embeddings(image_path)
    top_ids = [match["id"] for match in top_matches]

    # Paso 2: Cargar metadatos de perros
    dogs = load_dog_metadata()
    filtered_dogs = [d for d in dogs if d["id"] in top_ids]

    # DEBUG opcional
    print(f"🐾 Criterios recibidos: {size}, {age}, {zone}, {color}, {has_collar}")
    print(f"🔎 Filtrando lógica fuzzy sobre {len(filtered_dogs)} perros")

    # Paso 3: Ejecutar lógica fuzzy sobre los top visuales
    fuzzy_results = run_fuzzy_algorithm(
        filtered_dogs,
        {
            "size": size,
            "age": int(age),
            "zone": zone,
            "color": color,
            "hasCollar": has_collar,
        }
    )

    # Paso 4: Unir visual + fuzzy por ID
    final_results = []
    for match in top_matches:
        fuzzy_match = next((f for f in fuzzy_results if f["dog"]["id"] == match["id"]), None)
        score_fuzzy = fuzzy_match["probability"] if fuzzy_match else 0.0
        explanation = fuzzy_match["explanation"] if fuzzy_match else "Sin explicación fuzzy"

        score_total = 0.7 * match["similarity"] + 0.3 * score_fuzzy

        final_results.append({
            "id": match["id"],
            "cnn_similarity": float(match["similarity"]),
            "fuzzy_probability": float(score_fuzzy),
            "score_total": float(score_total),
            "path": match["path"],
            "class": match["class"],
            "fuzzy_explanation": explanation
        })

    # Paso 5: Ordenar por score combinado
    final_results.sort(key=lambda x: x["score_total"], reverse=True)

    return {
        "cnn_class_id": top_matches[0]["id"],
        "top_matches": final_results
    }
