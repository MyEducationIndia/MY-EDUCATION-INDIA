# MY EDUCATION INDIA ERP V2 — LINUX PRODUCTION DEPLOYMENT GUIDE

## 1. Host Architecture
- **Operating System**: Ubuntu 22.04 LTS / Debian 12
- **Reverse Proxy**: Nginx with HTTP/2 and TLS 1.3
- **Process Manager**: Systemd / Gunicorn with Uvicorn worker class

## 2. Systemd Service Configuration
Create `/etc/systemd/system/myeducation-backend.service`:
```ini
[Unit]
Description=MY EDUCATION INDIA ERP V2 Backend Service
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/my-education-india/backend
EnvironmentFile=/var/www/my-education-india/.env
ExecStart=/var/www/my-education-india/backend/venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    --access-logfile /var/log/myeducation/access.log \
    --error-logfile /var/log/myeducation/error.log
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 3. Nginx Reverse Proxy & Security Headers
Configure `/etc/nginx/sites-available/myeducation.conf`:
```nginx
server {
    listen 80;
    server_name myeducation.in api.myeducation.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.myeducation.in;

    ssl_certificate /etc/letsencrypt/live/myeducation.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myeducation.in/privkey.pem;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self';" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
