"use client";

import { useState, useRef } from "react";
import dynamic from "next/dynamic";
import { X, Plus, File, FileCode, FileText } from "lucide-react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export interface FileTab {
  id: string;
  name: string;
  content: string;
  language: "python" | "sql" | "text";
}

interface MultiFileEditorProps {
  files: FileTab[];
  onFilesChange: (files: FileTab[]) => void;
  onExecute?: () => void;
}

export default function MultiFileEditor({
  files,
  onFilesChange,
}: MultiFileEditorProps) {
  const [activeFileId, setActiveFileId] = useState(files[0]?.id || "");
  const editorRef = useRef<any>(null);

  const activeFile = files.find((f) => f.id === activeFileId) || files[0];

  const addNewFile = () => {
    const newId = `file-${Date.now()}`;
    const newFile: FileTab = {
      id: newId,
      name: `script${files.length + 1}.py`,
      content: "# New Python file\n",
      language: "python",
    };
    onFilesChange([...files, newFile]);
    setActiveFileId(newId);
  };

  const updateActiveFileContent = (content: string) => {
    onFilesChange(
      files.map((f) => (f.id === activeFileId ? { ...f, content } : f))
    );
  };

  const closeFile = (fileId: string) => {
    if (files.length <= 1) return;
    const newFiles = files.filter((f) => f.id !== fileId);
    onFilesChange(newFiles);
    if (activeFileId === fileId) {
      setActiveFileId(newFiles[0].id);
    }
  };

  const getFileIcon = (name: string) => {
    if (name.endsWith(".py")) return <FileCode size={14} className="text-[var(--color-success)]" />;
    if (name.endsWith(".sql")) return <FileText size={14} className="text-[var(--color-accent)]" />;
    return <File size={14} className="text-[var(--color-text-muted)]" />;
  };

  return (
    <div className="flex flex-col h-full border border-[var(--color-border)] rounded-xl overflow-hidden bg-[var(--color-background)]">
      {/* Tab bar */}
      <div className="flex items-center bg-[var(--color-surface)] border-b border-[var(--color-border)] overflow-x-auto">
        {files.map((file) => (
          <div
            key={file.id}
            className={`flex items-center gap-2 px-3 py-2 border-r border-[var(--color-border)] cursor-pointer transition-colors group ${
              file.id === activeFileId
                ? "bg-[var(--color-surface-2)] text-[var(--color-text-primary)]"
                : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-2)]"
            }`}
            onClick={() => setActiveFileId(file.id)}
          >
            {getFileIcon(file.name)}
            <span className="text-sm font-medium whitespace-nowrap">{file.name}</span>
            {files.length > 1 && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  closeFile(file.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-0.5 hover:bg-[var(--color-border)] rounded transition-all"
              >
                <X size={12} />
              </button>
            )}
          </div>
        ))}
        <button
          onClick={addNewFile}
          className="flex items-center gap-1 px-3 py-2 text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-2)] transition-colors"
        >
          <Plus size={14} />
          <span className="text-xs">New File</span>
        </button>
      </div>

      {/* Editor */}
      <div className="flex-1 min-h-[300px]">
        {activeFile && (
          <MonacoEditor
            value={activeFile.content}
            language={activeFile.language}
            theme="vs-dark"
            onChange={(value) => updateActiveFileContent(value || "")}
            onMount={(editor) => {
              editorRef.current = editor;
            }}
            options={{
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              fontSize: 13,
              lineNumbers: "on",
              padding: { top: 12, bottom: 12 },
              automaticLayout: true,
              tabSize: 4,
              wordWrap: "on",
            }}
          />
        )}
      </div>
    </div>
  );
}