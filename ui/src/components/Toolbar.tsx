import { Play, Square, RefreshCw, ExternalLink } from "lucide-react";

interface Props {
  selectedSkinId: string | null;
  isActive: boolean;
  onLoad: () => void;
  onUnload: () => void;
  onRefresh: () => void;
  loading: boolean;
}

export default function Toolbar({ selectedSkinId, isActive, onLoad, onUnload, onRefresh, loading }: Props) {
  const disabled = !selectedSkinId || loading;

  return (
    <div className="flex items-center gap-1 border-b bg-toolbar px-2 py-1.5">
      <ToolbarButton
        icon={<Play className="h-3.5 w-3.5" />}
        label="Load"
        onClick={onLoad}
        disabled={disabled || isActive}
      />
      <ToolbarButton
        icon={<Square className="h-3.5 w-3.5" />}
        label="Unload"
        onClick={onUnload}
        disabled={disabled || !isActive}
      />
      <ToolbarButton
        icon={<RefreshCw className="h-3.5 w-3.5" />}
        label="Refresh"
        onClick={onRefresh}
        disabled={disabled || !isActive}
      />
      <div className="mx-1 h-4 w-px bg-border" />
      <ToolbarButton
        icon={<ExternalLink className="h-3.5 w-3.5" />}
        label="Open in editor"
        onClick={() => {
          if (selectedSkinId) {
            navigator.clipboard.writeText(selectedSkinId);
            // TODO: xdg-open when running natively
          }
        }}
        disabled={!selectedSkinId}
      />

      {loading && (
        <span className="ml-2 text-xs text-muted-foreground animate-pulse">Working…</span>
      )}
    </div>
  );
}

function ToolbarButton({
  icon,
  label,
  onClick,
  disabled,
}: {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
  disabled: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      title={label}
      className="flex items-center gap-1 rounded px-2 py-1 text-xs text-foreground transition-colors hover:bg-panel-hover disabled:opacity-40 disabled:cursor-not-allowed"
    >
      {icon}
      <span className="hidden sm:inline">{label}</span>
    </button>
  );
}
