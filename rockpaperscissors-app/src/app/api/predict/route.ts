import { NextResponse } from "next/server";
import { runModel } from "@/lib/model";
import { appendResult, readResults, saveImage } from "@/lib/storage";

export const runtime = "nodejs";

const ALLOWED = ["image/jpeg", "image/png", "image/webp"];
const MAX_BYTES = 10 * 1024 * 1024;

// POST /api/predict  — recibe una imagen (campo "image"), la guarda, corre el modelo y guarda el resultado
export async function POST(req: Request) {
  const form = await req.formData();
  const file = form.get("image");

  if (!(file instanceof File)) {
    return NextResponse.json({ error: "Falta el archivo 'image'." }, { status: 400 });
  }
  if (!ALLOWED.includes(file.type)) {
    return NextResponse.json({ error: "Formato no permitido (usa JPG, PNG o WEBP)." }, { status: 415 });
  }
  if (file.size > MAX_BYTES) {
    return NextResponse.json({ error: "La imagen supera 10 MB." }, { status: 413 });
  }

  const { id, storedAs, fullPath } = await saveImage(file);
  let result;
  try {
    result = await runModel(fullPath);
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 502 });
  }

  const record = {
    id,
    originalName: file.name,
    storedAs,
    size: file.size,
    createdAt: new Date().toISOString(),
    result,
  };
  await appendResult(record);

  return NextResponse.json(record);
}

// GET /api/predict — historial de resultados guardados
export async function GET() {
  return NextResponse.json(await readResults());
}
