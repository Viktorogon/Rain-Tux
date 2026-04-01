export interface Skin {
  id: string;
  path: string;
}

export interface SkinConfig {
  x?: number;
  y?: number;
  monitor?: number;
  layer?: string;
  transparency?: number;
  snap?: boolean;
  click_through?: boolean;
  keep_on_screen?: boolean;
  load_on_startup?: boolean;
  update_rate?: number;
  [key: string]: unknown;
}

export interface SystemStatus {
  compositor: string;
  skins_loaded: number;
  api: {
    host: string;
    port: number;
  };
}

export interface MarketplaceSkin {
  id: string;
  name: string;
  author: string;
  description: string;
  image: string;
  downloads: number;
  url?: string;
}

export type TabId = "manage" | "marketplace" | "about";

export interface TreeNode {
  name: string;
  path: string;
  isLeaf: boolean;
  children: TreeNode[];
  skinId?: string;
}
