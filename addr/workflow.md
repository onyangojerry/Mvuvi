# Development Workflow

## Agile Methodology

### Sprint Structure
- **Duration**: 2 weeks
- **Sprint Planning**: Monday, Week 1 (2 hours)
- **Daily Standups**: Every day at 9:30 AM (15 min)
- **Sprint Review**: Friday, Week 2 (1 hour)
- **Sprint Retrospective**: Friday, Week 2 (1 hour)

---

## Git Workflow

### Branch Strategy (Git Flow)

```
main (production)
  │
  ├── develop (integration)
  │     │
  │     ├── feature/newspaper-upload-api
  │     ├── feature/ocr-integration
  │     ├── feature/real-time-feed
  │     │
  │     ├── bugfix/image-validation
  │     │
  │     └── hotfix/security-patch
  │
  └── release/v1.0.0
```

### Branch Naming Convention

**Features**:
```
feature/<ticket-number>-<short-description>
Example: feature/VUVA-123-newspaper-upload
```

**Bug Fixes**:
```
bugfix/<ticket-number>-<short-description>
Example: bugfix/VUVA-456-ocr-timeout
```

**Hotfixes**:
```
hotfix/<ticket-number>-<short-description>
Example: hotfix/VUVA-789-security-patch
```

**Releases**:
```
release/v<major>.<minor>.<patch>
Example: release/v1.2.0
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes
- `ci`: CI/CD changes

**Examples**:
```
feat(api): add newspaper upload endpoint

Implemented POST /api/v1/ingest/upload endpoint with
image validation and S3 storage integration.

Closes VUVA-123
```

```
fix(ocr): handle non-UTF8 characters in extracted text

Added character encoding detection and conversion to
prevent errors when processing newspapers with special
characters.

Fixes VUVA-456
```

```
perf(ml): optimize neural network inference time

Reduced model inference time by 40% through batch
processing and ONNX runtime optimization.

VUVA-789
```

---

## Development Process

### 1. Ticket Creation
- Product Manager creates user stories in Jira/Linear
- Technical Lead breaks down into technical tasks
- Estimate story points (Fibonacci: 1, 2, 3, 5, 8, 13)
- Assign to sprint backlog

### 2. Feature Development

#### Step 1: Start Work
```bash
# Sync with develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/VUVA-123-newspaper-upload

# Move ticket to "In Progress"
```

#### Step 2: Implementation
1. Write failing tests (TDD approach)
2. Implement feature
3. Make tests pass
4. Refactor code
5. Update documentation
6. Self-review changes

#### Step 3: Local Testing
```bash
# Run tests
pytest tests/

# Run linter
ruff check .

# Format code
black .

# Type checking
mypy src/
```

#### Step 4: Commit Changes
```bash
git add .
git commit -m "feat(api): add newspaper upload endpoint

Implemented POST /api/v1/ingest/upload with validation

VUVA-123"
```

#### Step 5: Push and Create PR
```bash
git push origin feature/VUVA-123-newspaper-upload
```

Create Pull Request on GitHub:
- Title: `[VUVA-123] Add newspaper upload endpoint`
- Description: Detailed explanation with context
- Link to ticket
- Screenshots/videos if UI changes
- Testing instructions

---

## Code Review Process

### PR Requirements
- ✅ All tests passing
- ✅ Code coverage maintained (>80%)
- ✅ Linting passed
- ✅ No merge conflicts
- ✅ Description complete
- ✅ Self-reviewed

### Review Guidelines

**Reviewers Check**:
1. **Functionality**: Does it work as intended?
2. **Code Quality**: Is it clean and maintainable?
3. **Performance**: Any performance concerns?
4. **Security**: Any security vulnerabilities?
5. **Tests**: Adequate test coverage?
6. **Documentation**: Is it documented?

**Review Timeline**:
- Small PRs (<200 lines): 4 hours
- Medium PRs (200-500 lines): 1 day
- Large PRs (>500 lines): 2 days

**Approval Requirements**:
- Backend: 2 approvals (1 from Backend Lead)
- Frontend: 2 approvals (1 from Frontend Lead)
- ML/AI: 2 approvals (1 from ML Lead)
- Infrastructure: 1 approval from DevOps Lead

### PR Comments
Use conventional labels:
- **[MUST]**: Required change
- **[SHOULD]**: Strong suggestion
- **[CONSIDER]**: Optional suggestion
- **[QUESTION]**: Need clarification
- **[NITPICK]**: Minor style preference

---

## Testing Workflow

### Test Levels

#### 1. Unit Tests
- **Who**: Developer writing the code
- **When**: During development (TDD)
- **Coverage Target**: >80%
- **Tools**: pytest, Jest
- **Run**: Automatically on commit (pre-commit hook)

#### 2. Integration Tests
- **Who**: Developer
- **When**: After unit tests pass
- **Coverage**: All API endpoints
- **Tools**: pytest with fixtures, Supertest
- **Run**: In CI pipeline

#### 3. E2E Tests
- **Who**: QA Engineers
- **When**: Before release
- **Coverage**: Critical user flows
- **Tools**: Playwright, Cypress
- **Run**: Nightly and before releases

#### 4. Performance Tests
- **Who**: DevOps + Backend team
- **When**: Weekly and before releases
- **Tools**: Locust, k6
- **Targets**: Match performance standards

#### 5. Security Tests
- **Who**: Security team / DevOps
- **When**: Weekly automated scans
- **Tools**: Snyk, OWASP ZAP, Trivy
- **Run**: CI pipeline + scheduled scans

### Test Environments

| Environment | Purpose | Data | Branch |
|-------------|---------|------|--------|
| Local | Development | Fake/Mock | feature/* |
| Dev | Integration | Test data | develop |
| Staging | Pre-production | Sanitized prod | release/* |
| Production | Live | Real data | main |

---

## CI/CD Pipeline

### Continuous Integration (GitHub Actions)

#### On Pull Request:
```yaml
jobs:
  - Lint and format check
  - Unit tests
  - Integration tests
  - Security scan
  - Build Docker images
  - Code coverage report
```

#### On Merge to Develop:
```yaml
jobs:
  - All PR checks
  - E2E tests
  - Deploy to Dev environment
  - Run smoke tests
```

#### On Merge to Main:
```yaml
jobs:
  - All checks
  - Build production images
  - Deploy to staging
  - Run full test suite
  - Deploy to production (manual approval)
  - Post-deployment tests
```

### Deployment Process

#### Dev Environment (Automatic)
```bash
1. Merge to develop
2. CI builds and tests
3. Auto-deploy to dev
4. Run smoke tests
5. Notify team in Slack
```

#### Staging (Automatic)
```bash
1. Create release branch
2. CI builds and tests
3. Deploy to staging
4. Run full test suite
5. QA validation
```

#### Production (Manual Approval)
```bash
1. All staging tests pass
2. Product Manager approval
3. Technical Lead approval
4. Deploy to production (blue-green)
5. Monitor for 30 minutes
6. Complete cutover or rollback
7. Tag release in Git
```

---

## Release Workflow

### Version Numbering (Semantic Versioning)
```
v<MAJOR>.<MINOR>.<PATCH>

Example: v1.4.2
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Process

#### Week Before Release
- **Monday**: Feature freeze, create release branch
- **Tuesday-Thursday**: Bug fixes only, QA testing
- **Friday**: Release notes preparation

#### Release Day
```bash
# 1. Create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.4.0

# 2. Update version numbers
# Update package.json, version.py, etc.

# 3. Update CHANGELOG.md
# Document all changes

# 4. Commit and push
git commit -m "chore: bump version to 1.4.0"
git push origin release/v1.4.0

# 5. Deploy to staging
# CI/CD handles deployment

# 6. Final QA approval

# 7. Merge to main
git checkout main
git merge release/v1.4.0
git tag -a v1.4.0 -m "Release version 1.4.0"
git push origin main --tags

# 8. Merge back to develop
git checkout develop
git merge release/v1.4.0
git push origin develop

# 9. Deploy to production
# Manual approval in CI/CD

# 10. Publish release notes
# GitHub Releases page
```

---

## Hotfix Workflow

For critical production issues:

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/VUVA-999-critical-bug

# 2. Fix the issue
# Implement fix and tests

# 3. Test locally and in staging

# 4. Create PR to main
# Requires immediate review

# 5. Deploy to production ASAP

# 6. Merge to develop
git checkout develop
git merge hotfix/VUVA-999-critical-bug
```

---

## Documentation Workflow

### When to Update Docs
- New API endpoints
- Changed functionality
- New configuration options
- Architecture changes
- Breaking changes

### Documentation Types

1. **Code Comments**
   - Inline for complex logic
   - Docstrings for functions/classes
   - Type hints (Python, TypeScript)

2. **API Documentation**
   - OpenAPI/Swagger specs
   - Auto-generated from code
   - Updated with every API change

3. **Architecture Docs**
   - ADRs (Architecture Decision Records)
   - System diagrams
   - Data flow diagrams

4. **User Guides**
   - Getting started
   - Feature tutorials
   - Troubleshooting

5. **Developer Docs**
   - Setup instructions
   - Contribution guidelines
   - Coding standards

---

## Monitoring and Incident Response

### Incident Severity Levels

**P0 - Critical**:
- Complete service outage
- Data loss
- Security breach
- **Response**: Immediate (24/7)

**P1 - High**:
- Major feature broken
- Performance degradation
- **Response**: <1 hour during business hours

**P2 - Medium**:
- Minor feature broken
- Non-critical bugs
- **Response**: <4 hours

**P3 - Low**:
- Cosmetic issues
- Minor inconveniences
- **Response**: Next sprint

### On-Call Rotation
- **Rotation**: Weekly
- **Coverage**: 24/7 for P0/P1
- **Escalation**: Team Lead → Technical Lead → CTO

### Incident Response Process
1. **Detect**: Monitoring alerts or user report
2. **Acknowledge**: On-call engineer responds
3. **Assess**: Determine severity
4. **Communicate**: Notify stakeholders
5. **Resolve**: Fix the issue
6. **Verify**: Confirm resolution
7. **Postmortem**: Document and learn

---

## Meeting Cadence

| Meeting | Frequency | Duration | Participants |
|---------|-----------|----------|--------------|
| Daily Standup | Daily | 15 min | Engineering team |
| Sprint Planning | Bi-weekly | 2 hours | All team |
| Sprint Review | Bi-weekly | 1 hour | All + stakeholders |
| Sprint Retro | Bi-weekly | 1 hour | Engineering team |
| Tech Sync | Weekly | 1 hour | Leads |
| Product Review | Weekly | 30 min | PM + Tech Lead |
| All Hands | Monthly | 1 hour | Entire company |

---

## Tools and Platforms

| Category | Tool | Purpose |
|----------|------|---------|
| Project Management | Jira/Linear | Task tracking |
| Version Control | GitHub | Code repository |
| CI/CD | GitHub Actions | Automation |
| Communication | Slack | Team chat |
| Documentation | Notion/Confluence | Knowledge base |
| Monitoring | Grafana | Metrics visualization |
| Error Tracking | Sentry | Error monitoring |
| API Testing | Postman | API development |
| Design | Figma | UI/UX design |
| Analytics | Mixpanel | Product analytics |
