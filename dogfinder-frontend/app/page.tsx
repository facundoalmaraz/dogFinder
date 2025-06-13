"use client";

import type React from "react";

import { useRouter } from "next/navigation";
import { useState } from "react";
import {
  Camera,
  MapPin,
  Calendar,
  Palette,
  Tag,
  Search,
  Upload,
} from "lucide-react";
import Image from "next/image";

export default function HomePage() {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [formData, setFormData] = useState({
    size: "",
    age: "",
    zone: "",
    color: "",
    hasCollar: false,
  });

  const router = useRouter();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setIsUploading(true);
      setImage(file);
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);

      // 🧠 Llamada al backend para auto-análisis
      const autoForm = new FormData();
      autoForm.append("image", file);

      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/auto-analyze`,
          {
            method: "POST",
            body: autoForm,
          }
        );
        const data = await res.json();

        setFormData((prev) => ({
          ...prev,
          size: data.size || "",
          age: data.age || "",
          color: data.color || "",
          hasCollar: data.hasCollar || false,
        }));
      } catch (err) {
        console.error("Error al autocompletar:", err);
      }

      setTimeout(() => setIsUploading(false), 800);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!image) return alert("Debes subir una imagen");

    const body = new FormData();
    body.append("image", image);
    Object.entries(formData).forEach(([key, value]) => {
      body.append(key, value.toString());
    });

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/compare`, {
        method: "POST",
        body,
      });

      const data = await res.json();

      // 🟨 Si hay traits sugeridos, los usamos
      if (data.traits) {
        setFormData((prev) => ({
          ...prev,
          size: data.traits.size || "",
          age: data.traits.age?.toString() || "",
        }));
      }

      // Guardar resultados para la página de resultado
      localStorage.setItem("dogfinder_result", JSON.stringify(data));
      localStorage.setItem("dogfinder_image", URL.createObjectURL(image));

      router.push("/resultado");
    } catch (error) {
      console.error("Error al enviar datos:", error);
      alert(
        "Hubo un error al procesar tu solicitud. Por favor intenta nuevamente."
      );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-100">
      <div className="max-w-4xl mx-auto p-6">
        <header className="text-center mb-10 pt-8">
          <h1 className="text-4xl font-bold text-amber-800 mb-2">
            Encuentra a tu amigo peludo
          </h1>
          <p className="text-amber-700 max-w-2xl mx-auto">
            Completa el formulario con los datos de tu mascota perdida y te
            ayudaremos a encontrar coincidencias
          </p>
        </header>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="md:flex">
            <div className="md:w-2/5 bg-amber-600 p-8 text-white">
              <div className="h-full flex flex-col">
                <h2 className="text-2xl font-bold mb-6">¿Cómo funciona?</h2>
                <ol className="space-y-6 flex-grow">
                  <li className="flex items-start">
                    <div className="bg-amber-500 rounded-full p-2 mr-4 mt-1">
                      <Camera size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">Sube una foto</h3>
                      <p className="text-amber-100">
                        Sube una imagen clara de tu mascota perdida
                      </p>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <div className="bg-amber-500 rounded-full p-2 mr-4 mt-1">
                      <Tag size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">Añade detalles</h3>
                      <p className="text-amber-100">
                        Completa la información sobre tu mascota
                      </p>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <div className="bg-amber-500 rounded-full p-2 mr-4 mt-1">
                      <Search size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">
                        Encuentra coincidencias
                      </h3>
                      <p className="text-amber-100">
                        Nuestro sistema buscará coincidencias en nuestra base de
                        datos
                      </p>
                    </div>
                  </li>
                </ol>
                <div className="mt-8">
                  <div className="bg-amber-500/30 p-4 rounded-lg">
                    <p className="text-sm">
                      Ya hemos ayudado a reunir más de 500 mascotas con sus
                      familias. ¡Tu amigo podría ser el siguiente!
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="md:w-3/5 p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">
                Datos de tu mascota
              </h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Subida de imagen */}
                <div className="mb-8">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Foto de tu mascota
                  </label>
                  <div
                    className={`border-2 border-dashed rounded-lg ${
                      preview ? "border-amber-300" : "border-gray-300"
                    } transition-all hover:border-amber-500 bg-gray-50 p-4 text-center cursor-pointer relative`}
                  >
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImage}
                      required
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    />

                    {isUploading ? (
                      <div className="py-8">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-700 mx-auto"></div>
                        <p className="mt-2 text-sm text-gray-500">
                          Procesando imagen...
                        </p>
                      </div>
                    ) : preview ? (
                      <div className="relative">
                        <Image
                          src={preview || "/placeholder.svg"}
                          alt="Vista previa"
                          width={300}
                          height={300}
                          className="mx-auto h-48 object-contain"
                        />
                        <button
                          type="button"
                          onClick={() => {
                            setPreview(null);
                            setImage(null);
                          }}
                          className="mt-2 text-xs text-amber-600 hover:text-amber-800"
                        >
                          Cambiar imagen
                        </button>
                      </div>
                    ) : (
                      <div className="py-8">
                        <Upload className="mx-auto h-12 w-12 text-amber-500" />
                        <p className="mt-2 text-sm text-gray-500">
                          Haz clic para subir o arrastra una imagen aquí
                        </p>
                        <p className="text-xs text-gray-400 mt-1">
                          PNG, JPG, GIF hasta 10MB
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {/* Tamaño */}
                  <div>
                    <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                      <Tag size={16} className="mr-2 text-amber-500" />
                      Tamaño
                    </label>
                    <select
                      name="size"
                      value={formData.size}
                      onChange={handleChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent text-black"
                    >
                      <option value="">Seleccionar...</option>
                      <option value="pequeño">Pequeño</option>
                      <option value="mediano">Mediano</option>
                      <option value="grande">Grande</option>
                    </select>
                  </div>

                  {/* Edad */}
                  <div>
                    <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                      <Calendar size={16} className="mr-2 text-amber-500" />
                      Edad (años)
                    </label>
                    <input
                      name="age"
                      type="number"
                      min={0}
                      value={formData.age}
                      onChange={handleChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent text-black"
                    />
                  </div>

                  {/* Zona */}
                  <div>
                    <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                      <MapPin size={16} className="mr-2 text-amber-500" />
                      Zona donde se perdió
                    </label>
                    <input
                      name="zone"
                      type="text"
                      value={formData.zone}
                      onChange={handleChange}
                      required
                      placeholder="Ej: Parque Central, Avenida Principal"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent text-black"
                    />
                  </div>

                  {/* Color */}
                  <div>
                    <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                      <Palette size={16} className="mr-2 text-amber-500" />
                      Color predominante
                    </label>
                    <input
                      name="color"
                      type="text"
                      value={formData.color}
                      onChange={handleChange}
                      required
                      placeholder="Ej: Marrón, Negro con manchas blancas"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent text-black"
                    />
                  </div>
                </div>

                {/* Collar */}
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="hasCollar"
                    name="hasCollar"
                    checked={formData.hasCollar}
                    onChange={handleChange}
                    className="h-4 w-4 text-amber-600 focus:ring-amber-500 border-gray-300 rounded"
                  />
                  <label
                    htmlFor="hasCollar"
                    className="ml-2 block text-sm text-gray-700"
                  >
                    Tiene collar o identificación
                  </label>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-amber-500 to-amber-700 text-white font-medium py-3 px-4 rounded-lg hover:from-amber-600 hover:to-amber-800 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2 shadow-md transition-all flex items-center justify-center"
                >
                  <Search size={18} className="mr-2" />
                  Buscar coincidencias
                </button>
              </form>
            </div>
          </div>
        </div>

        <footer className="mt-8 text-center text-sm text-amber-700">
          <p>© 2023 DogFinder - Ayudando a reunir mascotas con sus familias</p>
        </footer>
      </div>
    </div>
  );
}
