import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import LogViewer from "./LogViewer";
import { Info } from "lucide-react";

export default function AboutSettings() {
  const { data: status } = useQuery({
    queryKey: ["system-status"],
    queryFn: api.getSystemStatus,
    retry: 2,
  });

  return (
    <div className="p-4 space-y-4 max-w-xl">
      <h2 className="text-sm font-semibold text-foreground">About & Settings</h2>

      <div className="space-y-2 rounded border bg-card p-3">
        <div className="flex items-center gap-2 text-xs">
          <Info className="h-4 w-4 text-primary" />
          <span className="font-semibold text-foreground">RainTux</span>
        </div>
        <div className="space-y-1 text-xs text-muted-foreground">
          <p>Desktop skin engine for Linux — inspired by Rainmeter.</p>
          {status ? (
            <>
              <p>Compositor: <span className="text-foreground">{status.compositor}</span></p>
              <p>Skins loaded: <span className="text-foreground">{status.skins_loaded}</span></p>
              <p>API: <span className="text-foreground">{status.api.host}:{status.api.port}</span></p>
            </>
          ) : (
            <p className="text-destructive">Backend not reachable</p>
          )}
        </div>
      </div>

      <div className="rounded border bg-card p-3 space-y-2">
        <h3 className="text-xs font-semibold text-foreground">GNOME Extension</h3>
        <p className="text-xs text-muted-foreground">
          GNOME Shell extension integration will be available in a future release.
        </p>
      </div>

      <LogViewer />
    </div>
  );
}
