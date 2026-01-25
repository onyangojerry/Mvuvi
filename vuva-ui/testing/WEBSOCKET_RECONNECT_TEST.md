# WebSocket Client Reconnection Test: Node.js/Jest

## Purpose
This document explains the advanced reconnection test for the production WebSocket client in the Vuva frontend, ensuring robust, real-world reconnection logic in a Node.js/Jest environment.

## Why This Test Is Special
- **Simulates Real-World Failures:** Instead of closing the client (which disables reconnect logic), the test simulates a server-side close, mimicking real network/server failures.
- **Polyfills for Node.js:** Uses the `ws` package and polyfills `WebSocket` and `WebSocket.OPEN` for Node.js compatibility.
- **Tracks Server Connections:** The test tracks the current WebSocket server instance to trigger server-side disconnects.
- **Ensures Robustness:** Validates that the client automatically reconnects as expected, matching production browser behavior.

## Test Logic
1. **First Connection:**
   - The client connects to the test server.
   - The test simulates a server-side close (not a client-initiated close) after a short delay.
2. **Reconnection:**
   - The client should automatically reconnect.
   - On the second connection, the test closes the client for cleanup and calls `done()`.

## Key Implementation
- The test uses `server.on('connection', ...)` to track the current server-side WebSocket instance.
- The server-side close is triggered with `wsInstance.close()`.
- The client is only closed by the test after the second connection, ensuring the reconnect logic is exercised.

## Why Not Just Call client.close()?
Calling `client.close()` sets `closedByUser = true`, which disables reconnect logic in the client. Only a server/network close will trigger a true reconnect attempt.

## References
- [websocketClient.test.ts](../src/utils/websocketClient.test.ts)
- [websocketClient.ts](../src/utils/websocketClient.ts)

---
This approach ensures the WebSocket client is robust, production-grade, and ready for real-world network conditions.
