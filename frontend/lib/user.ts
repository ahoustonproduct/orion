import { v4 as uuidv4 } from "uuid";

const USER_KEY_STORAGE = "orion_user_key";

export function getUserKey(): string {
  if (typeof window === "undefined") return "";
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
