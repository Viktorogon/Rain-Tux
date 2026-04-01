import { useMemo } from "react";
import { useUiStore } from "@/store/uiStore";
import type { Skin, TreeNode } from "@/lib/types";
import { ChevronRight, ChevronDown, FileText } from "lucide-react";

function buildTree(skins: Skin[]): TreeNode[] {
  const root: TreeNode[] = [];

  for (const skin of skins) {
    const parts = skin.id.split("/");
    let current = root;

    for (let i = 0; i < parts.length; i++) {
      const name = parts[i];
      const path = parts.slice(0, i + 1).join("/");
      const isLeaf = i === parts.length - 1;

      let node = current.find((n) => n.name === name && n.path === path);
      if (!node) {
        node = { name, path, isLeaf, children: [], skinId: isLeaf ? skin.id : undefined };
        current.push(node);
      }
      current = node.children;
    }
  }

  return root;
}

interface Props {
  skins: Skin[];
  activeIds: Set<string>;
}

export default function SkinTree({ skins, activeIds }: Props) {
  const tree = useMemo(() => buildTree(skins), [skins]);

  if (skins.length === 0) {
    return (
      <div className="p-4 text-xs text-muted-foreground">
        No skins found. Make sure RainTux is running.
      </div>
    );
  }

  return (
    <div className="py-1">
      {tree.map((node) => (
        <TreeItem key={node.path} node={node} activeIds={activeIds} depth={0} />
      ))}
    </div>
  );
}

function TreeItem({ node, activeIds, depth }: { node: TreeNode; activeIds: Set<string>; depth: number }) {
  const { selectedSkinId, setSelectedSkinId, expandedFolders, toggleFolder } = useUiStore();
  const isExpanded = expandedFolders.has(node.path);
  const isSelected = node.skinId === selectedSkinId;
  const isActive = node.skinId ? activeIds.has(node.skinId) : false;

  if (node.isLeaf) {
    return (
      <button
        onClick={() => setSelectedSkinId(node.skinId || null)}
        className={`flex w-full items-center gap-1.5 py-1 text-left text-xs transition-colors ${
          isSelected ? "bg-primary/20 text-primary" : "text-foreground hover:bg-panel-hover"
        }`}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
      >
        <FileText className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
        <span className="truncate">{node.name}</span>
        {isActive && (
          <span className="ml-auto mr-2 h-2 w-2 shrink-0 rounded-full bg-active animate-pulse-dot" />
        )}
      </button>
    );
  }

  return (
    <div>
      <button
        onClick={() => toggleFolder(node.path)}
        className="flex w-full items-center gap-1 py-1 text-left text-xs text-muted-foreground hover:text-foreground"
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
      >
        {isExpanded ? (
          <ChevronDown className="h-3.5 w-3.5 shrink-0" />
        ) : (
          <ChevronRight className="h-3.5 w-3.5 shrink-0" />
        )}
        <span className="truncate font-medium">{node.name}</span>
      </button>
      {isExpanded &&
        node.children.map((child) => (
          <TreeItem key={child.path} node={child} activeIds={activeIds} depth={depth + 1} />
        ))}
    </div>
  );
}
