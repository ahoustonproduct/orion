"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart2, BookOpen, Brain, FileText, RefreshCw, Search, Settings, Sparkles, Zap } from "lucide-react";

const NAV_ITEMS = [
  { href: "/", icon: Zap, label: "Home" },
  { href: "/curriculum", icon: BookOpen, label: "Learn" },
  { href: "/quiz", icon: Brain, label: "Quiz" },
  { href: "/review-queue", icon: RefreshCw, label: "Review" },
  { href: "/progress", icon: BarChart2, label: "Progress" },
  { href: "/notebooks", icon: Sparkles, label: "Notebooks" },
  { href: "/notebook", icon: FileText, label: "Notes" },
  { href: "/glossary", icon: Search, label: "Glossary" },
  { href: "/settings", icon: Settings, label: "Settings" },
];

function isActivePath(pathname: string, href: string) {
  return pathname === href || (href !== "/" && pathname.startsWith(href));
}

export default function NavBar() {
  const pathname = usePathname();

  return (
    <>
      <nav aria-label="Primary navigation" className="fixed left-0 top-0 z-50 hidden h-full w-16 flex-col border-r border-border bg-surface md:flex">
        <div className="border-b border-border p-3">
          <Link
            href="/"
            aria-label="Orion Code home"
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-accent to-cyan-DEFAULT focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
          >
            <span className="text-sm font-bold text-white">O</span>
          </Link>
        </div>
        <div className="mt-2 flex flex-col gap-1 p-2">
          {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
            const active = isActivePath(pathname, href);
            return (
              <Link
                key={href}
                href={href}
                title={label}
                aria-label={label}
                aria-current={active ? "page" : undefined}
                className={`flex flex-col items-center gap-1 rounded-lg p-2 transition-all focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
                  active
                    ? "bg-accent/20 text-accent"
                    : "text-text-secondary hover:bg-surface-2 hover:text-text-primary"
                }`}
              >
                <Icon size={18} aria-hidden="true" />
                <span className="text-[10px]">{label}</span>
              </Link>
            );
          })}
        </div>
      </nav>

      <nav
        aria-label="Primary navigation"
        className="fixed bottom-0 left-0 right-0 z-50 flex overflow-x-auto border-t border-border bg-surface px-2 pb-[calc(env(safe-area-inset-bottom)+0.25rem)] pt-2 shadow-[0_-8px_24px_rgba(0,0,0,0.08)] md:hidden"
      >
        {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
          const active = isActivePath(pathname, href);
          return (
            <Link
              key={href}
              href={href}
              aria-label={label}
              aria-current={active ? "page" : undefined}
              className={`relative flex min-w-16 flex-1 flex-col items-center gap-1 rounded-lg px-2 py-2 text-center transition-all focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
                active ? "text-accent" : "text-text-muted hover:text-text-primary"
              }`}
            >
              {active && <span className="absolute left-3 right-3 top-0 h-0.5 rounded-full bg-accent" />}
              <Icon size={19} aria-hidden="true" />
              <span className="max-w-full truncate text-[10px] font-medium leading-tight">{label}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
