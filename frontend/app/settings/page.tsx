"use client";

import { useEffect, useState } from "react";
import { getUserKey, setUserKey } from "@/lib/user";
import { Settings, Copy, Check, Smartphone } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";

export default function SettingsPage() {
  const [userKey, setUserKeyState] = useState("");
  const [customKey, setCustomKey] = useState("");
  const [copied, setCopied] = useState(false);
  const [showQR, setShowQR] = useState(false);

  useEffect(() => {
    setUserKeyState(getUserKey());
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText(userKey);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleApplyKey = () => {
    const trimmed = customKey.trim();
    if (!trimmed) return;
    setUserKey(trimmed);
    setUserKeyState(trimmed);
    setCustomKey("");
    alert("Sync key applied! Your progress will now sync to this key. Refresh to load progress from the server.");
  };

  const syncUrl = typeof window !== "undefined"
    ? `${window.location.origin}?key=${userKey}`
    : "";

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-6">
      <div className="flex items-center gap-2">
        <Settings size={18} className="text-[var(--color-accent)]" />
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">Settings</h1>
      </div>

      {/* Sync Key */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-3">
        <div>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">Cross-Device Sync</h2>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Use this key to access your progress on any device. Copy the key or scan the QR code on your iPhone.
            If you ever lose your saved progress (cleared cookies, new browser, etc.), re-enter this key below to
            restore it.
          </p>
        </div>

        {/* Key display */}
        <div className="flex items-center gap-2">
          <code className="flex-1 text-xs text-[var(--color-text-primary)] bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg px-3 py-2 font-mono break-all">
            {userKey}
          </code>
          <button
            onClick={handleCopy}
            className="shrink-0 p-2 bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-all"
          >
            {copied ? <Check size={14} className="text-[var(--color-success)]" /> : <Copy size={14} />}
          </button>
        </div>

        {/* QR Code toggle */}
        <div>
          <button
            onClick={() => setShowQR(!showQR)}
            className="flex items-center gap-2 text-xs text-[var(--color-accent)] hover:opacity-80 transition-colors"
          >
            <Smartphone size={13} />
            {showQR ? "Hide QR Code" : "Show QR Code for iPhone"}
          </button>
          {showQR && syncUrl && (
            <div className="mt-3 flex flex-col items-center gap-2 p-4 bg-white rounded-xl">
              <QRCodeSVG value={syncUrl} size={180} />
              <p className="text-xs text-black/60 text-center">
                Scan with your iPhone camera to open Orion Code with your progress
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Enter a different key */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-3">
        <div>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">Enter Sync Key</h2>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Already have a key from another device? Enter it here to sync your progress. You can also use an
            email or short memorable phrase (anything stable you&apos;ll remember).
          </p>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={customKey}
            onChange={(e) => setCustomKey(e.target.value)}
            placeholder="Paste your sync key or pick a stable phrase..."
            className="flex-1 bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-xs text-[var(--color-text-primary)] font-mono placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-all"
          />
          <button
            onClick={handleApplyKey}
            disabled={!customKey.trim()}
            className="px-4 py-2 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] disabled:opacity-50 text-white rounded-lg text-xs font-medium transition-all"
          >
            Apply
          </button>
        </div>
      </div>

      {/* App info */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-2">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">About Orion Code</h2>
        <div className="space-y-1 text-xs text-[var(--color-text-secondary)]">
          <p>Version: 1.0.0</p>
          <p>AI Tutor: orion-tutor (Ollama — local)</p>
          <p>Built for: MS Business Analytics & AI</p>
          <p>Curriculum covers: 4 modules — Python, Data Analytics, SQL, Machine Learning</p>
        </div>
      </div>
    </div>
  );
}
