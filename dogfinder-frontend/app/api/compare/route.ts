import { NextRequest, NextResponse } from "next/server"
import { writeFile, mkdir } from "fs/promises"
import path from "path"
import { spawn } from "child_process"
import os from "os"

export async function POST(req: NextRequest) {
  const formData = await req.formData()

  const image = formData.get("image") as File
  const size = formData.get("size") as string
  const age = formData.get("age") as string
  const zone = formData.get("zone") as string
  const color = formData.get("color") as string
  const hasCollar = formData.get("hasCollar") === "true"

  if (!image || !image.name) {
    return NextResponse.json({ error: "No se recibió imagen" }, { status: 400 })
  }

  // 📁 Guardar imagen en /tmp para que Python pueda leerla
  const bytes = await image.arrayBuffer()
  const buffer = Buffer.from(bytes)

  const tempDir = path.join(os.tmpdir(), "dogfinder")
  await mkdir(tempDir, { recursive: true })

  const filePath = path.join(tempDir, "imagen_usuario.jpg")
  await writeFile(filePath, buffer)

  // 🐍 Llamar a Python
  return new Promise((resolve) => {
    const py = spawn("python", [
      "scripts/combined_fuzzy.py",
      filePath,
      size,
      age,
      zone,
      color,
      hasCollar ? "true" : "false",
    ])

    let output = ""
    py.stdout.on("data", (data) => {
      output += data.toString()
    })

    let error = ""
    py.stderr.on("data", (data) => {
      error += data.toString()
    })

    py.on("close", (code) => {
      if (code !== 0) {
        return resolve(
          NextResponse.json({ error: "Error al ejecutar Python", details: error }, { status: 500 })
        )
      }

      try {
        const result = JSON.parse(output)
        resolve(NextResponse.json(result))
      } catch (err) {
        resolve(NextResponse.json({ error: "Error al parsear JSON", raw: output }, { status: 500 }))
      }
    })
  })
}
