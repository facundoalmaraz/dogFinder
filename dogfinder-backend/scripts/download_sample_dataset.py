import os
import urllib.request
import tarfile


url = "http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar"
dataset_dir = "dataset"


os.makedirs(dataset_dir, exist_ok=True)


tar_path = os.path.join(dataset_dir, "images.tar")

print("Descargando el dataset (esto puede tardar un rato)...")
urllib.request.urlretrieve(url, tar_path)

print("Descomprimiendo...")
with tarfile.open(tar_path) as tar:
    tar.extractall(path=dataset_dir)

print("Limpieza del archivo .tar...")
os.remove(tar_path)

print("Listo. Las imágenes están en 'dataset/Images/'")
