import { useEffect, useRef } from "react";
import { getWsUrl } from "./api";
import { useUiStore } from "@/store/uiStore";

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const addLogLine = useUiStore((s) => s.addLogLine);

  useEffect(() => {
    let reconnectTimeout: ReturnType<typeof setTimeout>;

    function connect() {
      const ws = new WebSocket(getWsUrl());
      wsRef.current = ws;

      ws.onmessage = (ev) => {
        addLogLine(ev.data);
      };

      ws.onclose = () => {
        reconnectTimeout = setTimeout(connect, 3000);
      };

      ws.onerror = () => {
        ws.close();
      };
    }

    connect();

    return () => {
      clearTimeout(reconnectTimeout);
      wsRef.current?.close();
    };
  }, [addLogLine]);
}
