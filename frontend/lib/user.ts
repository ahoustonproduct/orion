import { v4 as uuidv4 } from "uuid";

const USER_KEY_STORAGE = "orion_user_key";

/**
 * Read any ?key= param from the current URL and, if present, promote it
 * to the stored user key. This makes QR/share links that end in ?key=<X>
 * automatically sync that user's progress on whichever device opened them.
 * Safe to call on every page load — it's idempotent.
 */
function applyKeyFromUrl(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const params = new URLSearchParams(window.location.search);
    const fromUrl = params.get("key");
    if (fromUrl && fromUrl.trim()) {
      const trimmed = fromUrl.trim();
      localStorage.setItem(USER_KEY_STORAGE, trimmed);
      // Strip the key from the URL so it's not left on screen or in history.
      params.delete("key");
      const newSearch = params.toString();
      const newUrl = window.location.pathname + (newSearch ? `?${newSearch}` : "") + window.location.hash;
      window.history.replaceState({}, "", newUrl);
      return trimmed;
    }
  } catch {
    /* ignore URL parse errors */
  }
  return null;
}

export function getUserKey(): string {
  if (typeof window === "undefined") return "";
  // URL param takes precedence — lets a shared/QR link re-sync a device.
  const fromUrl = applyKeyFromUrl();
  if (fromUrl) return fromUrl;

  let key = localStorage.getItem(USER_KEY_STORAGE);
  if (!key) {
    key = uuidv4();
    localStorage.setItem(USER_KEY_STORAGE, key);
  }
  return key;
}

export function setUserKey(key: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(USER_KEY_STORAGE, key);
}
