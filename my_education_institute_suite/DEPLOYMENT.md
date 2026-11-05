# MY EDUCATION INSTITUTE &bull; Production Deployment & DevOps Guide

This guide outlines deployment options for hosting **MY EDUCATION INSTITUTE** on Render, Docker Compose with PostgreSQL, AWS EC2, DigitalOcean Droplets, or on-premise institute servers.

---

## 🚀 Option 1: Render Cloud Deployment with Managed PostgreSQL (Recommended)

The suite is natively configured for zero-config production deployment on Render via `render.yaml`.

### 1. Render Blueprint Deployment
1. Connect your Git repository to [Render Dashboard](https://dashboard.render.com).
2. Select **New** &rarr; **Blueprint** and point to your repository.
3. Render automatically provisions:
   - **PostgreSQL Database** (`my-education-postgres`) with auto-generated connection string.
   - **FastAPI Web Service** (`my-education-institute`) with Python 3.11 runtime.
4. Render automatically executes the build command:
   ```bash
   pip install -r requirements.txt && alembic upgrade head
   ```
5. The `DATABASE_URL` environment variable is automatically linked from the PostgreSQL database to the web service.

---

## 🐳 Option 2: Docker Compose Deployment (PostgreSQL + FastAPI + Nginx)

The project includes an optimized multi-stage `Dockerfile` and `docker-compose.yml` orchestrating the FastAPI application, PostgreSQL 15 database, and Alpine Nginx reverse proxy.

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

# 4. Run database migrations and initial seed
docker compose exec suite-web alembic upgrade head
docker compose exec suite-web python3 -m app.db.seed_data

# 5. Check container logs
docker compose logs -f suite-web
```

---

## 🐧 Option 3: Ubuntu 22.04 / 24.04 LTS Native Systemd Deployment with PostgreSQL

### 1. Install Base Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib libpq-dev nginx certbot python3-certbot-nginx git curl
```

### 2. Configure PostgreSQL Database
```bash
sudo -u postgres psql -c "CREATE DATABASE my_education;"
sudo -u postgres psql -c "CREATE USER my_education_user WITH ENCRYPTED PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE my_education TO my_education_user;"
sudo -u postgres psql -d my_education -c "GRANT ALL ON SCHEMA public TO my_education_user;"
```

### 3. Configure Project Directory
```bash
sudo mkdir -p /var/www/my_education_erp
sudo chown -R $USER:$USER /var/www/my_education_erp
cd /var/www/my_education_erp

# Unzip project contents here
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cat << 'EOF' > .env
PROJECT_NAME="MY EDUCATION INSTITUTE"
ENVIRONMENT="production"
SECRET_KEY="replace-with-a-secure-random-64-character-hex-key"
DATABASE_URL="postgresql+psycopg2://my_education_user:your_secure_password@localhost:5432/my_education"
EOF

# Run database migrations and seed data
alembic upgrade head
python3 -m app.db.seed_data
```

### 4. Setup Systemd Service (`/etc/systemd/system/myeducationerp.service`)
```ini
[Unit]
Description=MY EDUCATION INSTITUTE Application Server
After=network.target postgresql.service

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

### 5. Configure Nginx Reverse Proxy (`/etc/nginx/sites-available/myeducationerp`)
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

## 💾 Automated PostgreSQL Database Backup (Cron)

Set up a daily automated database snapshot backup:
```bash
# Add to crontab (crontab -e)
0 2 * * * pg_dump -U my_education_user -h localhost my_education | gzip > /var/backups/erp_pg_backup_$(date +\%F).sql.gz
```
