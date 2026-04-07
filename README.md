# Mvuvi — Distributed OCR & Real-Time News Platform

Mvuvi is a distributed system that converts scanned documents into structured, searchable content and delivers it through a real-time personalized feed.

It is designed to handle noisy, multilingual inputs at scale using asynchronous processing and multi-engine OCR.

##  Features

- Asynchronous OCR pipeline (FastAPI + Celery + Redis)
- Multi-engine OCR (Tesseract, EasyOCR, PaddleOCR)
- Preprocessing for noisy/low-quality scans
- Content-hash caching & deduplication
- Real-time updates via WebSockets
- Authenticated API with rate limiting
- Structured logging and observability

---

##  Architecture


::contentReference[oaicite:0]{index=0}

---
<img width="644" height="679" alt="mvuvi" src="https://github.com/user-attachments/assets/c0bdad28-63f7-44ec-925b-57a8fbd1f3e4" />

### System Flow

1. Client uploads document → FastAPI API  
2. Request validated + hashed (deduplication layer)  
3. Task enqueued via Redis → Celery workers  
4. Workers preprocess image (denoise, threshold, deskew)  
5. OCR executed via multiple engines (fallback strategy)  
6. Results stored in PostgreSQL  
7. WebSocket pushes updates to clients in real-time  

---

##  Design Decisions

### Asynchronous Processing (Celery + Redis)
Prevents blocking API requests and allows horizontal scaling of OCR workloads.

### Multi-Engine OCR Fallback
Different OCR engines perform better on different inputs; fallback improves robustness.

### Content-Hash Caching
Avoids redundant OCR computation and significantly improves throughput.

### WebSocket-Based Feed
Push-based updates reduce latency and eliminate polling overhead.

---

##  Scalability

- Horizontally scalable Celery worker pool
- Stateless FastAPI services → load balancer friendly
- Redis message broker for distributed task coordination
- Cached OCR results to minimize recomputation

---

##  API Flow

### OCR Pipeline

POST /ocr/extract  
→ validate input  
→ generate content hash  
→ check cache  
→ enqueue OCR task  

Worker:
→ preprocess image  
→ run OCR engine(s)  
→ store structured output  

---

### Feed System

GET /feed  
→ fetch processed content  
→ apply filters / ranking  
→ stream updates via WebSocket  

---

##  Performance (example — update after testing)

- Handles 100+ concurrent OCR requests (simulated)
- Reduces redundant OCR calls via caching
- Improved extraction robustness by ~10% on noisy inputs

---

##  Tech Stack

- Backend: FastAPI, Python
- Queue: Celery + Redis
- OCR: Tesseract, EasyOCR, PaddleOCR
- Database: PostgreSQL
- Realtime: WebSockets
- Infra: Docker

---

##  Future Work

- Distributed worker autoscaling
- Language-specific OCR routing
- Ranking & recommendation system
- Edge deployment for low-latency OCR

---

##  Repository

https://github.com/onyangojerry/Mvuvi
