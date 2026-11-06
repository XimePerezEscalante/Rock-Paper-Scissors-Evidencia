import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image AI",
  description: "Sube imágenes y analízalas con tu modelo",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
