import json

def infer_traits_from_class(cnn_class_id):
    with open("scripts/class_traits.json") as f:
        traits = json.load(f)

    for item in traits:
        if str(item.get("cnn_id")) == str(cnn_class_id):
            return {
                "size": item.get("size", "desconocido"),
                "age": item.get("age", 0),
                "color": item.get("color", "mezclado"),
                "hasCollar": item.get("hasCollar", False),
            }

    return {
        "size": "desconocido",
        "age": 0,
        "color": "mezclado",
        "hasCollar": False,
    }




from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def extract_dominant_color(image_path, n_colors=3):
    image = Image.open(image_path).convert('RGB').resize((100, 100))
    pixels = np.array(image).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors).fit(pixels)
    dominant = kmeans.cluster_centers_[0].astype(int)

    r, g, b = dominant
    if r > 150 and g > 100 and b < 100:
        return "marrón"
    elif r > 200 and g > 200 and b > 200:
        return "blanco"
    elif r < 80 and g < 80 and b < 80:
        return "negro"
    else:
        return "mezclado"
