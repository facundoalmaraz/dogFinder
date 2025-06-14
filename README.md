# 🐶 DogFinder: Sistema Inteligente de Reconocimiento de Perros

DogFinder es un sistema híbrido que combina **redes neuronales convolucionales (CNN)** y **lógica difusa (fuzzy logic)** para identificar perros a partir de una foto y características físicas ingresadas por el usuario. Ideal para ayudar a encontrar mascotas perdidas.

---

## 🚀 Tecnologías utilizadas

- **Python** + **FastAPI** (backend API)
- **Torch / torchvision** (modelo de visión por computadora)
- **SQLite** o `.json` para metadatos
- **Fuzzy Logic** para análisis de características
- **Next.js 14** (frontend con App Router)

---

## 📁 Estructura del proyecto

```
dogfinder-backend/  
├── main.py                   # API principal FastAPI  
├── scripts/  
│   ├── combined_fuzzy.py       # Mezcla resultados CNN + fuzzy  
│   ├── cnn_compare.py          # Comparación visual con embeddings  
│   ├── fuzzy_logic.py          # Algoritmo fuzzy  
│   ├── retrain_model.py        # Reentrenar modelo CNN con nuevos datos  
│   ├── generate_embeddings.py  # Generar embeddings .npy  
│   └── metadata_generator.py   # Crear metadata desde embeddings  
├── embeddings_custom/       # Archivos .npy con embeddings de imágenes  
├── dataset/Images/          # Dataset de imágenes (por clase)  
├── new_samples/             # Nuevas imágenes subidas por usuarios  
├── dogs_metadata.json       # Metadata de perros (alternativa a SQLite)  
├── dogs.db                  # Base de datos SQLite con metadatos  
```


### 📜 Scripts disponibles (`scripts/`)

| Script                          | Descripción                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `auto_traits.py`                | Inferencia automática de tamaño y edad aproximada según clase CNN          |
| `cnn_compare.py`                | Extrae embedding de una imagen y lo compara contra todos los `.npy`        |
| `combined_fuzzy.py`            | Combina resultados visuales (CNN) con lógica difusa y devuelve top matches |
| `compare_image.py`             | Prueba local: compara una imagen suelta y muestra resultados en consola    |
| `db_setup.py`                  | Crea la base de datos `dogs.db` e importa desde `dogs_metadata.json`       |
| `download_sample_dataset.py`   | (opcional) Descarga un dataset de ejemplo si no tenés uno propio           |
| `extract_embeddings_custom.py` | Genera `.npy` con embeddings desde imágenes con modelo entrenado           |
| `fuzzy_logic.py`               | Implementación del algoritmo difuso basado en metadatos (JSON o SQLite)    |
| `generate_dogs_metadata.py`    | Genera archivo `dogs_metadata.json` con datos simulados                    |
| `train_model.py`               | Entrena o reentrena la red neuronal CNN (`resnet50_finetuned.pth`)         |



