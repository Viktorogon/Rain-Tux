import { create } from "zustand";
import type { TabId } from "@/lib/types";

interface UiState {
  activeTab: TabId;
  setActiveTab: (tab: TabId) => void;
  selectedSkinId: string | null;
  setSelectedSkinId: (id: string | null) => void;
  expandedFolders: Set<string>;
  toggleFolder: (path: string) => void;
  skinOrder: string[];
  setSkinOrder: (order: string[]) => void;
  logLines: string[];
  addLogLine: (line: string) => void;
  clearLog: () => void;
}

const savedOrder = JSON.parse(localStorage.getItem("raintux-skin-order") || "[]");

export const useUiStore = create<UiState>((set) => ({
  activeTab: "manage",
  setActiveTab: (tab) => set({ activeTab: tab }),
  selectedSkinId: null,
  setSelectedSkinId: (id) => set({ selectedSkinId: id }),
  expandedFolders: new Set<string>(),
  toggleFolder: (path) =>
    set((state) => {
      const next = new Set(state.expandedFolders);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return { expandedFolders: next };
    }),
  skinOrder: savedOrder,
  setSkinOrder: (order) => {
    localStorage.setItem("raintux-skin-order", JSON.stringify(order));
    set({ skinOrder: order });
  },
  logLines: [],
  addLogLine: (line) =>
    set((state) => ({ logLines: [...state.logLines.slice(-500), line] })),
  clearLog: () => set({ logLines: [] }),
}));
