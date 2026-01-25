# WebSocket Real-Time News Integration Plan

**Version:** 1.0.0  
**Last Updated:** January 25, 2026


## Overview

This document outlines the architecture, implementation plan, and integration standards for adding a production-grade WebSocket endpoint to the Vuva backend for real-time news delivery to the frontend UI. It includes backend design, security, scalability, and frontend connection strategy, following agile and enterprise best practices.


## 1. Backend WebSocket Implementation (FastAPI)

### 1.1. Endpoint Specification

### 1.2. Core Features

### 1.3. Security & Authentication

### 1.4. Scalability & Robustness

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


## 2. Frontend Integration Plan (React)

### 2.1. Connection Strategy

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


## 3. Agile Implementation Steps

1. **Backend:**
  - [x] Implement `/api/v1/feed/stream` WebSocket endpoint
  - [x] Add JWT authentication and connection management (guests supported)
  - [ ] Integrate with news ingestion pipeline (push new articles)
  - [ ] Add tests for connection, broadcast, and security
  - [x] Document usage and error handling (see below)
### Backend Implementation Progress (2026-01-25)


2. **Frontend:**
   - [ ] Add WebSocket client hook to UI
   - [ ] Replace mock stream with real-time updates
   - [ ] Handle reconnects and errors
   - [ ] Test with backend and document integration

3. **Production Readiness:**
   - [ ] Add monitoring/logging for connections
   - [ ] Plan for scaling (Redis pub/sub if needed)
   - [ ] Security review and penetration testing


## 4. References


**This plan is designed for robust, secure, and scalable real-time news delivery between the Vuva backend and frontend.**
