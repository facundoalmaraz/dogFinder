"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { ArrowLeft, Percent, MapPin, Calendar } from "lucide-react";

interface DogResult {
  id: number;
  filename: string;
  similarity: number;
  location?: string;
  contact?: string;
  date?: string;
}

export default function ResultadoPage() {
  const [results, setResults] = useState<DogResult[]>([]);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const storedResults = localStorage.getItem("dogfinder_result");
    const storedImage = localStorage.getItem("dogfinder_image");

    if (storedImage) {
      setUploadedImage(storedImage);
    }

    if (storedResults) {
      try {
        const parsedData = JSON.parse(storedResults);

        if (parsedData.top_matches && Array.isArray(parsedData.top_matches)) {
          const realResults: DogResult[] = parsedData.top_matches.map(
            (match: any, index: number) => ({
              id: index + 1,
              filename: match.path.replace(/\n/g, ""),
              similarity: match.score_total, // ← usamos el puntaje combinado visual + fuzzy
              cnn_similarity: match.cnn_similarity,
              fuzzy_probability: match.fuzzy_probability,
              fuzzy_explanation: match.fuzzy_explanation,
              location: "Ubicación desconocida",
              contact: "Sin datos",
              date: "Fecha no disponible",
            })
          );
          setResults(realResults);
        }
      } catch (error) {
        console.error("Error al procesar los resultados:", error);
      }
    }

    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-100">
      <div className="max-w-4xl mx-auto p-6">
        <header className="mb-8 pt-6">
          <button
            onClick={() => router.push("/")}
            className="flex items-center text-amber-700 hover:text-amber-900 mb-6"
          >
            <ArrowLeft size={18} className="mr-2" />
            Volver al formulario
          </button>

          <h1 className="text-3xl font-bold text-amber-800 mb-2">
            Resultados de la búsqueda
          </h1>
          <p className="text-amber-700">
            Hemos encontrado posibles coincidencias con tu mascota perdida
          </p>
        </header>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-amber-700"></div>
            <p className="mt-4 text-amber-800">Buscando coincidencias...</p>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="p-6 bg-amber-600 text-white">
              <h2 className="text-xl font-semibold">Tu mascota</h2>
            </div>

            {uploadedImage && (
              <div className="p-6 border-b">
                <div className="flex flex-col md:flex-row items-center">
                  <div className="md:w-1/3 mb-4 md:mb-0">
                    <div className="h-48 w-48 mx-auto relative">
                      <Image
                        src={uploadedImage}
                        alt="Tu mascota"
                        width={192}
                        height={192}
                        className="object-cover rounded-lg"
                        unoptimized // necesario si usás blobs (URL.createObjectURL)
                      />
                    </div>
                  </div>
                  <div className="md:w-2/3 md:pl-6">
                    <h3 className="text-lg font-medium text-gray-800 mb-2">
                      Imagen subida
                    </h3>
                    <p className="text-gray-600 mb-4">
                      Hemos analizado esta imagen y encontrado {results.length}{" "}
                      posibles coincidencias.
                    </p>
                    <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                      <p className="text-sm text-amber-800">
                        Las coincidencias se ordenan por porcentaje de
                        similitud. Te recomendamos contactar a las personas que
                        han reportado haber visto perros similares al tuyo.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Posibles coincidencias
              </h2>

              <div className="space-y-6">
                {results.map((result) => (
                  <div
                    key={result.id}
                    className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow"
                  >
                    <div className="flex flex-col md:flex-row">
                      <div className="md:w-1/4 bg-gray-100 p-4 flex items-center justify-center">
                        <div className="relative h-32 w-32 rounded overflow-hidden bg-gray-200">
                          <Image
                            src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/${result.filename}`}
                            alt={`Imagen ${result.id}`}
                            fill
                            className="object-cover"
                            unoptimized
                          />
                        </div>
                      </div>
                      <div className="md:w-3/4 p-4">
                        <div className="flex justify-between items-start mb-3">
                          <h3 className="text-lg font-medium text-gray-800">
                            Coincidencia #{result.id}
                          </h3>
                          <div className="flex items-center bg-amber-100 text-amber-800 px-3 py-1 rounded-full">
                            <Percent size={16} className="mr-1" />
                            <span className="font-medium">
                              {Math.round(result.similarity * 100)}% similar
                            </span>
                          </div>
                        </div>

                        <div className="space-y-2 text-sm text-gray-600">
                          <div className="flex items-start">
                            <MapPin
                              size={16}
                              className="mr-2 mt-0.5 text-amber-500 flex-shrink-0"
                            />
                            <span>{result.location}</span>
                          </div>
                          <div className="flex items-start">
                            <Calendar
                              size={16}
                              className="mr-2 mt-0.5 text-amber-500 flex-shrink-0"
                            />
                            <span>{result.date}</span>
                          </div>
                        </div>

                        <div className="mt-4 pt-3 border-t">
                          <p className="font-medium text-gray-700">Contacto:</p>
                          <p className="text-amber-600">{result.contact}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {results.length === 0 && (
                <div className="text-center py-10">
                  <p className="text-gray-500">
                    No se encontraron coincidencias. Intenta con otra imagen o
                    diferentes criterios.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        <footer className="mt-8 text-center text-sm text-amber-700">
          <p>© 2023 DogFinder - Ayudando a reunir mascotas con sus familias</p>
        </footer>
      </div>
    </div>
  );
}
