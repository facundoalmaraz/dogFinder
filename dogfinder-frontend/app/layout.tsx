import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "DogFinder - Encuentra a tu mascota perdida",
  description: "Ayudamos a reunir mascotas perdidas con sus familias",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="es">
      <body className="dark:bg-gray-900 dark:text-white text-gray-900">
        {children}
      </body>
    </html>
  );
}
