"use client";

import { useEffect, useState } from "react";
import { getUserKey, setUserKey } from "@/lib/user";
import { Settings, Copy, Check, RefreshCw, Smartphone } from "lucide-react";
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
    alert("Sync key applied! Your progress will now sync to this key.");
  };

  const syncUrl = typeof window !== "undefined"
    ? `${window.location.origin}?key=${userKey}`
    : "";

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-6">
      <div className="flex items-center gap-2">
        <Settings size={18} className="text-[#a01c2c]" />
        <h1 className="text-xl font-bold text-[#1c1410]">Settings</h1>
      </div>

      {/* Sync Key */}
      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
        <div>
          <h2 className="text-sm font-semibold text-[#1c1410] mb-1">Cross-Device Sync</h2>
          <p className="text-xs text-[#5c4f45]">
            Use this key to access your progress on any device. Copy the key or scan the QR code on your iPhone.
          </p>
        </div>

        {/* Key display */}
        <div className="flex items-center gap-2">
          <code className="flex-1 text-xs text-[#b8822a] bg-[#faf7f3] border border-[#e5ddd4] rounded-lg px-3 py-2 font-mono break-all">
            {userKey}
          </code>
          <button
            onClick={handleCopy}
            className="shrink-0 p-2 bg-[#f5f0ea] border border-[#e5ddd4] rounded-lg text-[#5c4f45] hover:text-[#1c1410] transition-all"
          >
            {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
          </button>
        </div>

        {/* QR Code toggle */}
        <div>
          <button
            onClick={() => setShowQR(!showQR)}
            className="flex items-center gap-2 text-xs text-[#a01c2c] hover:text-[#c97a84] transition-colors"
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
      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
        <div>
          <h2 className="text-sm font-semibold text-[#1c1410] mb-1">Enter Sync Key</h2>
          <p className="text-xs text-[#5c4f45]">
            Already have a key from another device? Enter it here to sync your progress.
          </p>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={customKey}
            onChange={(e) => setCustomKey(e.target.value)}
            placeholder="Paste your sync key..."
            className="flex-1 bg-[#faf7f3] border border-[#e5ddd4] rounded-lg px-3 py-2 text-xs text-[#1c1410] font-mono placeholder-[#9a8c80] outline-none focus:border-[#a01c2c] transition-all"
          />
          <button
            onClick={handleApplyKey}
            disabled={!customKey.trim()}
            className="px-4 py-2 bg-[#a01c2c] hover:bg-[#821624] disabled:opacity-50 text-white rounded-lg text-xs font-medium transition-all"
          >
            Apply
          </button>
        </div>
      </div>

      {/* App info */}
      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-2">
        <h2 className="text-sm font-semibold text-[#1c1410]">About Orion Code</h2>
        <div className="space-y-1 text-xs text-[#5c4f45]">
          <p>Version: 1.0.0</p>
          <p>AI Tutor: Claude claude-sonnet-4-6 (Anthropic)</p>
          <p>Built for: WashU MS Business Analytics — FinTech concentration</p>
          <p>Curriculum covers: 19 modules across 4 levels</p>
        </div>
      </div>
    </div>
  );
}
