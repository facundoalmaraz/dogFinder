import numpy as np
from scripts.cnn_compare import compare_image_to_embeddings
from scripts.fuzzy_logic import run_fuzzy_algorithm, load_dog_metadata

def process_image_and_criteria(image_path, size, age, zone, color, has_collar):
    # Buscar las 5 imágenes más parecidas
    top_matches = compare_image_to_embeddings(image_path)
    top1 = top_matches[0]  # el más similar visualmente

    # Cargar metadatos simulados (BD con descripción de perros)
    dogs = load_dog_metadata()

    # Ejecutar lógica fuzzy sobre los datos ingresados
    fuzzy_results = run_fuzzy_algorithm(
        dogs,
        {
            "size": size,
            "age": age,
            "zone": zone,
            "color": color,
            "hasCollar": has_collar,
        }
    )

    # Obtener mejor resultado fuzzy (mayor probabilidad)
    best_match = fuzzy_results[0]

    # Crear respuesta combinada
    response = {
        "cnn_class_id": top1["id"],
        "cnn_similarity": float(top1["similarity"]),
        "fuzzy_match_id": int(best_match["dog"]["id"]),
        "fuzzy_probability": float(best_match["probability"]),
        "fuzzy_explanation": str(best_match["explanation"]),
        "top_matches": top_matches  # ← incluye path, similarity e id de los 5 más parecidos
    }

    return response
