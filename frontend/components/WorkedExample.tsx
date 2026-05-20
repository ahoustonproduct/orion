"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, Eye } from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";

interface WorkedExampleProps {
  description: string;
  code: string;
  explanation: string;
}

function ExampleMarkdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      rehypePlugins={[rehypeSanitize]}
      components={{
        pre: ({ children }) => (
          <pre className="overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[#161413] p-4 text-sm text-[#f5f0e8]">
            {children}
          </pre>
        ),
        code: ({ className, children }) => {
          const isBlock = Boolean(className);
          return isBlock ? (
            <code className={`${className} font-mono leading-relaxed`}>{children}</code>
          ) : (
            <code className="rounded border border-[var(--color-border)] bg-[var(--color-surface-2)] px-1.5 py-0.5 font-mono text-[var(--color-accent)]">
              {children}
            </code>
          );
        },
        p: ({ children }) => <p className="text-sm leading-relaxed text-[var(--color-text-secondary)]">{children}</p>,
        ul: ({ children }) => <ul className="ml-5 list-disc space-y-1 text-sm text-[var(--color-text-secondary)]">{children}</ul>,
        ol: ({ children }) => <ol className="ml-5 list-decimal space-y-1 text-sm text-[var(--color-text-secondary)]">{children}</ol>,
        strong: ({ children }) => <strong className="font-semibold text-[var(--color-text-primary)]">{children}</strong>,
      }}
    >
      {text}
    </ReactMarkdown>
  );
}

export default function WorkedExample({ description, code, explanation }: WorkedExampleProps) {
  const [expanded, setExpanded] = useState(false);
  const hasStructuredExample = Boolean(code.trim() || explanation.trim());
  const markdownOnly = !explanation.trim() && /```|\*\*|^\s*[-#]/m.test(code);

  if (!description.trim() && !hasStructuredExample) return null;

  return (
    <div className="overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]">
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
        className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left transition-colors hover:bg-[var(--color-surface-2)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-accent)]"
      >
        <div className="flex min-w-0 items-center gap-2">
          <Eye size={15} className="shrink-0 text-[var(--color-accent)]" />
          <span className="shrink-0 text-sm font-semibold text-[var(--color-accent)]">Worked Example</span>
          {description.trim() && (
            <span className="hidden truncate text-xs text-[var(--color-text-muted)] sm:inline">
              {description}
            </span>
          )}
        </div>
        {expanded
          ? <ChevronUp size={15} className="shrink-0 text-[var(--color-text-muted)]" />
          : <ChevronDown size={15} className="shrink-0 text-[var(--color-text-muted)]" />}
      </button>

      {expanded && (
        <div className="space-y-4 border-t border-[var(--color-border)] px-4 py-4">
          {markdownOnly ? (
            <ExampleMarkdown text={code} />
          ) : (
            <>
              {description.trim() && (
                <p className="text-sm leading-relaxed text-[var(--color-text-secondary)]">{description}</p>
              )}

              {code.trim() && (
                <div className="overflow-hidden rounded-lg border border-[var(--color-border)] bg-[#161413]">
                  <div className="flex items-center gap-2 border-b border-white/10 px-3 py-2">
                    <div className="h-2.5 w-2.5 rounded-full bg-[#ff5f57]" />
                    <div className="h-2.5 w-2.5 rounded-full bg-[#febc2e]" />
                    <div className="h-2.5 w-2.5 rounded-full bg-[#28c840]" />
                    <span className="ml-1 text-xs text-[#a8a29e]">example.py</span>
                  </div>
                  <pre className="overflow-x-auto p-4 font-mono text-sm leading-relaxed text-[#f5f0e8]">
                    <code>{code}</code>
                  </pre>
                </div>
              )}

              {explanation.trim() && (
                <div className="space-y-1">
                  <p className="text-xs font-semibold uppercase text-[var(--color-text-muted)]">How it works</p>
                  <p className="whitespace-pre-line text-sm leading-relaxed text-[var(--color-text-secondary)]">
                    {explanation}
                  </p>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
