import { promises as fs } from "fs";
import path from "path";
import type { ModelResult } from "./model";

const DATA_DIR = path.join(process.cwd(), "data");
export const UPLOADS_DIR = path.join(DATA_DIR, "uploads");
const RESULTS_FILE = path.join(DATA_DIR, "results.json");

export type ResultRecord = {
  id: string;
  originalName: string;
  storedAs: string;
  size: number;
  createdAt: string;
  result: ModelResult;
};

export async function saveImage(file: File): Promise<{ id: string; storedAs: string; fullPath: string }> {
  await fs.mkdir(UPLOADS_DIR, { recursive: true });
  const id = crypto.randomUUID();
  const ext = path.extname(file.name).toLowerCase() || ".png";
  const storedAs = `${id}${ext}`;
  const fullPath = path.join(UPLOADS_DIR, storedAs);
  await fs.writeFile(fullPath, Buffer.from(await file.arrayBuffer()));
  return { id, storedAs, fullPath };
}

export async function readResults(): Promise<ResultRecord[]> {
  try {
    return JSON.parse(await fs.readFile(RESULTS_FILE, "utf8"));
  } catch {
    return [];
  }
}

export async function appendResult(record: ResultRecord): Promise<void> {
  await fs.mkdir(DATA_DIR, { recursive: true });
  const all = await readResults();
  all.unshift(record);
  await fs.writeFile(RESULTS_FILE, JSON.stringify(all, null, 2));
}
