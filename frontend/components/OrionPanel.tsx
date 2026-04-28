"use client";

import { useEffect, useRef } from "react";
import { Bot, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";

interface OrionPanelProps {
  content: string;
  loading: boolean;
  title?: string;
}

export default function OrionPanel({ content, loading, title = "Orion" }: OrionPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [content]);

  return (
    <div className="flex flex-col h-full bg-surface rounded-xl border border-border overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-surface-2">
        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-accent to-cyan-DEFAULT flex items-center justify-center">
          <Bot size={14} className="text-white" />
        </div>
        <span className="text-sm font-semibold text-text-primary">{title}</span>
        {loading && <Loader2 size={14} className="text-accent animate-spin ml-auto" />}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {loading && !content && (
          <div className="flex flex-col gap-2 animate-pulse">
            <div className="h-3 bg-surface-2 rounded w-3/4" />
            <div className="h-3 bg-surface-2 rounded w-full" />
            <div className="h-3 bg-surface-2 rounded w-5/6" />
            <div className="h-3 bg-surface-2 rounded w-2/3" />
          </div>
        )}
        {content && (
          <div className="orion-prose text-sm leading-relaxed animate-fade-in">
            <ReactMarkdown
              rehypePlugins={[rehypeSanitize]}
              components={{
                code: ({ className, children }) => {
                  const isBlock = className?.includes("block") || String(children).includes("\n");
                  return isBlock ? (
                    <pre className="bg-surface-2 border border-border rounded-lg p-3 my-2 overflow-x-auto">
                      <code className={className}>{children}</code>
                    </pre>
                  ) : (
                    <code className="bg-surface-2 border border-border rounded px-1.5 py-0.5 text-sm">
                      {children}
                    </code>
                  );
                },
                p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
                ul: ({ children }) => <ul className="list-disc ml-6 mb-3 space-y-1">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal ml-6 mb-3 space-y-1">{children}</ol>,
                strong: ({ children }) => <strong className="font-semibold text-text-primary">{children}</strong>,
                h2: ({ children }) => <h2 className="text-lg font-bold text-text-primary mt-4 mb-2">{children}</h2>,
                h3: ({ children }) => <h3 className="text-md font-bold text-text-primary mt-4 mb-2">{children}</h3>,
                li: ({ children }) => <li>{children}</li>,
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
