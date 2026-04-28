"use client";

import { useEffect } from "react";
import { AlertTriangle, RefreshCcw } from "lucide-react";
import Link from "next/link";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center p-8 text-center animate-fade-in">
      <div className="w-16 h-16 rounded-2xl bg-red-500/10 flex items-center justify-center mb-6">
        <AlertTriangle size={32} className="text-red-500" />
      </div>
      <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-3">
        Something went wrong!
      </h2>
      <p className="text-[var(--color-text-secondary)] mb-8 max-w-md mx-auto">
        We encountered an unexpected error while loading this page. Our team has been notified.
      </p>
      <div className="flex gap-4">
        <button
          onClick={() => reset()}
          className="flex items-center gap-2 px-6 py-3 bg-[var(--color-surface-2)] border border-[var(--color-border)] hover:border-[var(--color-accent)] text-[var(--color-text-primary)] rounded-xl font-medium transition-all"
        >
          <RefreshCcw size={18} />
          Try again
        </button>
        <Link
          href="/"
          className="px-6 py-3 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-white rounded-xl font-medium transition-all shadow-lg shadow-[var(--color-accent)]/20"
        >
          Go to Dashboard
        </Link>
      </div>
    </div>
  );
}
