import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    // Límite de tamaño para subir imágenes desde Server Actions / formularios
    serverActions: { bodySizeLimit: "10mb" },
  },
};

export default nextConfig;
