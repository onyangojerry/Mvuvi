# API Standards

## RESTful API Design Standards

### URL Structure
- Use lowercase letters
- Use hyphens for multi-word resources
- Use nouns, not verbs
- Maintain consistency across endpoints

**Examples**:
```
[Done] Good:
GET /api/v1/news-articles
POST /api/v1/newspaper-uploads
GET /api/v1/users/preferences

❌ Bad:
GET /api/v1/getNewsArticles
POST /api/v1/upload_newspaper
GET /api/v1/user-preferences
```

### HTTP Methods
- **GET**: Retrieve resources (idempotent, cacheable)
- **POST**: Create new resources
- **PUT**: Replace entire resource
- **PATCH**: Partial update
- **DELETE**: Remove resource

### Versioning
- Include version in URL: `/api/v1/`, `/api/v2/`
- Maintain backward compatibility for at least 2 versions
- Deprecation period: minimum 6 months
- Document breaking changes clearly

### Request Format

#### Headers
```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer {token}
X-Request-ID: {uuid}
X-API-Version: v1
```

#### Body Structure
```json
{
  "data": {
    "type": "newspaper-upload",
    "attributes": {
      "image": "base64_encoded_string",
      "language": "en",
      "source": "daily-times"
    }
  },
  "meta": {
    "timestamp": "2026-01-24T10:30:00Z",
    "client_version": "1.0.0"
  }
}
```

### Response Format

#### Success Response
```json
{
  "status": "success",
  "data": {
    "id": "article_123",
    "type": "news-article",
    "attributes": {
      "title": "Breaking News",
      "content": "Article content...",
      "extracted_at": "2026-01-24T10:30:15Z"
    }
  },
  "meta": {
    "processing_time_ms": 234,
    "confidence_score": 0.98
  }
}
```

#### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_IMAGE_FORMAT",
    "message": "The uploaded image must be in PNG, JPG, or PDF format",
    "details": {
      "received_format": "bmp",
      "supported_formats": ["png", "jpg", "jpeg", "pdf"]
    }
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-24T10:30:00Z"
  }
}
```

### Status Codes

#### Success Codes
- **200 OK**: Successful GET, PUT, PATCH, DELETE
- **201 Created**: Successful POST
- **202 Accepted**: Async processing started
- **204 No Content**: Successful DELETE with no body

#### Client Error Codes
- **400 Bad Request**: Invalid request format
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded

#### Server Error Codes
- **500 Internal Server Error**: Unexpected server error
- **502 Bad Gateway**: Upstream service error
- **503 Service Unavailable**: Temporary unavailability
- **504 Gateway Timeout**: Upstream timeout

### Error Codes Reference

| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_IMAGE_FORMAT` | Unsupported image format | Use PNG, JPG, or PDF |
| `IMAGE_TOO_LARGE` | File size exceeds limit | Max 10MB per image |
| `OCR_PROCESSING_FAILED` | OCR engine error | Retry or check image quality |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait or upgrade plan |
| `INVALID_TOKEN` | Invalid authentication | Refresh token |
| `INSUFFICIENT_CREDITS` | API credits depleted | Purchase more credits |

### Pagination

#### Query Parameters
```
GET /api/v1/news-articles?page=2&page_size=20&sort=-created_at
```

#### Response Structure
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "page_size": 20,
    "total_pages": 15,
    "total_items": 293,
    "has_next": true,
    "has_previous": true
  },
  "links": {
    "self": "/api/v1/news-articles?page=2",
    "first": "/api/v1/news-articles?page=1",
    "prev": "/api/v1/news-articles?page=1",
    "next": "/api/v1/news-articles?page=3",
    "last": "/api/v1/news-articles?page=15"
  }
}
```

### Filtering and Sorting

#### Filtering
```
GET /api/v1/news-articles?category=politics&language=en&date_from=2026-01-01
```

#### Sorting
- Use `-` prefix for descending order
- Use `+` or no prefix for ascending
```
GET /api/v1/news-articles?sort=-created_at,title
```

### Rate Limiting

#### Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1706097600
```

#### Limits by Tier
- **Free**: 100 requests/hour
- **Basic**: 1,000 requests/hour
- **Pro**: 10,000 requests/hour
- **Enterprise**: Custom limits

### Authentication

#### JWT Token Structure
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Token Refresh
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "refresh_token_value"
}
```

### WebSocket Standards

#### Connection
```javascript
const ws = new WebSocket('wss://api.example.com/v1/feed/stream');
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['breaking-news', 'user-preferences']
}));
```

#### Message Format
```json
{
  "type": "news_update",
  "data": {
    "article_id": "article_456",
    "title": "Breaking: Major announcement"
  },
  "timestamp": "2026-01-24T10:30:00Z"
}
```

### Documentation Standards

#### OpenAPI/Swagger
- All endpoints must be documented in OpenAPI 3.0 format
- Include request/response examples
- Document all error scenarios
- Keep documentation in sync with code

#### Changelog
- Document all API changes
- Include migration guides for breaking changes
- Publish release notes

### Performance Standards

#### Response Time Targets
- **Simple GET requests**: <50ms (p95)
- **Complex queries**: <200ms (p95)
- **Upload processing**: <5 seconds
- **Real-time updates**: <100ms latency

#### Payload Size
- Request body: Max 10MB
- Response body: Max 5MB (use pagination for larger datasets)
- Compression: Always use gzip/brotli

### Security Standards

#### HTTPS Only
- All API traffic must use HTTPS
- Minimum TLS 1.3
- Valid SSL certificate required

#### Input Validation
- Validate all input data
- Sanitize user inputs
- Use parameter type checking
- Implement max length limits

#### CORS Configuration
```javascript
{
  "allowed_origins": ["https://app.example.com"],
  "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
  "allowed_headers": ["Content-Type", "Authorization"],
  "max_age": 86400
}
```

### Monitoring and Logging

#### Request Logging
- Log all API requests with:
  - Request ID
  - Method and path
  - Status code
  - Response time
  - User ID (if authenticated)

#### Metrics to Track
- Request rate per endpoint
- Error rate by type
- Average response time
- P95 and P99 latency
- Active connections (WebSocket)

### Deprecation Process

1. **Announce**: 6 months notice
2. **Mark**: Add deprecation headers
   ```http
   X-API-Deprecated: true
   X-API-Deprecation-Date: 2026-07-24
   X-API-Migration-Guide: https://docs.example.com/migration
   ```
3. **Sunset**: Final removal date
4. **Redirect**: Provide migration path

### Testing Standards

#### API Testing Requirements
- Unit tests: 80%+ coverage
- Integration tests for all endpoints
- Load testing for performance targets
- Security testing (OWASP compliance)

#### Mock Responses
- Provide sandbox environment
- Mock data for testing
- No rate limits in sandbox

### Compliance

- **GDPR**: Data privacy requirements
- **CCPA**: California privacy compliance
- **SOC 2**: Security controls
- **OWASP Top 10**: Security standards
