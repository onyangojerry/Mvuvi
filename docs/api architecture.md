# API Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                        │
│  (Web App, Mobile App, Third-party Integrations)        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  API Gateway                            │
│  (Load Balancer, Rate Limiting, Authentication)         │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌▼──────────────┐
│ Ingestion    │ │News Feed  │ │User Service   │
│ API Service  │ │API Service│ │API Service    │
└───────┬──────┘ └──┬────────┘ └┬──────────────┘
        │           │            │
        │           │            │
┌───────▼───────────▼────────────▼───────────────┐
│         Processing Layer                        │
│  ┌─────────────┐  ┌──────────────────┐         │
│  │OCR Engine   │  │Neural Network    │         │
│  │             │  │Error Correction  │         │
│  └─────────────┘  └──────────────────┘         │
│  ┌─────────────┐  ┌──────────────────┐         │
│  │Randomization│  │Agentic Systems   │         │
│  │Algorithms   │  │                  │         │
│  └─────────────┘  └──────────────────┘         │
└────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│              Data Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │PostgreSQL│  │Redis     │  │S3 Storage│      │
│  │          │  │Cache     │  │(Images)  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
```

## Core Services

### 1. Ingestion API Service ✅ IMPLEMENTED
**Purpose**: Handle newspaper image uploads and initial processing
**Status**: Structure complete, pending database integration

**Endpoints**:
- `POST /api/v1/ingest/upload` ✅ - Upload newspaper image (validation ready)
- `POST /api/v1/ingest/batch` ✅ - Batch upload multiple images
- `GET /api/v1/ingest/status/{id}` ⚙️ - Check processing status (pending DB)
- `GET /api/v1/ingest/history` ⚙️ - Get upload history (pending DB)

**Responsibilities**:
- ✅ Image validation (type, size)
- ✅ File upload handling with multipart
- 🔴 Storage to S3/local (pending)
- 🔴 Queue jobs for OCR processing (pending)
- 🔴 Track processing status (pending DB)

### 2. OCR API Service ✅ IMPLEMENTED
**Purpose**: Extract text from newspaper images using multiple OCR engines
**Status**: Fully operational with 3 engines

**Endpoints**:
- `POST /api/v1/ocr/extract` ✅ - Single image OCR
- `POST /api/v1/ocr/extract/compare` ✅ - Compare all 3 engines
- `POST /api/v1/ocr/extract/batch` ✅ - Batch processing
- `GET /api/v1/ocr/engines` ✅ - List available engines

**Engines Available**:
- ✅ Tesseract OCR (fast, reliable)
- ✅ EasyOCR (deep learning, complex layouts)
- ✅ PaddleOCR (mobile-optimized, Asian languages)

**Features**:
- ✅ Lazy-loading for memory efficiency
- ✅ Image preprocessing pipeline
- ✅ Confidence scoring
- ✅ Multi-language support
- ✅ Async processing with executor pool

### 3. News Feed API Service ⚙️ PARTIALLY IMPLEMENTED
**Purpose**: Deliver personalized news feed using randomization algorithms
**Status**: Endpoint structure ready, logic pending

**Endpoints**:
- `GET /api/v1/feed` ⚙️ - Get personalized news feed (structure only)
- `GET /api/v1/feed/stream` 🔴 - WebSocket for real-time updates (not implemented)
- `POST /api/v1/feed/preferences` 🔴 - Update user preferences (pending)
- `GET /api/v1/feed/article/{id}` 🔴 - Get specific article (pending DB)

**Responsibilities**:
- 🔴 Apply randomization algorithms
- 🔴 Real-time feed delivery
- 🔴 Content filtering and ranking
- 🔴 Personalization engine

### 4. Health & Monitoring ✅ IMPLEMENTED
**Purpose**: System health checks and monitoring
**Status**: Operational

**Endpoints**:
- `GET /` ✅ - Root with API information
- `GET /health` ✅ - Health check endpoint
- `GET /api/v1/health` ✅ - Detailed health status
- `GET /docs` ✅ - Interactive API documentation (Swagger UI)
- `GET /redoc` ✅ - ReDoc API documentation

### 5. User Service API 🔴 NOT IMPLEMENTED
**Purpose**: Manage user accounts and preferences
**Status**: Planned, not started

**Planned Endpoints**:
- `POST /api/v1/users/register` - User registration
- `POST /api/v1/users/login` - Authentication
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/preferences` - Update preferences

## Processing Components

### OCR Engine
- **Technology**: Tesseract OCR / Google Cloud Vision API
- **Input**: Raw newspaper images
- **Output**: Extracted text with confidence scores
- **Performance**: <2 seconds per page

### Neural Network Error Correction
- **Framework**: PyTorch with ONNX runtime
- **Model**: Transformer-based sequence correction
- **Purpose**: Fix OCR errors and improve accuracy
- **Target Accuracy**: 99%+

### Randomization Algorithms
- **Novel Approach**: Weighted randomization with diversity constraints
- **Factors**: 
  - User preferences
  - Content freshness
  - Topic diversity
  - Reading history
- **Algorithm**: Custom hybrid of collaborative filtering + controlled randomness

### Agentic Systems
- **Framework**: LangChain / AutoGen
- **Purpose**: Intelligent content processing and categorization
- **Tasks**:
  - Content summarization
  - Entity extraction
  - Topic classification
  - Quality assessment

## Data Flow

### 1. Image Upload Flow (Current Implementation)
```
User uploads image ✅ → FastAPI Endpoint ✅ → File Validation ✅
  → Temporary Storage ✅ → OCR Service ✅
  → Text Extraction ✅ → Return Result ✅
  
[Pending: S3 Storage 🔴, Database Logging 🔴, Queue System 🔴]
```

### 2. OCR Processing Flow (Implemented)
```
Image File → ImagePreprocessor ✅
  → Grayscale + Denoise + Threshold ✅
  → OCR Engine (Tesseract/EasyOCR/PaddleOCR) ✅
  → Text Extraction + Confidence Score ✅
  → Return OCRResult ✅
```

### 3. Real-time Feed Flow (Not Yet Implemented)
```
User requests feed 🔴 → API Gateway 🔴 → Feed Service 🔴
  → Randomization Algorithm 🔴 → Database Query 🔴
  → Apply Filters 🔴 → WebSocket Stream 🔴 → User Display 🔴
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python) / Express.js (Node.js)
- **API Standards**: RESTful + GraphQL
- **Real-time**: WebSockets / Server-Sent Events

### AI/ML
- **OCR**: Tesseract, EasyOCR, PaddleOCR
- **Neural Networks**: PyTorch, ONNX
- **Agentic**: LangChain, Semantic Kernel

### Database
- **Primary**: PostgreSQL (structured data)
- **Cache**: Redis (sessions, real-time)
- **Storage**: S3-compatible (images)

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

## API Design Principles

### Lightweight & Efficient
- Minimal payload sizes
- Efficient serialization (Protocol Buffers optional)
- Connection pooling
- Request batching where applicable

### Scalability
- Stateless services
- Horizontal scaling capability
- Load balancing
- Async processing for heavy tasks

### Security
- JWT authentication
- API rate limiting
- Input validation
- HTTPS only
- CORS configuration

## Performance Targets

### Current Metrics (Development)
- **API Startup Time**: ~2 seconds (with lazy-loading) ✅
- **Health Check Response**: <50ms ✅
- **OCR Processing**: 
  - Tesseract: 1-3 seconds per image
  - EasyOCR: 3-8 seconds per image (first load + processing)
  - PaddleOCR: 2-5 seconds per image
- **API Response Time**: <100ms for simple endpoints ✅

### Production Targets (Goals)
- **API Response Time**: <100ms (p95)
- **Upload Processing**: <5 seconds per image
- **Feed Delivery**: <50ms
- **Real-time Updates**: <100ms latency
- **Throughput**: 1000+ requests/second
- **Uptime**: 99.9%
