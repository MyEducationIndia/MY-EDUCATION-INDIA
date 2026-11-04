# MY EDUCATION INSTITUTE &bull; Production Deployment & DevOps Guide

This guide outlines deployment options for hosting **MY EDUCATION INSTITUTE** on dedicated virtual private servers (VPS), AWS EC2, DigitalOcean Droplets, or on-premise institute servers.

---

## 🐳 Option 1: Docker Compose Deployment (Recommended)

The project includes an optimized multi-stage `Dockerfile` and `docker-compose.yml` orchestrating the FastAPI application behind an Alpine Nginx reverse proxy.

### 1. Prerequisites
- Docker Engine 24.0+ & Docker Compose v2.0+

### 2. Deployment Steps
```bash
# 1. Clone repository or unzip production suite
cd my_education_erp

# 2. Configure production environment
cp .env.example .env
nano .env # Set your secret key and domain name

# 3. Build and launch containers
docker compose up -d --build

# 4. Initialize and seed database inside container
docker compose exec suite-web python3 -m app.db.init_db
docker compose exec suite-web python3 -m app.db.seed_data

# 5. Check container logs
docker compose logs -f suite-web
```

---

## 🐧 Option 2: Ubuntu 22.04 / 24.04 LTS Native Systemd Deployment

### 1. Install Base Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git curl
```

### 2. Configure Project Directory
```bash
sudo mkdir -p /var/www/my_education_erp
sudo chown -R $USER:$USER /var/www/my_education_erp
cd /var/www/my_education_erp

# Unzip project contents here
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
python3 -m app.db.init_db
python3 -m app.db.seed_data
```

### 3. Setup Systemd Service (`/etc/systemd/system/myeducationerp.service`)
```ini
[Unit]
Description=MY EDUCATION INSTITUTE Application Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/my_education_erp
Environment="PATH=/var/www/my_education_erp/venv/bin"
ExecStart=/var/www/my_education_erp/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable myeducationerp
sudo systemctl start myeducationerp
sudo systemctl status myeducationerp
```

### 4. Configure Nginx Reverse Proxy (`/etc/nginx/sites-available/myeducationerp`)
```nginx
server {
    listen 80;
    server_name myeducation.edu.in www.myeducation.edu.in;

    client_max_body_size 50M;

    # Gzip Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable Nginx site and obtain Free Let's Encrypt SSL:
```bash
sudo ln -s /etc/nginx/sites-available/myeducationerp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d myeducation.edu.in -d www.myeducation.edu.in
```

---

## 💾 Automated Database Backup Configuration (Cron)

Set up a daily automated database snapshot backup:
```bash
# Add to crontab (crontab -e)
0 2 * * * /usr/bin/python3 -c "import urllib.request; urllib.request.urlretrieve('http://127.0.0.1:8000/api/v1/settings/backup/json', '/var/backups/erp_backup_$(date +\%F).json')"
```
