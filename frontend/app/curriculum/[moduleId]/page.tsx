import ModulePageClient, { type ModuleExtended } from "@/components/ModulePageClient";

export const dynamic = "force-dynamic";

interface ModulePageProps {
  params: Promise<{ moduleId: string }>;
}

async function fetchInitialModule(moduleId: string): Promise<{
  module: ModuleExtended | null;
  error: string | null;
}> {
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

  try {
    const res = await fetch(`${backendUrl}/curriculum/modules/${moduleId}`, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`Initial module fetch failed: ${res.status}`);
    }

    return {
      module: (await res.json()) as ModuleExtended,
      error: null,
    };
  } catch (error) {
    console.error("Module initial fetch failed", error);
    return {
      module: null,
      error: "Module could not be loaded from the backend.",
    };
  }
}

export default async function ModulePage({ params }: ModulePageProps) {
  const { moduleId } = await params;
  const initial = await fetchInitialModule(moduleId);

  return (
    <ModulePageClient
      moduleId={moduleId}
      initialModule={initial.module}
      initialModuleError={initial.error}
    />
  );
}
