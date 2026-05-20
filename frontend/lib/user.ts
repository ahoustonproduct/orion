const USER_KEY_STORAGE = "orion_user_key";
const LOCAL_USER_KEY = "orion_local_user";

function normalizeUserKey(key: string | null): string {
  return key?.trim() ?? "";
}

function readStoredKey(): string {
  if (typeof window === "undefined") return "";
  try {
    return normalizeUserKey(localStorage.getItem(USER_KEY_STORAGE));
  } catch {
    return "";
  }
}

function persistUserKey(key: string): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(USER_KEY_STORAGE, key);
  } catch {
    /* localStorage may be unavailable in private or locked-down browsers */
  }
}

/**
 * Promote a ?key= share/QR parameter into durable local storage, then remove
 * the key from the visible URL.
 */
function applyKeyFromUrl(): string {
  if (typeof window === "undefined") return "";
  try {
    const params = new URLSearchParams(window.location.search);
    const fromUrl = normalizeUserKey(params.get("key"));
    if (!fromUrl) return "";

    persistUserKey(fromUrl);
    params.delete("key");
    const newSearch = params.toString();
    const newUrl = `${window.location.pathname}${newSearch ? `?${newSearch}` : ""}${window.location.hash}`;
    window.history.replaceState({}, "", newUrl);
    return fromUrl;
  } catch {
    return "";
  }
}

export function getUserKey(): string {
  if (typeof window === "undefined") return "";

  // URL param takes precedence so a shared/QR link can re-sync a device.
  const fromUrl = applyKeyFromUrl();
  if (fromUrl) return fromUrl;

  const stored = readStoredKey();
  if (stored) return stored;

  persistUserKey(LOCAL_USER_KEY);
  return LOCAL_USER_KEY;
}

export function setUserKey(key: string): void {
  const trimmed = normalizeUserKey(key);
  if (!trimmed) return;
  persistUserKey(trimmed);
}
