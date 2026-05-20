import { NextRequest, NextResponse } from "next/server";

const LOOPBACK_HOSTS = new Set(["localhost", "127.0.0.1", "::1", "[::1]"]);
const LOCAL_ONLY_EXECUTION_MESSAGE =
  "Code execution is limited to local browser sessions. " +
  "Set ORION_ALLOW_REMOTE_EXECUTION=1 only on a trusted network.";

function requestHost(request: NextRequest) {
  const rawHost =
    request.headers.get("x-forwarded-host") ?? request.headers.get("host") ?? "";
  if (rawHost.startsWith("[") && rawHost.includes("]")) {
    return rawHost.slice(1, rawHost.indexOf("]")).toLowerCase();
  }
  return rawHost.split(":")[0].toLowerCase();
}

export function proxy(request: NextRequest) {
  if (process.env.ORION_ALLOW_REMOTE_EXECUTION === "1") {
    return NextResponse.next();
  }

  const host = requestHost(request);
  if (!LOOPBACK_HOSTS.has(host)) {
    return NextResponse.json(
      {
        error: LOCAL_ONLY_EXECUTION_MESSAGE,
      },
      { status: 403 },
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/api/execute/:path*"],
};
