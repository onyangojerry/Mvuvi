# WebSocket Real-Time News Integration Plan

**Version:** 1.0.0  
**Last Updated:** January 25, 2026

---

## Overview

This document outlines the architecture, implementation plan, and integration standards for adding a production-grade WebSocket endpoint to the Vuva backend for real-time news delivery to the frontend UI. It includes backend design, security, scalability, and frontend connection strategy, following agile and enterprise best practices.

---

## 1. Backend WebSocket Implementation (FastAPI)

### 1.1. Endpoint Specification
- **Path:** `/api/v1/feed/stream`
- **Protocol:** WebSocket (ws/wss)
- **Purpose:** Broadcast new news articles and feed updates to all connected clients in real time.

### 1.2. Core Features
- Broadcast new articles as soon as they are ingested/processed
- Support for multiple concurrent clients
- Personalized feed for registered (authenticated) users
- Randomized/generic feed for non-registered (unauthenticated) users
- Optional: Filtered streams (by category, user, etc.)
- Heartbeat/ping for connection health
- Graceful disconnect and reconnect support
- Production-ready error handling and logging

### 1.3. Security & Authentication
- If JWT token is provided on connection (query param or header), validate token and user permissions before accepting connection
- If authenticated, stream a personalized feed based on user preferences/history
- If not authenticated, stream a randomized/generic feed
- Enforce rate limits and connection limits per user/IP
- Sanitize all outgoing data

### 1.4. Scalability & Robustness
- Use FastAPI's `WebSocket` and `WebSocketDisconnect`
- Maintain a set of active connections (in-memory or Redis pub/sub for scale-out)
- Handle client disconnects and errors gracefully
- Support horizontal scaling (future: Redis pub/sub or message broker)

### 1.5. Example FastAPI WebSocket Handler
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi_jwt_auth import AuthJWT
from typing import List

router = APIRouter()

active_connections: List[WebSocket] = []

def get_current_user(websocket: WebSocket, Authorize: AuthJWT = Depends()):
    token = websocket.query_params.get('token')
    if not token:
        raise Exception('Missing token')
    Authorize.jwt_required(token=token)
    return Authorize.get_jwt_subject()

@router.websocket('/api/v1/feed/stream')
async def feed_stream(websocket: WebSocket):
    await websocket.accept()
    try:
      user = None
      try:
        user = get_current_user(websocket)
      except Exception:
        pass  # Not authenticated
      active_connections.append(websocket)
      while True:
        if user:
          # Personalized feed for authenticated user
          data = await get_next_personalized_article(user)
        else:
          # Randomized/generic feed for guest
          data = await get_next_random_article()
        await websocket.send_json(data)
    except WebSocketDisconnect:
      active_connections.remove(websocket)
    except Exception as e:
      await websocket.close()
```

---

## 2. Frontend Integration Plan (React)

### 2.1. Connection Strategy
- Use native `WebSocket` or a library (e.g., `reconnecting-websocket`)
- If user is logged in, connect to `ws://<backend>/api/v1/feed/stream?token=<JWT>` to receive a personalized feed
- If user is not logged in, connect to `ws://<backend>/api/v1/feed/stream` (no token) to receive a randomized/generic feed
- On message, parse and update Zustand store/news feed
- Handle reconnects, errors, and connection drops
- Show connection status in UI (optional)

### 2.2. Example React Hook
```js
import { useEffect } from 'react';

export function useNewsWebSocket(token, onMessage) {
  useEffect(() => {
    const url = token
      ? `ws://localhost:8000/api/v1/feed/stream?token=${token}`
      : `ws://localhost:8000/api/v1/feed/stream`;
    const ws = new WebSocket(url);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
    ws.onerror = () => {/* handle error */};
    ws.onclose = () => {/* handle close/reconnect */};
    return () => ws.close();
  }, [token, onMessage]);
}
```

---

## 3. Agile Implementation Steps

1. **Backend:**
  - [x] Implement `/api/v1/feed/stream` WebSocket endpoint
  - [x] Add JWT authentication and connection management (guests supported)
  - [ ] Integrate with news ingestion pipeline (push new articles)
  - [ ] Add tests for connection, broadcast, and security
  - [x] Document usage and error handling (see below)
---
### Backend Implementation Progress (2026-01-25)

- WebSocket endpoint `/api/v1/feed/stream` created in `src/api/v1/feed.py`.
- JWT authentication is supported (token via query param), with guest fallback.
- Connection management and robust error handling implemented.
- Logging for connect/disconnect/error events added.
- Next: Integrate real news ingestion, add rate limiting, and write tests.

2. **Frontend:**
   - [ ] Add WebSocket client hook to UI
   - [ ] Replace mock stream with real-time updates
   - [ ] Handle reconnects and errors
   - [ ] Test with backend and document integration

3. **Production Readiness:**
   - [ ] Add monitoring/logging for connections
   - [ ] Plan for scaling (Redis pub/sub if needed)
   - [ ] Security review and penetration testing

---

## 4. References
- [FastAPI WebSocket Docs](https://fastapi.tiangolo.com/advanced/websockets/)
- [OWASP WebSocket Security](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

**This plan is designed for robust, secure, and scalable real-time news delivery between the Vuva backend and frontend.**
