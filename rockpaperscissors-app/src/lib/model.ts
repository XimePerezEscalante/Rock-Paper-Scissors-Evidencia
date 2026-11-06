/**
 * Punto de conexión con el modelo de IA.
 *
 * Envía la imagen al servidor de inferencia de Python (FastAPI, `serve.py` en
 * la raíz del repositorio), que tiene cargada la CNN de piedra, papel o tijera.
 * La URL se puede cambiar con la variable de entorno MODEL_URL.
 */
import { promises as fs } from "fs";
import path from "path";

const MODEL_URL = process.env.MODEL_URL ?? "http://127.0.0.1:8000/predict";

export type ModelResult = {
  label: string;
  confidence: number;
  counter?: string; // jugada que le gana a la predicción
  raw?: unknown; // salida completa del modelo, si la necesitas
};

type ServerResponse = {
  label: string;
  confidence: number;
  probabilities: Record<string, number>;
  counter: string;
};

export async function runModel(imagePath: string): Promise<ModelResult> {
  const form = new FormData();
  form.append("image", new Blob([await fs.readFile(imagePath)]), path.basename(imagePath));

  let res: Response;
  try {
    res = await fetch(MODEL_URL, { method: "POST", body: form });
  } catch {
    throw new Error(`No se pudo conectar con el servidor del modelo (${MODEL_URL}). ¿Está corriendo serve.py?`);
  }
  if (!res.ok) {
    const detail = await res.json().then((d) => d.detail).catch(() => res.statusText);
    throw new Error(`El servidor del modelo respondió ${res.status}: ${detail}`);
  }

  const data: ServerResponse = await res.json();
  return {
    label: data.label,
    confidence: data.confidence,
    counter: data.counter,
    raw: data.probabilities,
  };
}
