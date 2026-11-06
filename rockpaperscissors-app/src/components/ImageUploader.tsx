"use client";

import { useEffect, useRef, useState } from "react";

type Record = {
  id: string;
  originalName: string;
  createdAt: string;
  result: { label: string; confidence: number; counter?: string };
};

export default function ImageUploader() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<Record[]>([]);

  useEffect(() => {
    fetch("/api/predict").then((r) => r.json()).then(setHistory).catch(() => {});
  }, []);

  useEffect(() => {
    if (!file) return setPreview(null);
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  function pick(f: File | undefined) {
    setError(null);
    if (f && f.type.startsWith("image/")) setFile(f);
    else if (f) setError("Select an image.");
  }

  async function submit() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const body = new FormData();
      body.append("image", file);
      const res = await fetch("/api/predict", { method: "POST", body });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Error al procesar la imagen");
      setHistory((h) => [data, ...h]);
      setFile(null);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <section >
        <section className="card">

        
        <div
          className={`dropzone ${dragging ? "active" : ""} lekton-regular`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => { e.preventDefault(); setDragging(false); pick(e.dataTransfer.files[0]); }}
        >
          {file ? file.name : "Drop your image or click to select one from your files"}
          <input
            ref={inputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            hidden
            onChange={(e) => pick(e.target.files?.[0])}
          />
        </div>
        {preview && <img src={preview} alt="Vista previa" className="preview" />}
        {error && <p className="error">{error}</p>}
        <button className="lekton-regular" onClick={submit} disabled={!file || loading}>
          {loading ? "Loading..." : "Send"}
        </button>
        </section>
        <section className="card">

        </section>
      </section>

      <section className="card lekton-regular">
        <h2 style={{ marginTop: 0, fontSize: "1rem" }}>Resultados guardados</h2>
        {history.length === 0 ? (
          <p className="muted">Aún no hay resultados.</p>
        ) : (
          <table>
            <thead style={{ marginTop: 0, fontSize: "0.7rem" }}>
              <tr><th>Imagen</th><th>Resultado</th><th>Confianza</th><th>El modelo juega</th><th>Fecha</th></tr>
            </thead>
            <tbody style={{ marginTop: 0, fontSize: "0.5rem" }}>
              {history.map((r) => (
                <tr key={r.id}>
                  <td>{r.originalName}</td>
                  <td>{r.result.label}</td>
                  <td>{(r.result.confidence * 100).toFixed(1)}%</td>
                  <td>{r.result.counter ?? "—"}</td>
                  <td>{new Date(r.createdAt).toLocaleString("es-MX")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </>
  );
}
