import type { NextConfig } from "next";

const allowedDevOrigins = ["localhost", "127.0.0.1", "192.168.1.210"];

if (process.env.LAN_HOST && !allowedDevOrigins.includes(process.env.LAN_HOST)) {
  allowedDevOrigins.push(process.env.LAN_HOST);
}

const nextConfig: NextConfig = {
  allowedDevOrigins,
  turbopack: {
    root: process.cwd(),
  },
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
