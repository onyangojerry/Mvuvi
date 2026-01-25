// src/utils/websocketClient.ts
// Production-ready, secure, reconnecting WebSocket client for Vuva

// Polyfill WebSocket for Node.js/Jest using 'ws' package
// This ensures the client works in both browser and Node.js test environments
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const _WebSocket: any = (typeof global !== 'undefined' && (global as any).WebSocket)
  ? (global as any).WebSocket
  : (typeof window !== 'undefined' && (window as any).WebSocket)
    ? (window as any).WebSocket
    : (() => { try { return require('ws'); } catch { return undefined; } })();

export type WebSocketMessage = {
  type: string;
  [key: string]: any;
};

export interface WebSocketClientOptions {
  url: string;
  token?: string;
  onMessage: (msg: WebSocketMessage) => void;
  onError?: (err: Event) => void;
  onOpen?: () => void;
  onClose?: (ev: CloseEvent) => void;
  reconnect?: boolean;
  reconnectIntervalMs?: number;
  maxReconnectAttempts?: number;
}

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private options: WebSocketClientOptions;
  private reconnectAttempts = 0;
  private closedByUser = false;

  constructor(options: WebSocketClientOptions) {
    this.options = options;
    this.connect();
  }

  private connect() {
    const { url, token } = this.options;
    let wsUrl = url;
    if (token) {
      wsUrl += (url.includes('?') ? '&' : '?') + `token=${encodeURIComponent(token)}`;
    }
    if (!_WebSocket) {
      throw new Error('WebSocket is not available in this environment.');
    }
    this.ws = new _WebSocket(wsUrl);

    this.ws!.onopen = () => {
      this.reconnectAttempts = 0;
      this.options.onOpen?.();
    };
    this.ws!.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.options.onMessage(data);
      } catch (e) {
        // Optionally log parse error
      }
    };
    this.ws!.onerror = (event) => {
      this.options.onError?.(event);
    };
    this.ws!.onclose = (event) => {
      this.options.onClose?.(event);
      if (!this.closedByUser && this.options.reconnect !== false) {
        this.tryReconnect();
      }
    };
  }

  private tryReconnect() {
    if (
      this.options.maxReconnectAttempts &&
      this.reconnectAttempts >= this.options.maxReconnectAttempts
    ) {
      return;
    }
    this.reconnectAttempts++;
    setTimeout(() => {
      this.connect();
    }, this.options.reconnectIntervalMs || 2000);
  }

  public close() {
    this.closedByUser = true;
    this.ws?.close();
  }

  public send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}
