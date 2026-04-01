import { useRef, useEffect } from "react";
import { useUiStore } from "@/store/uiStore";
import { Trash2 } from "lucide-react";

export default function LogViewer() {
  const { logLines, clearLog } = useUiStore();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logLines.length]);

  return (
    <div className="flex flex-col rounded border bg-muted/20">
      <div className="flex items-center justify-between border-b px-3 py-1.5">
        <span className="text-xs font-medium text-muted-foreground">Log</span>
        <button
          onClick={clearLog}
          title="Clear log"
          className="text-muted-foreground transition-colors hover:text-foreground"
        >
          <Trash2 className="h-3.5 w-3.5" />
        </button>
      </div>
      <div className="h-40 overflow-auto p-2 font-mono text-xs leading-relaxed text-foreground">
        {logLines.length === 0 && (
          <span className="text-muted-foreground">Waiting for log output…</span>
        )}
        {logLines.map((line, i) => (
          <div key={i} className="whitespace-pre-wrap break-all">
            {line}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
