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

### 1. Ingestion API Service [Done] IMPLEMENTED
**Purpose**: Handle newspaper image uploads and initial processing
**Status**: Structure complete, pending database integration

**Endpoints**:
- `POST /api/v1/ingest/upload` [Done] - Upload newspaper image (validation ready)
- `POST /api/v1/ingest/batch` [Done] - Batch upload multiple images
- `GET /api/v1/ingest/status/{id}` [Config] - Check processing status (pending DB)
- `GET /api/v1/ingest/history` [Config] - Get upload history (pending DB)

**Responsibilities**:
- [Done] Image validation (type, size)
- [Done] File upload handling with multipart
- [Urgent] Storage to S3/local (pending)
- [Urgent] Queue jobs for OCR processing (pending)
- [Urgent] Track processing status (pending DB)

### 2. OCR API Service [Done] IMPLEMENTED
**Purpose**: Extract text from newspaper images using multiple OCR engines
**Status**: Fully operational with 3 engines

**Endpoints**:
- `POST /api/v1/ocr/extract` [Done] - Single image OCR
- `POST /api/v1/ocr/extract/compare` [Done] - Compare all 3 engines
- `POST /api/v1/ocr/extract/batch` [Done] - Batch processing
- `GET /api/v1/ocr/engines` [Done] - List available engines

**Engines Available**:
- [Done] Tesseract OCR (fast, reliable)
- [Done] EasyOCR (deep learning, complex layouts)
- [Done] PaddleOCR (mobile-optimized, Asian languages)

**Features**:
- [Done] Lazy-loading for memory efficiency
- [Done] Image preprocessing pipeline
- [Done] Confidence scoring
- [Done] Multi-language support
- [Done] Async processing with executor pool

### 3. News Feed API Service [Config] PARTIALLY IMPLEMENTED
**Purpose**: Deliver personalized news feed using randomization algorithms
**Status**: Endpoint structure ready, logic pending

**Endpoints**:
- `GET /api/v1/feed` [Config] - Get personalized news feed (structure only)
- `GET /api/v1/feed/stream` [Urgent] - WebSocket for real-time updates (not implemented)
- `POST /api/v1/feed/preferences` [Urgent] - Update user preferences (pending)
- `GET /api/v1/feed/article/{id}` [Urgent] - Get specific article (pending DB)

**Responsibilities**:
- [Urgent] Apply randomization algorithms
- [Urgent] Real-time feed delivery
- [Urgent] Content filtering and ranking
- [Urgent] Personalization engine

### 4. Health & Monitoring [Done] IMPLEMENTED
**Purpose**: System health checks and monitoring
**Status**: Operational

**Endpoints**:
- `GET /` [Done] - Root with API information
- `GET /health` [Done] - Health check endpoint
- `GET /api/v1/health` [Done] - Detailed health status
- `GET /docs` [Done] - Interactive API documentation (Swagger UI)
- `GET /redoc` [Done] - ReDoc API documentation

### 5. User Service API [Urgent] NOT IMPLEMENTED
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
User uploads image [Done] → FastAPI Endpoint [Done] → File Validation [Done]
  → Temporary Storage [Done] → OCR Service [Done]
  → Text Extraction [Done] → Return Result [Done]
  
[Pending: S3 Storage [Urgent], Database Logging [Urgent], Queue System [Urgent]]
```

### 2. OCR Processing Flow (Implemented)
```
Image File → ImagePreprocessor [Done]
  → Grayscale + Denoise + Threshold [Done]
  → OCR Engine (Tesseract/EasyOCR/PaddleOCR) [Done]
  → Text Extraction + Confidence Score [Done]
  → Return OCRResult [Done]
```

### 3. Real-time Feed Flow (Not Yet Implemented)
```
User requests feed [Urgent] → API Gateway [Urgent] → Feed Service [Urgent]
  → Randomization Algorithm [Urgent] → Database Query [Urgent]
  → Apply Filters [Urgent] → WebSocket Stream [Urgent] → User Display [Urgent]
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
- **API Startup Time**: ~2 seconds (with lazy-loading) [Done]
- **Health Check Response**: <50ms [Done]
- **OCR Processing**: 
  - Tesseract: 1-3 seconds per image
  - EasyOCR: 3-8 seconds per image (first load + processing)
  - PaddleOCR: 2-5 seconds per image
- **API Response Time**: <100ms for simple endpoints [Done]

### Production Targets (Goals)
- **API Response Time**: <100ms (p95)
- **Upload Processing**: <5 seconds per image
- **Feed Delivery**: <50ms
- **Real-time Updates**: <100ms latency
- **Throughput**: 1000+ requests/second
- **Uptime**: 99.9%
