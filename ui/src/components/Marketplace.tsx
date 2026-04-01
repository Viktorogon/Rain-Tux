import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Download, Package } from "lucide-react";
import { toast } from "sonner";

export default function Marketplace() {
  const { data: items = [], isLoading, error } = useQuery({
    queryKey: ["marketplace"],
    queryFn: api.getMarketplace,
    retry: 1,
  });

  if (isLoading) {
    return <div className="p-4 text-xs text-muted-foreground">Loading marketplace…</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-xs text-destructive">
        Failed to load marketplace feed.
      </div>
    );
  }

  return (
    <div className="p-4">
      <h2 className="mb-3 text-sm font-semibold text-foreground">Marketplace</h2>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <div
            key={item.id}
            className="flex flex-col rounded border bg-card p-3 transition-colors hover:border-primary/40"
          >
            {/* Image placeholder */}
            <div className="mb-2 flex h-24 items-center justify-center rounded bg-muted/30">
              <Package className="h-8 w-8 text-muted-foreground" />
            </div>

            <h3 className="text-xs font-semibold text-foreground">{item.name}</h3>
            <p className="mt-0.5 text-xs text-muted-foreground">{item.author}</p>
            <p className="mt-1 flex-1 text-xs text-muted-foreground leading-relaxed">
              {item.description}
            </p>

            <div className="mt-2 flex items-center justify-between">
              <span className="flex items-center gap-1 text-xs text-muted-foreground">
                <Download className="h-3 w-3" />
                {item.downloads.toLocaleString()}
              </span>
              <button
                onClick={() => toast.info("Install API not yet available")}
                className="rounded bg-primary px-2.5 py-1 text-xs font-medium text-primary-foreground transition-colors hover:bg-primary/80"
              >
                Install
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
