# Vuva Deployment Guide

**Version**: 1.2.1  
**Last Updated**: January 24, 2026  
**Target Environment**: Production

## Overview

This guide covers deployment of the Vuva Newspaper Ingestion API to production environments. Includes configuration, security hardening, monitoring setup, and operational procedures.

## Prerequisites

### System Requirements

**Minimum**:
- CPU: 2 cores
- RAM: 4GB
- Disk: 20GB SSD
- OS: Linux (Ubuntu 22.04 LTS recommended)

**Recommended**:
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 50GB+ SSD
- OS: Ubuntu 22.04 LTS / Debian 12

### Software Dependencies

- Python 3.9+
- PostgreSQL 15+
- Redis 7+ (optional, for caching)
- Nginx (reverse proxy)
- Supervisor / Systemd (process management)

---

## 1. Server Setup

### Install System Packages

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.9 python3.9-venv python3.9-dev
sudo apt install -y build-essential libpq-dev

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Redis (optional)
sudo apt install -y redis-server

# Install Nginx
sudo apt install -y nginx

# Install Tesseract OCR
sudo apt install -y tesseract-ocr libtesseract-dev

# Install supervisor
sudo apt install -y supervisor

# Install git
sudo apt install -y git
```

### Create Application User

```bash
# Create dedicated user
sudo useradd -m -s /bin/bash vuva
sudo usermod -aG sudo vuva  # Optional: if user needs sudo

# Switch to vuva user
sudo su - vuva
```

---

## 2. Application Deployment

### Clone Repository

```bash
# As vuva user
cd /home/vuva
git clone https://github.com/your-org/vuva.git
cd vuva
```

### Python Environment

```bash
# Create virtual environment
python3.9 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install production-only dependencies
pip install gunicorn uvicorn[standard] python-multipart
```

### Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with production values
nano .env
```

**Production `.env`**:
```bash
# Application
APP_NAME="Vuva Production"
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=INFO

# Security
SECRET_KEY="<GENERATE-STRONG-32+-CHARACTER-KEY>"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL="postgresql+asyncpg://vuva_user:<PASSWORD>@localhost:5432/vuva_prod"

# Redis (optional)
REDIS_URL="redis://localhost:6379/0"

# CORS (restrict to your domains)
ALLOWED_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES="jpg,jpeg,png,pdf,tiff"

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

**Generate Strong Secret Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 3. Database Setup

### Create Production Database

```bash
# Switch to postgres user
sudo su - postgres

# Create database and user
psql << EOF
CREATE DATABASE vuva_prod;
CREATE USER vuva_user WITH ENCRYPTED PASSWORD '<STRONG_PASSWORD>';
GRANT ALL PRIVILEGES ON DATABASE vuva_prod TO vuva_user;
ALTER DATABASE vuva_prod OWNER TO vuva_user;
\q
EOF

# Exit postgres user
exit
```

### Configure PostgreSQL

Edit `/etc/postgresql/15/main/postgresql.conf`:
```conf
# Performance tuning
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 2621kB
min_wal_size = 1GB
max_wal_size = 4GB
max_connections = 100
```

Edit `/etc/postgresql/15/main/pg_hba.conf`:
```conf
# Local connections
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### Run Database Migrations

```bash
# As vuva user, in project directory
source venv/bin/activate

# Run Alembic migrations
alembic upgrade head

# Verify
psql -U vuva_user -d vuva_prod -h localhost -c "\dt"
```

---

## 4. Application Service

### Systemd Service Configuration

Create `/etc/systemd/system/vuva.service`:

```ini
[Unit]
Description=Vuva Newspaper Ingestion API
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=notify
User=vuva
Group=vuva
WorkingDirectory=/home/vuva/vuva
Environment="PATH=/home/vuva/vuva/venv/bin"
ExecStart=/home/vuva/vuva/venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 4 \
    -b 127.0.0.1:8000 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile /var/log/vuva/access.log \
    --error-logfile /var/log/vuva/error.log \
    --log-level info \
    src.main:app

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/vuva/vuva/logs /home/vuva/vuva/uploads

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
```

### Create Log Directories

```bash
sudo mkdir -p /var/log/vuva
sudo chown vuva:vuva /var/log/vuva

# Application uploads directory
mkdir -p /home/vuva/vuva/uploads
```

### Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable vuva

# Start service
sudo systemctl start vuva

# Check status
sudo systemctl status vuva

# View logs
sudo journalctl -u vuva -f
```

---

## 5. Nginx Configuration

### Create Nginx Configuration

Create `/etc/nginx/sites-available/vuva`:

```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=vuva_general:10m rate=60r/m;
limit_req_zone $binary_remote_addr zone=vuva_auth:10m rate=5r/m;

# Upstream application server
upstream vuva_backend {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Logging
    access_log /var/log/nginx/vuva_access.log;
    error_log /var/log/nginx/vuva_error.log;
    
    # Client body size (10MB for file uploads)
    client_max_body_size 10M;
    client_body_buffer_size 128k;
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # General rate limiting
    location / {
        limit_req zone=vuva_general burst=10 nodelay;
        
        proxy_pass http://vuva_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Stricter rate limiting for auth endpoints
    location /api/v1/auth/ {
        limit_req zone=vuva_auth burst=3 nodelay;
        
        proxy_pass http://vuva_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static files (if any)
    location /static/ {
        alias /home/vuva/vuva/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check endpoint (no rate limit)
    location /health {
        proxy_pass http://vuva_backend;
        access_log off;
    }
}
```

### Enable Site

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/vuva /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (certbot installs a timer automatically)
sudo systemctl status certbot.timer
```

---

## 6. Redis Setup (Optional)

### Configure Redis

Edit `/etc/redis/redis.conf`:
```conf
# Bind to localhost only
bind 127.0.0.1 ::1

# Enable persistence
save 900 1
save 300 10
save 60 10000

# Memory management
maxmemory 256mb
maxmemory-policy allkeys-lru

# Security
requirepass <STRONG_REDIS_PASSWORD>
```

Start Redis:
```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Update `.env`:
```bash
REDIS_URL="redis://:PASSWORD@localhost:6379/0"
```

---

## 7. Monitoring & Logging

### Structured Logging

Logs are written to:
- `/var/log/vuva/access.log` - HTTP access logs
- `/var/log/vuva/error.log` - Application errors
- `/var/log/nginx/vuva_access.log` - Nginx access logs
- `/var/log/nginx/vuva_error.log` - Nginx errors

### Log Rotation

Create `/etc/logrotate.d/vuva`:
```conf
/var/log/vuva/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 vuva vuva
    sharedscripts
    postrotate
        systemctl reload vuva
    endscript
}
```

### Health Monitoring

Use the health endpoint:
```bash
curl https://yourdomain.com/api/v1/health
```

Set up monitoring with:
- **Uptime Monitoring**: UptimeRobot, Pingdom
- **APM**: New Relic, Datadog
- **Error Tracking**: Sentry
- **Log Aggregation**: ELK Stack, Loki

---

## 8. Backup Strategy

### Database Backups

Create backup script `/home/vuva/backup_db.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/home/vuva/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vuva_prod_$TIMESTAMP.sql.gz"

mkdir -p $BACKUP_DIR

# Backup
PGPASSWORD='<PASSWORD>' pg_dump -U vuva_user -h localhost vuva_prod | gzip > $BACKUP_FILE

# Keep only last 30 days
find $BACKUP_DIR -name "vuva_prod_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
```

Make executable:
```bash
chmod +x /home/vuva/backup_db.sh
```

Create cron job:
```bash
crontab -e

# Daily backup at 2 AM
0 2 * * * /home/vuva/backup_db.sh >> /var/log/vuva/backup.log 2>&1
```

### File Backups

Backup uploads directory:
```bash
# Rsync to backup server
rsync -avz /home/vuva/vuva/uploads/ backup-server:/backups/vuva/uploads/
```

---

## 9. Security Hardening

### Firewall Configuration

```bash
# UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### SSH Hardening

Edit `/etc/ssh/sshd_config`:
```conf
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
X11Forwarding no
MaxAuthTries 3
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

### Fail2Ban

```bash
sudo apt install -y fail2ban

# Create jail
sudo nano /etc/fail2ban/jail.local
```

Add:
```ini
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/vuva_error.log
maxretry = 3
bantime = 600
```

Start Fail2Ban:
```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 10. Performance Optimization

### Gunicorn Workers

Calculate workers:
```python
# Formula: (2 x $num_cores) + 1
# For 4 cores: (2 x 4) + 1 = 9 workers
```

Update systemd service:
```ini
ExecStart=/home/vuva/vuva/venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 9 \
    ...
```

### Database Connection Pooling

In `.env`:
```bash
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### Nginx Caching

Add to nginx config:
```nginx
# Cache zone
proxy_cache_path /var/cache/nginx/vuva levels=1:2 keys_zone=vuva_cache:10m max_size=1g inactive=60m;

# In location block
proxy_cache vuva_cache;
proxy_cache_valid 200 5m;
proxy_cache_key "$scheme$request_method$host$request_uri";
```

---

## 11. Deployment Checklist

### Pre-Deployment

- [ ] Server provisioned and hardened
- [ ] Database created and migrated
- [ ] SSL certificates obtained
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Backup system configured

### Deployment

- [ ] Code deployed from git
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database migrations run
- [ ] Static files collected (if any)
- [ ] Systemd service created
- [ ] Nginx configured
- [ ] Service started and enabled

### Post-Deployment

- [ ] Health check passing
- [ ] API endpoints responding
- [ ] SSL working correctly
- [ ] Logs being written
- [ ] Monitoring active
- [ ] Backups running
- [ ] Performance acceptable
- [ ] Security scan passed

---

## 12. Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status vuva

# View logs
sudo journalctl -u vuva -n 100

# Check port binding
sudo netstat -tlnp | grep 8000

# Test manually
cd /home/vuva/vuva
source venv/bin/activate
python -m src.main
```

### Database Connection Issues

```bash
# Test connection
psql -U vuva_user -d vuva_prod -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Nginx 502 Bad Gateway

```bash
# Check upstream
curl http://127.0.0.1:8000/health

# Check Nginx error log
sudo tail -f /var/log/nginx/vuva_error.log

# Test Nginx config
sudo nginx -t
```

### High Memory Usage

```bash
# Check memory
free -h

# Check process memory
ps aux --sort=-%mem | head

# Reduce workers if needed
sudo systemctl edit vuva
```

---

## 13. Maintenance

### Update Application

```bash
# As vuva user
cd /home/vuva/vuva

# Pull latest code
git pull origin main

# Activate venv
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Restart service
sudo systemctl restart vuva
```

### Update System

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Reboot if kernel updated
sudo reboot
```

### Monitor Disk Usage

```bash
# Check disk space
df -h

# Find large files
du -ah /home/vuva | sort -h -r | head -n 20

# Clean old logs
sudo journalctl --vacuum-time=30d
```

---

## 14. Rollback Procedure

```bash
# Stop service
sudo systemctl stop vuva

# Rollback code
cd /home/vuva/vuva
git checkout <previous-commit-hash>

# Rollback database (if needed)
alembic downgrade -1

# Restart service
sudo systemctl start vuva

# Verify
curl https://yourdomain.com/health
```

---

## 15. Scaling

### Horizontal Scaling

1. **Load Balancer**: Use Nginx, HAProxy, or cloud load balancer
2. **Multiple App Servers**: Deploy on multiple servers
3. **Shared Database**: Point all servers to same PostgreSQL
4. **Shared Redis**: Centralized Redis for caching
5. **Shared Storage**: S3 or NFS for uploads

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Increase database resources
3. Add more Gunicorn workers
4. Optimize database queries

---

**Last Updated**: January 24, 2026  
**Version**: 1.2.1  
**Next Review**: February 24, 2026
