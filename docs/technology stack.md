# Technology Stack

## Overview
Comprehensive technology choices for the Newspaper Ingestion API system, prioritizing lightweight, efficient, and scalable solutions.

## Backend Stack

### API Framework [Done] IMPLEMENTED
**Chosen**: **FastAPI 0.109.0** (Python)
- **Status**: [Done] Fully operational
- **Features Implemented**: 
  - [Done] Async/await pattern throughout
  - [Done] Automatic OpenAPI documentation at /docs
  - [Done] Pydantic 2.5.3 for validation
  - [Done] CORS and GZip middleware
  - [Done] Global exception handling
  - [Done] Lifespan management
- **Server**: Uvicorn 0.27.0 with hot-reload

### Programming Languages
- **Python 3.9+**: [Done] Main backend (current implementation)
- **JavaScript/TypeScript**: [Urgent] Not yet used (planned for frontend)
- **Go**: [Urgent] Not planned currently

### API Standards
- **REST**: Primary API pattern
- **GraphQL**: Optional for complex queries
- **WebSockets**: Real-time feed delivery
- **gRPC**: Internal service communication (optional)

## Frontend Stack

### Framework
**Choice**: **Next.js** (React)
- Server-side rendering
- Excellent performance
- Built-in API routes
- Easy deployment

### UI Library
- **React 18+**: Component library
- **Tailwind CSS**: Styling
- **shadcn/ui**: Component primitives

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state management
- **WebSocket**: Real-time updates

### Real-time Display
- **WebSocket API**: Primary protocol
- **Server-Sent Events**: Fallback
- **React Spring**: Smooth animations

## AI/ML Stack

### OCR Engines [Done] IMPLEMENTED
**Multi-engine Approach**: All three engines integrated with lazy-loading

1. **Tesseract OCR** (Primary) [Done]
   - **Version**: pytesseract 0.3.10, tesseract 5.5.2
   - **Status**: [Done] Fully operational
   - **Features**: Command-line interface, fast processing
   - **Best for**: Standard newspaper text, speed-critical applications
   - **Lazy-loaded**: No (lightweight CLI tool)
   - **NEW: Fast transcription endpoint using Tesseract (~100-300ms)**

2. **EasyOCR** (Secondary) [Done]
   - **Version**: 1.7.1 (with PyTorch 2.8.0)
   - **Status**: [Done] Fully operational with lazy-loading
   - **Features**: Deep learning, 80+ languages
   - **Best for**: Complex layouts, low-quality scans
   - **Lazy-loaded**: Yes (deferred torch import)

3. **PaddleOCR** (Fallback) [Done]
   - **Version**: 2.7.3 (with PaddlePaddle 2.6.0)
   - **Status**: [Done] Fully operational with lazy-loading
   - **Features**: Fast inference, mobile-optimized
   - **Best for**: Asian languages, batch processing
   - **Lazy-loaded**: Yes (deferred import)

**Image Preprocessing Pipeline** [Done]:
- Grayscale conversion
- Gaussian blur noise reduction
- Adaptive threshold
- OpenCV 4.9.0 (headless)

**NEW: Fast Transcription** [Done]:
- Dedicated `/transcribe-fast` endpoint
- Optimized for real-time applications
- Skips preprocessing for speed
- Returns minimal JSON response
- Target: 100-300ms response time

### News Aggregation [Done] NEW
**Free News Sources Integrated**:

1. **RSS Feeds** [Done]
   - **Library**: feedparser 6.0.12
   - **Status**: [Done] Fully operational
   - **Sources**: 15+ free RSS feeds
   - **Categories**: Technology, World, Business, Science, General
   - **Features**: Async fetching, connection pooling

2. **Hacker News** [Done]
   - **Library**: requests + custom client
   - **Status**: [Done] Fully operational
   - **Features**: Top stories API integration
   - **Data**: Title, URL, score, comments

3. **Article Extraction** [Done]
   - **Library**: newspaper3k 0.2.8
   - **Status**: [Done] Fully operational
   - **Features**: Full article text extraction, author, publish date
   - **Dependencies**: beautifulsoup4 4.14.3, lxml 6.0.2, nltk 3.9.2

4. **Date Parsing** [Done]
   - **Library**: python-dateutil
   - **Status**: [Done] Fully operational
   - **Features**: Flexible date parsing for various formats

### Neural Network Framework
**PyTorch** (Primary)
- Flexible and pythonic
- Strong research community
- Easy debugging
- ONNX export support

**Inference**: ONNX Runtime
- Optimized for production
- Cross-platform
- Hardware acceleration
- Low memory footprint

### Agentic Systems
**Primary Framework**: **LangChain**
- Rich ecosystem
- LLM integrations
- Agent templates
- Vector store support

**LLM Options**:
- **GPT-4/GPT-4o**: High quality (API)
- **Claude 3.5**: Good for analysis (API)
- **Llama 3**: Open source, self-hosted
- **Mistral**: Efficient, open source

### Model Deployment
- **ONNX Runtime**: Fast inference
- **TorchServe**: Model serving
- **BentoML**: ML model serving platform

## Data Layer

### Primary Database [Config] CONFIGURED
**PostgreSQL 15+** (Not yet installed)
- **Driver**: asyncpg 0.29.0 [Done]
- **ORM**: SQLAlchemy 2.0.25 [Done]
- **Migrations**: Alembic 1.13.1 [Done]
- **Connection String**: `postgresql+asyncpg://postgres:password@localhost:5432/newspaper_db`
- **Status**: [Config] Configured but database not created
- **Planned Schema**: 
  - Users and authentication
  - News articles and metadata
  - Processing status and logs
  - Analytics and metrics

**Planned Extensions**:
- `pg_vector`: Vector similarity search
- `pg_trgm`: Full-text search
- `uuid-ossp`: UUID generation

### Cache Layer [Config] CONFIGURED
**Redis 7+** (Not yet installed)
- **Client**: redis 5.0.1, aioredis 2.0.1 [Done]
- **Connection String**: `redis://localhost:6379/0`
- **Status**: [Config] Configured but not running
- **Planned Uses**:
  - Session management
  - Rate limiting
  - Real-time feed cache
  - OCR result caching

### Object Storage
**S3-Compatible Storage**
- AWS S3 / MinIO / Cloudflare R2
- Newspaper images
- Processed documents
- Model files

### Vector Database
**Qdrant** or **Pinecone**
- Semantic search
- Article similarity
- Content recommendation

### Message Queue
**RabbitMQ** or **Redis Streams**
- Async task processing
- OCR job queue
- Real-time event streaming

## Infrastructure

### Containerization
**Docker**
- All services containerized
- Development and production parity
- Easy deployment

### Orchestration
**Kubernetes** (Production)
- Auto-scaling
- Load balancing
- Self-healing
- Rolling updates

**Docker Compose** (Development)
- Simple local setup
- Fast iteration

### Cloud Provider
**Flexible**: AWS / GCP / Azure
- **Compute**: EC2 / GKE / AKS
- **Storage**: S3 / GCS / Azure Blob
- **CDN**: CloudFront / Cloud CDN
- **Functions**: Lambda (for lightweight tasks)

### CI/CD
- **GitHub Actions**: Primary CI/CD
- **Jenkins**: Alternative for complex pipelines
- **ArgoCD**: GitOps for Kubernetes

## Monitoring & Observability

### Metrics
**Prometheus + Grafana**
- System metrics
- Application metrics
- Custom dashboards
- Alerting

### Logging
**ELK Stack** (Elasticsearch, Logstash, Kibana)
- Centralized logging
- Log analysis
- Search and visualization

**Alternative**: **Loki** (lighter weight)

### Tracing
**Jaeger** or **Zipkin**
- Distributed tracing
- Performance bottleneck identification
- Request flow visualization

### Error Tracking
**Sentry**
- Error monitoring
- Performance monitoring
- Release tracking

### APM
**New Relic** or **DataDog**
- Application performance
- Infrastructure monitoring
- User experience tracking

## Development Tools

### Version Control
- **Git**: Source control
- **GitHub**: Repository hosting
- **Git LFS**: Large file storage (models)

### Code Quality
- **Ruff**: Python linting (fast)
- **Black**: Python formatting
- **ESLint**: JavaScript linting
- **Prettier**: JavaScript formatting
- **pre-commit**: Git hooks

### Testing [Done] COMPREHENSIVE SUITE
- **pytest**: Python testing framework [Done]
  - Comprehensive OCR test suite (25+ tests)
  - Security validation tests
  - Performance benchmarks
  - Error handling tests
  - Batch processing tests
- **Jest**: JavaScript testing (planned)
- **Playwright**: E2E testing (planned)
- **Locust**: Load testing (planned)

### API Documentation
- **Swagger/OpenAPI**: Auto-generated docs
- **Redoc**: Alternative documentation UI
- **Postman**: API testing and documentation

### IDE & Extensions
**VS Code** with:
- Python
- Pylance
- ESLint
- Prettier
- Docker
- Kubernetes

## Security

### Authentication & Authorization [Done] FRAMEWORK READY
- **JWT**: Token-based auth (configured, not active)
- **API Keys**: Custom "vuva_*" format with SHA-256 hashing [Done]
- **OAuth 2.0**: Third-party login (planned)
- **Auth0** or **Keycloak**: Identity provider (planned)

### Input Validation & Sanitization [Done] NEW
- **SecurityValidator class**: Input sanitization [Done]
  - Filename sanitization (path traversal prevention)
  - Language code validation
  - Text input sanitization (XSS/injection prevention)
  - Image content validation (magic bytes checking)
- **File Size Limits**: 10MB per image
- **Allowed Formats**: PNG, JPG, JPEG, BMP, TIFF

### API Security [Done] CONFIGURED
- **Rate Limiting**: slowapi (configured, not enforced) [Done]
  - FREE tier: 100 requests/hour
  - BASIC tier: 1,000 requests/hour
  - PREMIUM tier: 10,000 requests/hour
- **Security Headers**: X-Frame-Options, CSP, XSS-Protection [Done]
- **CORS**: Configured per environment
- **HTTPS**: TLS 1.3 (production ready)

### Secrets Management
- **HashiCorp Vault**: Production secrets
- **.env files**: Development (gitignored)
- **Kubernetes Secrets**: K8s deployments

### Vulnerability Scanning
- **Snyk**: Dependency scanning
- **Trivy**: Container scanning
- **OWASP ZAP**: Security testing

## Development Environment

### Package Managers
- **pip** + **poetry**: Python dependencies
- **npm** / **pnpm**: JavaScript dependencies

### Virtualization
- **pyenv**: Python version management
- **nvm**: Node version management
- **Docker**: Environment isolation

## Performance Optimization

### Caching Strategy
- **CDN**: Static assets
- **Redis**: API responses, sessions
- **Browser**: Service workers
- **Database**: Query results

### Compression
- **gzip/brotli**: HTTP responses
- **Image optimization**: Sharp, Pillow
- **Asset minification**: Webpack, Vite

### Load Balancing
- **Nginx**: Reverse proxy
- **HAProxy**: Alternative
- **Cloud Load Balancer**: AWS ALB, GCP LB

## Cost Optimization
 Status |
|-------|-----------|---------|--------|
| API | FastAPI 0.109.0 | Backend services | [Done] Operational |
| OCR | Tesseract + EasyOCR + Paddle | Text extraction | [Done] Operational |
| Fast OCR | Tesseract (optimized) | Real-time transcription | [Done] NEW |
| News | RSS + Hacker News + newspaper3k | Content aggregation | [Done] NEW |
| Security | Custom validation + API keys | Input protection | [Done] NEW |
| Testing | pytest + custom suite | Quality assurance | [Done] NEW |
| Frontend | Next.js | User interface | [Planned] Not started |
| ML | PyTorch + ONNX | Neural networks | [Config] Configured |
| Agents | LangChain | Intelligent processing | [Planned] Not started |
| Database | PostgreSQL + asyncpg | Primary data | [Config] Configured |
| Cache | Redis | Performance | [Config] Configured |
| Deployment | Docker + Kubernetes | Production | [Planned] Not started |

**Total Dependencies**: 67 packages (was 62)
**New Additions**: feedparser, newspaper3k, beautifulsoup4, slowapi, python-dateutilcost optimization
- **CDN**: Reduce bandwidth costs
- **Compression**: Reduce storage size

### Database
- **Read replicas**: Distribute load
- **Connection pooling**: Efficient connections
- **Query optimization**: Reduce compute

## Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API | FastAPI | Backend services |
| Frontend | Next.js | User interface |
| OCR | Tesseract + EasyOCR | Text extraction |
| ML | PyTorch + ONNX | Neural networks |
| Agents | LangChain | Intelligent processing |
| Database | PostgreSQL | Primary data |
| Cache | Redis | Performance |
| Storage | S3 | Images and files |
| Container | Docker | Deployment |
| Orchestration | Kubernetes | Scaling |
| Monitoring | Prometheus + Grafana | Observability |

**Total Stack Philosophy**: Lightweight, efficient, scalable, and developer-friendly.
