import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useUiStore } from "@/store/uiStore";
import SkinTree from "./SkinTree";
import SkinDetails from "./SkinDetails";
import Toolbar from "./Toolbar";
import { toast } from "sonner";

export default function ManageSkins() {
  const queryClient = useQueryClient();
  const { selectedSkinId } = useUiStore();

  const { data: skins = [], isLoading } = useQuery({
    queryKey: ["skins"],
    queryFn: api.getSkins,
    retry: 2,
  });

  const { data: activeSkins = [] } = useQuery({
    queryKey: ["skins-active"],
    queryFn: api.getActiveSkins,
    refetchInterval: 5000,
    retry: 2,
  });

  const activeIds = new Set(activeSkins.map((s) => s.id));

  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["skins"] });
    queryClient.invalidateQueries({ queryKey: ["skins-active"] });
  };

  const loadMutation = useMutation({
    mutationFn: api.loadSkin,
    onSuccess: () => { toast.success("Skin loaded"); invalidate(); },
    onError: (e: Error) => toast.error(e.message),
  });

  const unloadMutation = useMutation({
    mutationFn: api.unloadSkin,
    onSuccess: () => { toast.success("Skin unloaded"); invalidate(); },
    onError: (e: Error) => toast.error(e.message),
  });

  const refreshMutation = useMutation({
    mutationFn: api.refreshSkin,
    onSuccess: () => { toast.success("Skin refreshed"); invalidate(); },
    onError: (e: Error) => toast.error(e.message),
  });

  const isActive = selectedSkinId ? activeIds.has(selectedSkinId) : false;
  const selectedSkin = skins.find((s) => s.id === selectedSkinId) || null;

  return (
    <div className="flex h-full flex-col">
      <Toolbar
        selectedSkinId={selectedSkinId}
        isActive={isActive}
        onLoad={() => selectedSkinId && loadMutation.mutate(selectedSkinId)}
        onUnload={() => selectedSkinId && unloadMutation.mutate(selectedSkinId)}
        onRefresh={() => selectedSkinId && refreshMutation.mutate(selectedSkinId)}
        loading={loadMutation.isPending || unloadMutation.isPending || refreshMutation.isPending}
      />
      <div className="flex flex-1 overflow-hidden">
        <div className="w-[35%] min-w-[200px] overflow-auto border-r">
          {isLoading ? (
            <div className="p-4 text-xs text-muted-foreground">Loading skins…</div>
          ) : (
            <SkinTree skins={skins} activeIds={activeIds} />
          )}
        </div>
        <div className="flex-1 overflow-auto">
          <SkinDetails skin={selectedSkin} isActive={isActive} />
        </div>
      </div>
    </div>
  );
}
