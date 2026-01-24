# Week 5 Implementation Checklist

> Detailed task breakdown for Phase 2.6 - Production Hardening

**Week:** Jan 27 - Jan 31, 2026  
**Focus:** Redis caching, rate limiting, database optimization, scheduled tasks, integration tests  
**Goal:** Achieve 80% overall completion

---

## 🎯 Week 5 Objectives

- ✅ **v1.2.0 Complete** (75% overall)
- 🎯 **v1.3.0 Target** (80% overall) - Production hardening
- 🎯 **Test Coverage:** 75% → 85%
- 🎯 **API Response Time:** 100ms → <50ms (p95)
- 🎯 **Cache Hit Rate:** 0% → 80%

---

## Day 1: Monday, Jan 27 - Redis Caching Foundation

### Morning (3 hours)
- [ ] **Install Redis** (if not running)
  ```bash
  brew install redis          # macOS
  brew services start redis
  redis-cli ping              # Should return PONG
  ```

- [ ] **Add Redis dependencies**
  ```bash
  pip install redis hiredis aioredis
  echo "redis==5.2.1" >> requirements.txt
  echo "hiredis==3.0.0" >> requirements.txt
  ```

- [ ] **Create cache service** (`src/services/cache_service.py`)
  - CacheService class
  - get(), set(), delete() methods
  - TTL support
  - Connection pooling
  - Graceful degradation

### Afternoon (4 hours)
- [ ] **Integrate caching with OCR**
  - Cache OCR results (1-hour TTL)
  - Key format: `ocr:{image_hash}`
  - Update `src/services/ocr_service.py`
  - Add cache hit/miss metrics

- [ ] **Write cache tests** (`tests/test_cache.py`)
  - Test get/set/delete
  - Test TTL expiration
  - Test connection failure handling
  - Test cache invalidation

- [ ] **Update configuration**
  - Add REDIS_URL to .env
  - Add cache settings to src/config.py

**End of Day Deliverables:**
- ✅ Redis running and connected
- ✅ CacheService implemented
- ✅ OCR caching working
- ✅ 10+ cache tests passing

---

## Day 2: Tuesday, Jan 28 - Complete Caching + Rate Limiting

### Morning (3 hours)
- [ ] **Extend caching to news API**
  - Cache article lists (5-minute TTL)
  - Cache user preferences (15-minute TTL)
  - Update `src/api/v1/news.py`
  - Add cache warming for popular queries

- [ ] **Add cache monitoring**
  - Cache hit rate metric (Prometheus)
  - Cache size tracking
  - Cache eviction stats
  - Update /metrics endpoint

- [ ] **Cache middleware** (`src/middleware/cache.py`)
  - Response caching for GET requests
  - ETag support
  - Cache-Control headers

### Afternoon (4 hours)
- [ ] **Implement rate limiting** (`src/middleware/rate_limit.py`)
  - Redis-backed rate limiter
  - Tier-based limits (FREE: 100/day, BASIC: 1000/day, PREMIUM: 10000/day)
  - Per-endpoint limits
  - Rate limit headers (X-RateLimit-*)
  - 429 responses with Retry-After

- [ ] **Integrate rate limiting**
  - Apply to all API endpoints
  - Admin bypass logic
  - Rate limit tests (20+ cases)

**End of Day Deliverables:**
- ✅ News API cached
- ✅ Cache monitoring active
- ✅ Rate limiting enforced
- ✅ Rate limit tests passing

---

## Day 3: Wednesday, Jan 29 - Database Optimization

### Morning (3 hours)
- [ ] **Database performance analysis**
  - Run query profiling
  - Identify slow queries
  - Check missing indexes

- [ ] **Create optimization migration**
  ```bash
  alembic revision -m "add_performance_indexes"
  ```

- [ ] **Add indexes** (`alembic/versions/002_performance_indexes.py`)
  ```sql
  CREATE INDEX idx_articles_published ON articles(published_date DESC);
  CREATE INDEX idx_articles_category ON articles(category);
  CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);
  CREATE INDEX idx_audit_logs_created ON audit_logs(created_at DESC);
  CREATE INDEX idx_sources_status ON sources(status) WHERE status = 'active';
  ```

- [ ] **Run migration**
  ```bash
  alembic upgrade head
  ```

### Afternoon (4 hours)
- [ ] **Query optimization**
  - Fix N+1 queries (use joinedload)
  - Update article retrieval queries
  - Add query result caching
  - Optimize full-text search

- [ ] **Connection pool tuning**
  - Adjust pool size based on load
  - Add connection monitoring
  - Test under load

- [ ] **Performance testing**
  - Benchmark before/after
  - Run load tests
  - Document improvements

**End of Day Deliverables:**
- ✅ Database indexes added
- ✅ Query times <50ms
- ✅ No N+1 queries
- ✅ Performance report

---

## Day 4: Thursday, Jan 30 - Scheduled Tasks

### Morning (3 hours)
- [ ] **Install task scheduler**
  ```bash
  pip install apscheduler
  echo "APScheduler==3.10.4" >> requirements.txt
  ```

- [ ] **Create scheduler service** (`src/services/scheduler_service.py`)
  - Initialize APScheduler
  - Job management
  - Error handling
  - Job monitoring

- [ ] **Implement news fetching job**
  - Fetch from all active sources
  - Store new articles
  - Update existing articles
  - Detect duplicates
  - Handle failures

### Afternoon (4 hours)
- [ ] **Configure fetch schedules**
  - Tech sources: Every 15 minutes
  - Business sources: Every 30 minutes
  - General news: Every 1 hour

- [ ] **Add job monitoring**
  - Job execution metrics
  - Failure alerts
  - Last run timestamp
  - Success rate tracking

- [ ] **Test scheduler**
  - Manual trigger
  - Scheduled execution
  - Error recovery
  - Duplicate prevention

- [ ] **Update main.py**
  - Start scheduler on startup
  - Shutdown scheduler gracefully

**End of Day Deliverables:**
- ✅ APScheduler configured
- ✅ News fetching automated
- ✅ Monitoring active
- ✅ Scheduler tests passing

---

## Day 5: Friday, Jan 31 - Integration Tests & Documentation

### Morning (3 hours)
- [ ] **Create integration test suite** (`tests/test_integration.py`)
  - Test fixtures (database, Redis, auth)
  - End-to-end test scenarios
  - Test data factories

- [ ] **Write integration tests**
  - [ ] User registration → login → API key → protected endpoint
  - [ ] News fetch → store → cache → retrieve → invalidate
  - [ ] OCR upload → process → cache → retrieve
  - [ ] Rate limit → 429 response → retry after timeout
  - [ ] Scheduled task execution
  - [ ] Database transaction rollback
  - [ ] Cache fallback when Redis down

### Afternoon (4 hours)
- [ ] **Run full test suite**
  ```bash
  pytest -v --cov=src --cov-report=html --cov-report=term
  ```

- [ ] **Fix failing tests**
  - Debug failures
  - Update test fixtures
  - Ensure all tests pass

- [ ] **Generate coverage report**
  - Target: 85% overall coverage
  - Identify gaps
  - Add missing tests

- [ ] **Update documentation**
  - Update CHANGELOG.md with v1.3.0
  - Update project status (75% → 80%)
  - Update roadmap
  - Document new features
  - Update testing.md

- [ ] **Commit and push**
  ```bash
  git add -A
  git commit -m "feat: Phase 2.6 complete - caching, rate limiting, optimization, scheduling"
  git push origin main
  ```

**End of Day Deliverables:**
- ✅ 20+ integration tests
- ✅ 85% test coverage
- ✅ All tests passing
- ✅ Documentation updated
- ✅ v1.3.0 released

---

## Success Criteria (Week 5)

### Performance
- [ ] API response time <50ms (p95)
- [ ] Cache hit rate >80%
- [ ] Database queries <50ms (p95)
- [ ] Zero N+1 queries

### Reliability
- [ ] Rate limiting enforced
- [ ] Scheduled tasks running reliably
- [ ] Graceful degradation if Redis fails
- [ ] 99.9% uptime target

### Quality
- [ ] 85% test coverage
- [ ] All integration tests passing
- [ ] Zero critical bugs
- [ ] Documentation complete

### Metrics
- [ ] Prometheus metrics for cache
- [ ] Prometheus metrics for rate limiting
- [ ] Job execution monitoring
- [ ] Performance benchmarks documented

---

## Testing Checklist

### Unit Tests (Existing + New)
- [ ] Cache service tests (10+)
- [ ] Rate limit tests (20+)
- [ ] Scheduler tests (10+)
- [ ] Database optimization tests (5+)

### Integration Tests (New)
- [ ] End-to-end authentication flow
- [ ] News ingestion pipeline
- [ ] OCR processing with caching
- [ ] Rate limiting behavior
- [ ] Scheduled task execution
- [ ] Cache invalidation
- [ ] Database transactions

### Performance Tests
- [ ] Load testing (100 concurrent users)
- [ ] Cache performance benchmarks
- [ ] Database query benchmarks
- [ ] API endpoint response times

---

## Files to Create/Modify

### New Files
1. `src/services/cache_service.py` (~200 lines)
2. `src/middleware/rate_limit.py` (~150 lines)
3. `src/middleware/cache.py` (~100 lines)
4. `src/services/scheduler_service.py` (~200 lines)
5. `tests/test_cache.py` (~150 lines)
6. `tests/test_rate_limit.py` (~200 lines)
7. `tests/test_scheduler.py` (~100 lines)
8. `tests/test_integration.py` (~300 lines)
9. `alembic/versions/002_performance_indexes.py` (~100 lines)

### Modified Files
1. `src/config.py` - Add Redis and cache settings
2. `src/main.py` - Integrate scheduler, cache middleware
3. `src/services/ocr_service.py` - Add caching
4. `src/api/v1/news.py` - Add caching
5. `requirements.txt` - Add new dependencies
6. `.env` - Add REDIS_URL
7. `CHANGELOG.md` - Add v1.3.0 section
8. `docs/project status.md` - Update to 80%
9. `docs/roadmap.md` - Mark Phase 2.6 complete

---

## Dependencies to Add

```bash
# Redis
redis==5.2.1
hiredis==3.0.0

# Task Scheduling
APScheduler==3.10.4

# Testing
pytest-timeout==2.2.0      # For timeout tests
pytest-benchmark==4.0.0    # For performance tests
faker==24.1.0              # For test data generation
```

---

## Configuration Updates

### .env additions
```bash
# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=50

# Cache settings
CACHE_OCR_TTL=3600          # 1 hour
CACHE_ARTICLES_TTL=300      # 5 minutes
CACHE_PREFERENCES_TTL=900   # 15 minutes

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_FREE_DAILY=100
RATE_LIMIT_BASIC_DAILY=1000
RATE_LIMIT_PREMIUM_DAILY=10000

# Scheduler
NEWS_FETCH_INTERVAL=15      # minutes
SCHEDULER_TIMEZONE=UTC
```

---

## Git Commit Strategy

### Daily Commits
- **Day 1:** `feat: Add Redis caching for OCR`
- **Day 2:** `feat: Add rate limiting middleware`
- **Day 3:** `perf: Add database indexes and optimize queries`
- **Day 4:** `feat: Add scheduled news fetching`
- **Day 5:** `test: Add integration tests and achieve 85% coverage`

### Final Commit
```bash
git commit -m "feat: v1.3.0 - Production hardening complete

Major updates:
- Redis caching (80% hit rate)
- Rate limiting enforcement
- Database optimization (<50ms queries)
- Scheduled news fetching
- Integration test suite (20+ tests)
- 85% test coverage

Performance improvements:
- API response time: 100ms → 50ms
- Cache hit rate: 0% → 80%
- Database queries optimized

Phase 2.6 complete: 75% → 80% overall progress"
```

---

## Quick Reference

### Start of Week Checklist
- [ ] Pull latest code: `git pull origin main`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Verify all services running (PostgreSQL, Redis)
- [ ] Run existing tests: `pytest -v`

### End of Week Checklist
- [ ] All tests passing
- [ ] Coverage report generated
- [ ] Documentation updated
- [ ] Code committed and pushed
- [ ] Performance benchmarks documented
- [ ] Ready for Phase 3.0

---

**Status:** Ready to start Week 5 🚀  
**Next Review:** Monday, Jan 27, 2026, 9:00 AM  
**Estimated Time:** 5 days (35 hours)
