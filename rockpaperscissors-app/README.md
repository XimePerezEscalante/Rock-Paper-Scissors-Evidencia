# Image AI

Base en Next.js (App Router + TypeScript) para subir imágenes, procesarlas con un modelo de IA y guardar los resultados en un archivo.

## Correr el proyecto

La app necesita dos procesos: el servidor del modelo (Python) y Next.js.

**1. Servidor del modelo** (en la raíz del repositorio, terminal aparte). La primera vez hay que crear el entorno de Python; ver el `README.md` de la raíz.

```bash
cd ..
.venv/bin/uvicorn serve:app --port 8000
```

**2. Next.js:**

```bash
npm install
npm run dev
```

Abre http://localhost:3000

Si el servidor del modelo corre en otra URL, defínela en `.env.local`:

```
MODEL_URL=http://127.0.0.1:8000/predict
```

## Estructura

```
src/
  app/
    page.tsx               # Página principal
    api/predict/route.ts   # POST: recibe imagen → modelo → guarda | GET: historial
  components/
    ImageUploader.tsx      # Subida (clic o arrastrar), vista previa e historial
  lib/
    model.ts               # ← AQUÍ conectas tu modelo (función runModel)
    storage.ts             # Guarda imágenes y resultados en disco
data/
  uploads/                 # Imágenes subidas
  results.json             # Resultados (se crea solo)
```

## Modelo

`src/lib/model.ts` envía cada imagen a `serve.py` (FastAPI), que tiene cargada la CNN de piedra, papel o tijera (`rps_cnn.keras`). La respuesta incluye:

- `label`: clase predicha (`rock`, `paper` o `scissors`)
- `confidence`: probabilidad de esa clase
- `counter`: jugada que le gana a la predicción (lo que "juega" el modelo)
- `raw`: probabilidades de las tres clases

Si el servidor del modelo no está corriendo, `/api/predict` responde 502 con un mensaje que lo indica.

Si cambias la forma del resultado, actualiza el tipo `ModelResult` y la tabla en `ImageUploader.tsx`.
