import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useUiStore } from "@/store/uiStore";
import { useWebSocket } from "@/lib/useWebSocket";
import ManageSkins from "./ManageSkins";
import Marketplace from "./Marketplace";
import AboutSettings from "./AboutSettings";
import type { TabId } from "@/lib/types";

const tabs: { id: TabId; label: string }[] = [
  { id: "manage", label: "Manage skins" },
  { id: "marketplace", label: "Marketplace" },
  { id: "about", label: "About & settings" },
];

export default function Layout() {
  useWebSocket();

  const { activeTab, setActiveTab } = useUiStore();

  const { data: status } = useQuery({
    queryKey: ["system-status"],
    queryFn: api.getSystemStatus,
    refetchInterval: 10000,
    retry: 2,
  });

  return (
    <div className="flex h-screen flex-col overflow-hidden">
      {/* Top bar */}
      <header className="flex items-center gap-3 border-b px-4 py-2">
        <h1 className="text-sm font-semibold tracking-wide">
          <span className="text-primary">Rain</span>
          <span className="text-foreground">Tux</span>
        </h1>

        {status && (
          <>
            <span className="rounded bg-secondary px-2 py-0.5 text-xs text-muted-foreground">
              {status.compositor}
            </span>
            <span className="ml-auto rounded bg-secondary px-2 py-0.5 text-xs text-muted-foreground">
              {status.api.host}:{status.api.port}
            </span>
          </>
        )}
        {!status && (
          <span className="ml-auto rounded bg-destructive/20 px-2 py-0.5 text-xs text-destructive">
            disconnected
          </span>
        )}
      </header>

      {/* Tabs */}
      <nav className="flex border-b bg-toolbar">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2 text-xs font-medium transition-colors ${
              activeTab === t.id
                ? "border-b-2 border-primary text-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {/* Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === "manage" && <ManageSkins />}
        {activeTab === "marketplace" && <Marketplace />}
        {activeTab === "about" && <AboutSettings />}
      </main>
    </div>
  );
}
