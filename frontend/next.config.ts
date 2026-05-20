import type { NextConfig } from "next";
import { networkInterfaces } from "node:os";

function localIpv4Hosts() {
  return Object.values(networkInterfaces())
    .flatMap((networkInterface) => networkInterface ?? [])
    .filter((address) => address.family === "IPv4" && !address.internal)
    .map((address) => address.address);
}

const allowedDevOrigins = Array.from(
  new Set([
    "localhost",
    "127.0.0.1",
    ...localIpv4Hosts(),
    ...(process.env.LAN_HOST ? [process.env.LAN_HOST] : []),
  ]),
);

const connectSources = [
  "'self'",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
  ...allowedDevOrigins.flatMap((host) => [
    `http://${host}:3000`,
    `ws://${host}:3000`,
  ]),
];

const securityHeaders = [
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "base-uri 'self'",
      "frame-ancestors 'none'",
      "object-src 'none'",
      "img-src 'self' data: blob:",
      "font-src 'self' data:",
      "style-src 'self' 'unsafe-inline'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
      `connect-src ${connectSources.join(" ")}`,
      "worker-src 'self' blob:",
      "frame-src 'none'",
    ].join("; "),
  },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  { key: "Strict-Transport-Security", value: "max-age=31536000; includeSubDomains" },
];

const nextConfig: NextConfig = {
  allowedDevOrigins,
  turbopack: {
    root: process.cwd(),
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
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
