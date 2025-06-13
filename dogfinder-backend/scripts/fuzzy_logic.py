import json
from typing import List, Dict, Any

Dog = Dict[str, Any]
def load_dog_metadata(db_path: str = "dogs.db"):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, size, color, age, zone, hasCollar FROM dogs")
    rows = cursor.fetchall()
    conn.close()

    keys = ["id", "name", "size", "color", "age", "zone", "hasCollar"]
    return [dict(zip(keys, row)) for row in rows]


def run_fuzzy_algorithm(dogs: List[Dog], criteria: Dict[str, Any], limit: int = 3):
    """
    Aplica lógica difusa para comparar características del formulario contra cada perro.
    Retorna los 'limit' mejores resultados con explicación y puntaje.
    """
    results = []

    for dog in dogs:
        score = 0.0
        explanation = []

        # Comparar tamaño
        if dog.get("size") == criteria.get("size"):
            score += 0.25
            explanation.append("✔️ Tamaño coincide")

        # Comparar edad ± 2 años
        try:
            if abs(int(dog.get("age", 0)) - int(criteria.get("age", 0))) <= 2:
                score += 0.20
                explanation.append("✔️ Edad similar")
        except:
            explanation.append("⚠️ Edad inválida")

        # Comparar zona
        if dog.get("zone") == criteria.get("zone"):
            score += 0.20
            explanation.append("✔️ Zona exacta")

        # Comparar color
        if dog.get("color") == criteria.get("color"):
            score += 0.20
            explanation.append("✔️ Color coincide")

        # Comparar collar
        if dog.get("hasCollar") == criteria.get("hasCollar"):
            score += 0.15
            explanation.append("✔️ Collar coincide")

        results.append({
            "dog": dog,
            "probability": round(score, 4),
            "explanation": ", ".join(explanation) or "❌ Sin coincidencias fuzzy"
        })

    results.sort(key=lambda x: x["probability"], reverse=True)
    return results[:limit]
