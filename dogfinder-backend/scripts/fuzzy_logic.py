import json
from typing import List, Dict, Any

Dog = Dict[str, Any]

def load_dog_metadata(path: str = "data/dogs_metadata.json") -> List[Dog]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_fuzzy_algorithm(dogs: List[Dog], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = []
    for dog in dogs:
        score = 0
        explanation = []

        # Tamaño
        if criteria["size"] == dog["size"]:
            score += 0.3
            explanation.append(f"tamaño {dog['size']}")

        # Color
        if criteria["color"] == dog["color"]:
            score += 0.2
            explanation.append(f"color {dog['color']}")

        # Edad (más cerca = mejor)
        age_diff = abs(int(criteria["age"]) - int(dog["age"]))
        if age_diff == 0:
            score += 0.2
            explanation.append("edad exacta")
        elif age_diff <= 2:
            score += 0.1
            explanation.append("edad cercana")

        # Zona
        if criteria["zone"].lower() == dog["zone"].lower():
            score += 0.2
            explanation.append(f"zona {dog['zone']}")

        # Collar
        if bool(criteria["hasCollar"]) == bool(dog["hasCollar"]):
            score += 0.1
            explanation.append("coincide collar")

        results.append({
            "dog": dog,
            "probability": round(score, 3),
            "explanation": ", ".join(explanation)
        })

    results.sort(key=lambda x: x["probability"], reverse=True)
    return results
