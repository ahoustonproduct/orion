import DashboardClient from "@/components/DashboardClient";
import type { Module } from "@/lib/api";

export const dynamic = "force-dynamic";

async function fetchInitialModules(): Promise<{ modules: Module[]; modulesError: string | null }> {
  const backendUrl = process.env.BACKEND_URL || "http://127.0.0.1:8000";

  try {
    const res = await fetch(`${backendUrl}/curriculum/modules`, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`Initial module fetch failed: ${res.status}`);
    }

    const modules = (await res.json()) as Module[];
    return { modules, modulesError: null };
  } catch (error) {
    console.error("Dashboard initial module fetch failed", error);
    return {
      modules: [],
      modulesError: "Modules could not be loaded from the backend.",
    };
  }
}

export default async function DashboardPage() {
  const { modules, modulesError } = await fetchInitialModules();

  return (
    <DashboardClient
      initialModules={modules}
      initialModulesError={modulesError}
    />
  );
}
