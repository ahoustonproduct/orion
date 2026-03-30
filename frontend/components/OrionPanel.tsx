"use client";

import { useEffect, useRef } from "react";
import { Bot, Loader2 } from "lucide-react";

interface OrionPanelProps {
  content: string;
  loading: boolean;
  title?: string;
}

// Simple markdown renderer for Orion's responses
function renderMarkdown(text: string): string {
  return text
    // Code blocks
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Bold
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // Headers
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    // Bullet points
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>(\n|$))+/g, '<ul>$&</ul>')
    // Numbered lists
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // Line breaks to paragraphs (simple)
    .replace(/\n\n/g, '</p><p>')
    // Wrap in paragraph
    .replace(/^([\s\S])/, '<p>$1')
    .replace(/([\s\S])$/, '$1</p>');
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
          <div
            className="orion-prose text-sm leading-relaxed animate-fade-in"
            dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
          />
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
