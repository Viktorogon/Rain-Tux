import type { Skin } from "@/lib/types";
import { Monitor } from "lucide-react";

interface Props {
  skin: Skin | null;
  isActive: boolean;
}

export default function SkinDetails({ skin, isActive }: Props) {
  if (!skin) {
    return (
      <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
        Select a skin to view details
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center gap-2">
        <h2 className="text-sm font-semibold text-foreground">{skin.id}</h2>
        {isActive && (
          <span className="inline-flex items-center gap-1 rounded bg-active/15 px-2 py-0.5 text-xs text-active">
            <span className="h-1.5 w-1.5 rounded-full bg-active" />
            Active
          </span>
        )}
      </div>

      <div className="space-y-2 text-xs">
        <div>
          <span className="text-muted-foreground">Path: </span>
          <span className="font-mono text-foreground">{skin.path}</span>
        </div>
        <div>
          <span className="text-muted-foreground">ID: </span>
          <span className="font-mono text-foreground">{skin.id}</span>
        </div>
      </div>

      {/* Thumbnail placeholder */}
      <div className="flex h-32 w-full items-center justify-center rounded border border-dashed bg-muted/30">
        <div className="flex flex-col items-center gap-1 text-muted-foreground">
          <Monitor className="h-6 w-6" />
          <span className="text-xs">Preview not available</span>
        </div>
      </div>

      <p className="text-xs text-muted-foreground">
        Author and description metadata will appear here when skin parsing is implemented.
      </p>
    </div>
  );
}
