# 🚀 Guida al Deployment - Zone4Love

Questa guida ti aiuterà a mettere in produzione il social network Zone4Love.

## 📋 Prerequisiti

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Server Linux (Ubuntu 22.04 consigliato) o Windows Server
- Dominio configurato (opzionale ma consigliato)

## 🔧 Setup Produzione

### 1. Clona il Repository

```bash
git clone <your-repo-url>
cd social
```

### 2. Crea Ambiente Virtuale

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows
```

### 3. Installa Dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura Variabili d'Ambiente

Copia `.env.example` in `.env` e modifica i valori:

```bash
cp .env.example .env
```

Modifica `.env`:

```env
SECRET_KEY=genera-una-chiave-segreta-sicura-qui
DEBUG=False
ALLOWED_HOSTS=tuodominio.com,www.tuodominio.com

DB_NAME=zone4love_production
DB_USER=zone4love_user
DB_PASSWORD=password-sicura-qui
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
```

**Genera una SECRET_KEY sicura:**

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Setup Database PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE zone4love_production;
CREATE USER zone4love_user WITH PASSWORD 'password-sicura-qui';
ALTER ROLE zone4love_user SET client_encoding TO 'utf8';
ALTER ROLE zone4love_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE zone4love_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE zone4love_production TO zone4love_user;
\q
```

### 6. Setup Redis

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Verifica
redis-cli ping  # Dovrebbe rispondere "PONG"
```

### 7. Migrazioni Database

```bash
python manage.py migrate
python manage.py create_achievements  # Crea achievement predefiniti
python manage.py createsuperuser  # Crea admin
```

### 8. Raccogli File Statici

```bash
python manage.py collectstatic --noinput
```

### 9. Crea Directory per Logs

```bash
mkdir logs
touch logs/django_errors.log
```

## 🌐 Deployment con Gunicorn + Nginx

### 1. Installa Nginx

```bash
sudo apt install nginx
```

### 2. Configura Gunicorn

Crea file `gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
```

### 3. Crea Systemd Service per Gunicorn

File: `/etc/systemd/system/zone4love.service`

```ini
[Unit]
Description=Zone4Love Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/social
Environment="PATH=/path/to/social/venv/bin"
ExecStart=/path/to/social/venv/bin/gunicorn --config gunicorn_config.py zone4love.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4. Crea Systemd Service per Daphne (WebSockets)

File: `/etc/systemd/system/zone4love-daphne.service`

```ini
[Unit]
Description=Zone4Love Daphne daemon (WebSockets)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/social
Environment="PATH=/path/to/social/venv/bin"
ExecStart=/path/to/social/venv/bin/daphne -b 127.0.0.1 -p 8001 zone4love.asgi:application

[Install]
WantedBy=multi-user.target
```

### 5. Configura Nginx

File: `/etc/nginx/sites-available/zone4love`

```nginx
upstream django {
    server 127.0.0.1:8000;
}

upstream daphne {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name tuodominio.com www.tuodominio.com;
    
    client_max_body_size 20M;
    
    location /static/ {
        alias /path/to/social/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /path/to/social/media/;
        expires 30d;
    }
    
    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Abilita il sito:

```bash
sudo ln -s /etc/nginx/sites-available/zone4love /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Avvia i Servizi

```bash
sudo systemctl start zone4love
sudo systemctl start zone4love-daphne
sudo systemctl enable zone4love
sudo systemctl enable zone4love-daphne

# Verifica status
sudo systemctl status zone4love
sudo systemctl status zone4love-daphne
```

## 🔒 SSL/HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tuodominio.com -d www.tuodominio.com
```

Dopo aver ottenuto il certificato, aggiorna `.env`:

```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

E riavvia:

```bash
sudo systemctl restart zone4love
```

## 📊 Monitoraggio

### Logs

```bash
# Django errors
tail -f logs/django_errors.log

# Gunicorn
tail -f logs/gunicorn_error.log

# Nginx
tail -f /var/log/nginx/error.log

# Systemd
sudo journalctl -u zone4love -f
sudo journalctl -u zone4love-daphne -f
```

### Database Backup

```bash
# Backup
pg_dump -U zone4love_user zone4love_production > backup_$(date +%Y%m%d).sql

# Restore
psql -U zone4love_user zone4love_production < backup_20260118.sql
```

## 🔄 Aggiornamenti

```bash
# Pull nuove modifiche
git pull origin main

# Aggiorna dipendenze
pip install -r requirements.txt

# Migrazioni
python manage.py migrate

# Raccogli static files
python manage.py collectstatic --noinput

# Riavvia servizi
sudo systemctl restart zone4love
sudo systemctl restart zone4love-daphne
```

## ⚡ Performance Tips

1. **Database Connection Pooling**: Usa `pgbouncer`
2. **Caching**: Configura Redis per cache Django
3. **CDN**: Usa Cloudflare o AWS CloudFront per static/media files
4. **Monitoring**: Installa Sentry per error tracking

## 🐛 Troubleshooting

### WebSocket non funzionano

```bash
# Verifica Redis
redis-cli ping

# Verifica Daphne
sudo systemctl status zone4love-daphne
sudo journalctl -u zone4love-daphne -n 50
```

### Static files non caricano

```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database connection errors

```bash
# Verifica PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -c "\l"
```

## 📞 Supporto

Per problemi o domande, consulta la documentazione Django:
- https://docs.djangoproject.com/en/5.0/howto/deployment/
- https://channels.readthedocs.io/en/stable/deploying.html

---

**Zone4Love** - Social Network Rivoluzionario 💕
