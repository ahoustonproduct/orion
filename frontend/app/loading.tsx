import { Loader2 } from "lucide-react";

export default function Loading() {
  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center p-8 animate-fade-in">
      <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-accent-light)] flex items-center justify-center animate-pulse mb-4 shadow-lg shadow-[var(--color-accent)]/20">
        <Loader2 size={24} className="text-white animate-spin" />
      </div>
      <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
        Loading...
      </h2>
      <p className="text-sm text-[var(--color-text-muted)] mt-2">
        Preparing your learning experience
      </p>
    </div>
  );
}
