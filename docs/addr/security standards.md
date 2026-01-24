# Security Standards

## Overview
Comprehensive security standards for the Newspaper Ingestion API system to ensure data protection, secure operations, and compliance with industry best practices.

---

## Authentication & Authorization

### Authentication Methods

#### JWT (JSON Web Tokens)
**Implementation**:
```python
# Token structure
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id_123",
    "email": "user@example.com",
    "role": "premium",
    "iat": 1706097600,
    "exp": 1706184000
  }
}
```

**Requirements**:
- Algorithm: RS256 (asymmetric)
- Token expiry: 15 minutes (access token)
- Refresh token expiry: 7 days
- Token rotation on refresh
- Revocation list for compromised tokens

#### OAuth 2.0
**Supported Flows**:
- Authorization Code (for web apps)
- PKCE (for mobile/SPA)
- Client Credentials (for service-to-service)

**Third-party Providers**:
- Google OAuth
- GitHub OAuth
- Microsoft Azure AD

### Authorization Model

#### Role-Based Access Control (RBAC)

**Roles**:
```yaml
free:
  - read:own_uploads
  - upload:newspapers (100/month)
  - read:feed

basic:
  - read:own_uploads
  - upload:newspapers (1000/month)
  - read:feed
  - write:preferences

premium:
  - read:own_uploads
  - upload:newspapers (unlimited)
  - read:feed
  - write:preferences
  - read:analytics
  - access:api

admin:
  - all:permissions
  - manage:users
  - access:admin_panel
```

#### API Key Management
- API keys for programmatic access
- Scoped permissions per key
- Rate limits per key
- Key rotation every 90 days
- Automatic expiration warning
- Audit log for key usage

---

## Data Security

### Encryption Standards

#### Data at Rest
**Database Encryption**:
- PostgreSQL: Transparent Data Encryption (TDE)
- Encryption algorithm: AES-256-GCM
- Key management: AWS KMS / HashiCorp Vault
- Automatic key rotation: 90 days

**File Storage Encryption**:
- S3 server-side encryption (SSE-S3 or SSE-KMS)
- All newspaper images encrypted
- Encrypted backups
- Secure deletion (7-pass overwrite)

#### Data in Transit
**Requirements**:
- TLS 1.3 minimum
- TLS 1.2 acceptable (with strong ciphers only)
- Disable SSL, TLS 1.0, TLS 1.1
- Perfect Forward Secrecy (PFS)
- HSTS enabled (max-age: 31536000)

**Cipher Suites** (Preferred order):
```
TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
TLS_AES_128_GCM_SHA256
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-RSA-AES128-GCM-SHA256
```

**Certificate Management**:
- Valid SSL certificates from trusted CAs
- Automatic renewal (Let's Encrypt)
- Certificate pinning for mobile apps
- OCSP stapling enabled

### Sensitive Data Handling

#### PII (Personally Identifiable Information)
**Data Classification**:
- **Restricted**: Passwords, API keys, tokens
- **Confidential**: Email, phone, payment info
- **Internal**: User preferences, usage stats
- **Public**: Published articles, public profiles

**Protection Measures**:
- Hash passwords with bcrypt (cost factor: 12)
- Never log PII
- Mask PII in non-production environments
- Data minimization principle
- Pseudonymization where possible

#### Password Policy
**Requirements**:
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, special chars
- No common passwords (check against breach database)
- Password history: prevent reuse of last 5 passwords
- Account lockout: 5 failed attempts (15-minute lockout)
- Password reset: secure token (1-hour expiry)

**Implementation**:
```python
# Password strength requirements
MIN_LENGTH = 12
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL = True
CHECK_BREACH_DATABASE = True  # HaveIBeenPwned API
```

### Data Retention and Deletion

**Retention Policies**:
- User data: Until account deletion + 30 days
- Upload history: 2 years
- Processed articles: 1 year
- Logs: 90 days (security logs: 1 year)
- Backups: 30 days

**Right to Deletion** (GDPR Article 17):
- User can request account deletion
- Complete data removal within 30 days
- Confirmation email sent
- Exceptions: legal obligations, fraud prevention

---

## Application Security

### Input Validation

#### API Input Validation
**Validation Rules**:
```python
# Example validation schema
newspaper_upload_schema = {
    "image": {
        "type": "file",
        "max_size": "10MB",
        "allowed_types": ["image/jpeg", "image/png", "application/pdf"],
        "required": True
    },
    "language": {
        "type": "string",
        "pattern": "^[a-z]{2}$",
        "default": "en"
    },
    "source": {
        "type": "string",
        "max_length": 100,
        "sanitize": True
    }
}
```

**Sanitization**:
- Strip HTML tags from text inputs
- Escape special characters
- Validate file types (magic numbers, not extensions)
- Reject malformed JSON/data

#### File Upload Security
**Checks**:
1. Validate MIME type
2. Check magic numbers (file signature)
3. Scan for malware (ClamAV)
4. Size limits enforced
5. Rename uploaded files (UUID)
6. Store outside web root
7. Generate signed URLs for access

**Rejected Files**:
- Executable files (.exe, .sh, .bat)
- Archives (.zip, .tar, .gz) - unless explicitly supported
- Files with double extensions
- Files with EXIF data containing scripts

### SQL Injection Prevention

**Measures**:
- Use parameterized queries ONLY
- ORM (SQLAlchemy) with proper escaping
- Principle of least privilege for DB users
- Disable dynamic SQL where possible
- Input validation before DB queries

**Example (Correct)**:
```python
# [Done] Safe - parameterized query
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (user_email,)
)

# ❌ NEVER do this
cursor.execute(
    f"SELECT * FROM users WHERE email = '{user_email}'"
)
```

### XSS (Cross-Site Scripting) Prevention

**Measures**:
- Content Security Policy (CSP)
- Output encoding/escaping
- HTTPOnly cookies
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY

**CSP Header**:
```
Content-Security-Policy: 
  default-src 'self'; 
  script-src 'self' 'strict-dynamic'; 
  style-src 'self' 'unsafe-inline'; 
  img-src 'self' https: data:; 
  font-src 'self'; 
  connect-src 'self' wss://api.example.com;
  frame-ancestors 'none';
```

### CSRF (Cross-Site Request Forgery) Prevention

**Measures**:
- CSRF tokens for state-changing operations
- SameSite cookie attribute
- Verify Origin/Referer headers
- Double-submit cookie pattern

**Implementation**:
```python
# CSRF token generation
csrf_token = secrets.token_urlsafe(32)

# Cookie settings
Set-Cookie: session_id=abc123; 
  HttpOnly; 
  Secure; 
  SameSite=Strict; 
  Max-Age=3600
```

### SSRF (Server-Side Request Forgery) Prevention

**Measures**:
- Whitelist allowed domains
- Disable URL redirects
- Validate and sanitize URLs
- Use network segmentation
- Block internal IP ranges

**Blocked IP Ranges**:
```
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
127.0.0.0/8
169.254.0.0/16
```

---

## API Security

### Rate Limiting

**Limits by Endpoint**:
```yaml
# Unauthenticated
/api/v1/auth/login: 5 requests/min
/api/v1/auth/register: 3 requests/min

# Free tier
/api/v1/ingest/upload: 100 requests/day
/api/v1/feed: 1000 requests/hour

# Premium tier
/api/v1/ingest/upload: unlimited
/api/v1/feed: 10000 requests/hour
```

**Implementation**:
- Redis-based rate limiting
- Token bucket algorithm
- Rate limit headers in response
- 429 status code when exceeded

**Headers**:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1706097600
Retry-After: 3600
```

### API Request Signing

**For Sensitive Operations**:
```python
# HMAC signature verification
def verify_signature(request):
    timestamp = request.headers.get('X-Timestamp')
    signature = request.headers.get('X-Signature')
    
    # Prevent replay attacks (5-minute window)
    if abs(time.time() - int(timestamp)) > 300:
        return False
    
    # Verify signature
    payload = f"{timestamp}{request.method}{request.path}{request.body}"
    expected = hmac.new(
        api_secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)
```

### CORS Configuration

**Settings**:
```python
CORS_CONFIG = {
    "allowed_origins": [
        "https://app.example.com",
        "https://mobile.example.com"
    ],
    "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    "allowed_headers": [
        "Content-Type", 
        "Authorization",
        "X-Request-ID"
    ],
    "expose_headers": [
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining"
    ],
    "max_age": 3600,
    "credentials": True
}
```

---

## Infrastructure Security

### Network Security

**Architecture**:
```
Internet → WAF → Load Balancer → API Servers (Private Subnet)
                                   ↓
                              Database (Isolated Subnet)
```

**Firewall Rules**:
- Deny all by default
- Allow HTTPS (443) from internet
- Allow SSH (22) from bastion host only
- Database accessible only from API servers
- Egress filtering for sensitive data

**WAF (Web Application Firewall)**:
- OWASP Core Rule Set
- DDoS protection
- Rate limiting at edge
- Bot detection
- Geo-blocking (if needed)

### Container Security

**Docker Best Practices**:
- Use minimal base images (Alpine, Distroless)
- Run as non-root user
- Read-only root filesystem
- No secrets in images
- Scan images for vulnerabilities
- Sign images

**Example Dockerfile**:
```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . /app
WORKDIR /app

# Switch to non-root user
USER appuser

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

**Kubernetes Security**:
- Pod Security Standards (restricted)
- Network Policies
- RBAC for service accounts
- Secrets encrypted at rest
- No privileged containers
- Resource limits enforced

### Secrets Management

**HashiCorp Vault** (Preferred):
```python
# Dynamic secrets
import hvac

client = hvac.Client(url='https://vault.example.com')
client.auth.kubernetes.login(role='api-server')

# Read database credentials (auto-rotated)
db_creds = client.secrets.database.generate_credentials(
    name='postgres-role',
    ttl='1h'
)
```

**Best Practices**:
- Never commit secrets to Git
- Rotate secrets regularly
- Use different secrets per environment
- Audit secret access
- Automatic expiration

---

## Monitoring & Incident Response

### Security Monitoring

**Metrics to Track**:
- Failed login attempts
- API rate limit violations
- Unusual traffic patterns
- Database query anomalies
- File upload patterns
- Token usage patterns

**Alerting**:
```yaml
alerts:
  - name: "Multiple Failed Logins"
    condition: failed_logins > 10 in 5min
    severity: HIGH
    notify: security-team
    
  - name: "Unusual API Traffic"
    condition: requests > 2x baseline
    severity: MEDIUM
    notify: devops-team
    
  - name: "Malware Detected"
    condition: malware_scan = positive
    severity: CRITICAL
    notify: security-team
    action: quarantine_file
```

### Logging Standards

**What to Log**:
- Authentication attempts (success/failure)
- API requests (method, path, user, IP)
- Authorization failures
- Data access (who accessed what)
- Configuration changes
- Error and exceptions

**What NOT to Log**:
- Passwords
- API keys/tokens
- Credit card numbers
- Session IDs
- Other PII

**Log Format** (JSON):
```json
{
  "timestamp": "2026-01-24T10:30:00Z",
  "level": "INFO",
  "service": "api-server",
  "user_id": "user_123",
  "ip": "203.0.113.42",
  "method": "POST",
  "path": "/api/v1/ingest/upload",
  "status": 201,
  "duration_ms": 234,
  "request_id": "req_abc123"
}
```

### Incident Response Plan

**Phases**:
1. **Preparation**: Playbooks, tools, training
2. **Detection**: Monitoring, alerts, reports
3. **Containment**: Isolate affected systems
4. **Eradication**: Remove threat
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Postmortem, improvements

**Response Times**:
- **Critical** (data breach, active attack): <15 minutes
- **High** (vulnerability exploitation): <1 hour
- **Medium** (suspicious activity): <4 hours
- **Low** (potential threats): <24 hours

**Communication**:
- Internal: Slack #security-incidents
- External: security@example.com
- Users: Status page, email notifications

---

## Compliance

### GDPR (General Data Protection Regulation)

**Requirements**:
- [Done] Lawful basis for processing
- [Done] Data minimization
- [Done] Purpose limitation
- [Done] Storage limitation
- [Done] Integrity and confidentiality
- [Done] Accountability

**User Rights**:
- Right to access (export data)
- Right to rectification (update data)
- Right to erasure (delete account)
- Right to data portability (download)
- Right to object (opt-out)

**Implementation**:
```python
# Data export endpoint
@app.get("/api/v1/users/me/export")
def export_user_data(user: User):
    return {
        "personal_info": user.personal_data(),
        "uploads": user.uploads.all(),
        "preferences": user.preferences,
        "activity": user.activity_log
    }
```

### CCPA (California Consumer Privacy Act)

**Requirements**:
- Disclose data collection practices
- Allow opt-out of data sale
- Provide data deletion
- Non-discrimination for exercising rights

### SOC 2 Type II

**Focus Areas**:
- Security
- Availability
- Processing Integrity
- Confidentiality
- Privacy

**Controls**:
- Access controls
- Encryption
- Change management
- Incident response
- Vendor management

### PCI DSS (If handling payments)

**Requirements**:
- Use payment processor (Stripe, PayPal)
- No storage of card data
- Secure transmission
- Regular security testing
- Access control measures

---

## Security Testing

### Automated Testing

**SAST (Static Application Security Testing)**:
- **Tool**: Bandit (Python), SonarQube
- **Frequency**: Every commit (CI/CD)
- **Checks**: Code vulnerabilities, secrets

**DAST (Dynamic Application Security Testing)**:
- **Tool**: OWASP ZAP
- **Frequency**: Weekly, before releases
- **Checks**: Runtime vulnerabilities

**Dependency Scanning**:
- **Tool**: Snyk, Dependabot
- **Frequency**: Daily
- **Action**: Auto-create PRs for updates

**Container Scanning**:
- **Tool**: Trivy, Clair
- **Frequency**: On image build
- **Action**: Block deployment if critical

### Manual Security Testing

**Penetration Testing**:
- **Frequency**: Quarterly
- **Scope**: Full application
- **Provider**: External security firm
- **Report**: Detailed findings + remediation

**Code Review**:
- Security-focused review for sensitive code
- Cryptography implementation review
- Authentication/authorization review

---

## Security Checklist

### Development
- [ ] Input validation on all endpoints
- [ ] Parameterized queries only
- [ ] Output encoding
- [ ] CSRF tokens
- [ ] Secure password hashing
- [ ] No secrets in code
- [ ] Security headers configured

### Deployment
- [ ] TLS 1.3 enabled
- [ ] Security patches applied
- [ ] Secrets in vault
- [ ] Firewall rules configured
- [ ] Monitoring enabled
- [ ] Backups encrypted
- [ ] Access logs enabled

### Production
- [ ] Regular security scans
- [ ] Penetration testing done
- [ ] Incident response plan ready
- [ ] On-call rotation configured
- [ ] Audit logs reviewed
- [ ] Compliance requirements met
- [ ] Security training completed

---

## Security Contacts

- **Security Team**: security@example.com
- **Incident Hotline**: +1-XXX-XXX-XXXX
- **Bug Bounty**: https://hackerone.com/example
- **Responsible Disclosure**: security.txt

## Security Training

**Required Training**:
- OWASP Top 10
- Secure coding practices
- Data privacy (GDPR/CCPA)
- Incident response procedures
- Social engineering awareness

**Frequency**: Quarterly for all engineers
