const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:7272";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json();
}

function encodeSkinPath(skinPath: string): string {
  return skinPath
    .split("/")
    .map((seg) => encodeURIComponent(seg))
    .join("/");
}

import type { Skin, SkinConfig, SystemStatus, MarketplaceSkin } from "./types";

export const api = {
  getSkins: () => apiFetch<Skin[]>("/skins"),

  getActiveSkins: () => apiFetch<Skin[]>("/skins/active"),

  loadSkin: (skinPath: string) =>
    apiFetch<unknown>(`/skins/${encodeSkinPath(skinPath)}/load`, { method: "POST" }),

  unloadSkin: (skinPath: string) =>
    apiFetch<unknown>(`/skins/${encodeSkinPath(skinPath)}/unload`, { method: "POST" }),

  refreshSkin: (skinPath: string) =>
    apiFetch<unknown>(`/skins/${encodeSkinPath(skinPath)}/refresh`, { method: "POST" }),

  getSkinConfig: (skinPath: string) =>
    apiFetch<SkinConfig>(`/skins/${encodeSkinPath(skinPath)}/config`),

  updateSkinConfig: (skinPath: string, config: Partial<SkinConfig>) =>
    apiFetch<unknown>(`/skins/${encodeSkinPath(skinPath)}/config`, {
      method: "PUT",
      body: JSON.stringify(config),
    }),

  getSystemStatus: () => apiFetch<SystemStatus>("/system/status"),

  getMarketplace: async (): Promise<MarketplaceSkin[]> => {
    const url = import.meta.env.VITE_MARKETPLACE_URL || "/marketplace.example.json";
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch marketplace");
    return res.json();
  },
};

export function getWsUrl(): string {
  try {
    const url = new URL(BASE_URL);
    const protocol = url.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${url.host}/ws`;
  } catch {
    return "ws://127.0.0.1:7272/ws";
  }
}
