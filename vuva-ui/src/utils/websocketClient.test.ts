// Polyfill WebSocket for Node.js/Jest using 'ws' package
if (typeof global.WebSocket === 'undefined') {
  // @ts-ignore
  global.WebSocket = require('ws');
}
// Polyfill WebSocket.OPEN for Node.js/Jest (ws package)

if (typeof global.WebSocket !== 'undefined' && typeof global.WebSocket.OPEN === 'undefined') {
  Object.defineProperty(global.WebSocket, 'OPEN', {
    value: 1,
    writable: false,
    configurable: true,
    enumerable: true,
  });
}

// src/utils/websocketClient.test.ts
// Diverse tests for WebSocketClient utility

import { WebSocketClient } from './websocketClient';

describe('WebSocketClient', () => {
  let server: any;
  const port = 12345;
  const url = `ws://localhost:${port}`;
  let messages: any[] = [];

  beforeAll((done) => {
    // Use ws for a local test server
    const { Server } = require('ws');
    server = new Server({ port }, () => done());
    server.on('connection', (ws: any) => {
      ws.on('message', (msg: string) => { 
        ws.send(msg); // echo
      });
      ws.send(JSON.stringify({ type: 'news', article: { title: 'Test News' } }));
    });
  });

  afterAll((done) => {
    server.close(() => done());
  });

  it('connects and receives messages', (done) => {
    const client = new WebSocketClient({
      url,
      onMessage: (msg) => {
        messages.push(msg);
        if (msg.type === 'news') {
          expect(msg.article.title).toBe('Test News');
          client.close();
          done();
        }
      },
      onError: (e) => done(e),
      reconnect: false,
    });
  });

  it('reconnects on close', (done) => {
    jest.setTimeout(15000);
    let reconnects = 0;
    let wsInstance: any = null;
    const client = new WebSocketClient({
      url,
      onMessage: () => {},
      onOpen: () => {
        reconnects++;
        if (reconnects === 1) {
          // Simulate server-side close to trigger reconnect
          setTimeout(() => {
            if (wsInstance) {
              wsInstance.close();
            }
          }, 50);
        } else if (reconnects === 2) {
          client.close();
          done();
        }
      },
      onClose: () => {},
      reconnect: true,
      reconnectIntervalMs: 100,
      maxReconnectAttempts: 2,
    });
    // Track the current ws instance from the server
    server.on('connection', (ws: any) => {
      wsInstance = ws;
    });
  });

  it('sends and receives echo', (done) => {
    const client = new WebSocketClient({
      url,
      onMessage: (msg) => {
        if (msg.echo) {
          expect(msg.echo).toBe('hello');
          client.close();
          done();
        }
      },
      onOpen: () => {
        client.send({ echo: 'hello' });
      },
      reconnect: false,
    });
  });
});
