"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, Flame, Zap, FileText, Search, Settings, BarChart2, RefreshCw } from "lucide-react";

const NAV_ITEMS = [
  { href: "/", icon: Zap, label: "Home" },
  { href: "/curriculum", icon: BookOpen, label: "Learn" },
  { href: "/quiz", icon: Flame, label: "Quiz" },
  { href: "/review-queue", icon: RefreshCw, label: "Review" },
  { href: "/progress", icon: BarChart2, label: "Progress" },
  { href: "/notebook", icon: FileText, label: "Notes" },
  { href: "/glossary", icon: Search, label: "Glossary" },
  { href: "/settings", icon: Settings, label: "Settings" },
];

export default function NavBar() {
  const pathname = usePathname();

  return (
    <>
      {/* Desktop sidebar */}
      <nav className="hidden md:flex flex-col fixed left-0 top-0 h-full w-16 bg-surface border-r border-border z-50">
        <div className="p-3 border-b border-border">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-cyan-DEFAULT flex items-center justify-center">
            <span className="text-white font-bold text-sm">O</span>
          </div>
        </div>
        <div className="flex flex-col gap-1 p-2 mt-2">
          {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
            const active = pathname === href || (href !== "/" && pathname.startsWith(href));
            return (
              <Link
                key={href}
                href={href}
                title={label}
                className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
                  active
                    ? "bg-accent/20 text-accent"
                    : "text-text-secondary hover:text-text-primary hover:bg-surface-2"
                }`}
              >
                <Icon size={18} />
                <span className="text-[10px]">{label}</span>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Mobile bottom bar */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-surface border-t border-border z-50 flex">
        {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
          const active = pathname === href || (href !== "/" && pathname.startsWith(href));
          return (
            <Link
              key={href}
              href={href}
              className={`flex-1 flex flex-col items-center gap-1 py-2 px-1 transition-all ${
                active ? "text-accent" : "text-text-muted"
              }`}
            >
              <Icon size={18} />
              <span className="text-[9px]">{label}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
