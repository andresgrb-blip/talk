# 🔧 Fix WebSocket Failed Connection

## Problema
```
WebSocket connection to 'wss://talkie.ovh/ws/notifications/' failed
```

Questo significa che Daphne (il server WebSocket) non risponde o nginx non inoltra correttamente.

---

## 🚨 Diagnosi Rapida

Esegui sul server:

```bash
# 1. Daphne è attivo?
systemctl status talkie-daphne

# 2. Daphne ascolta sulla porta 8001?
netstat -tlnp | grep 8001

# 3. Redis funziona?
redis-cli ping

# 4. Test diretto a Daphne
curl -I http://127.0.0.1:8001/
```

---

## ✅ Soluzione Step-by-Step

### Step 1: Verifica/Avvia Daphne

```bash
# Controlla status
systemctl status talkie-daphne

# Se non esiste il servizio, crealo:
sudo nano /etc/systemd/system/talkie-daphne.service
```

**Contenuto del file:**
```ini
[Unit]
Description=Talkie Daphne WebSocket Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/talkie/app
Environment="PATH=/opt/talkie/app/venv/bin"
ExecStart=/opt/talkie/app/venv/bin/daphne -b 127.0.0.1 -p 8001 talkie.asgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Poi:**
```bash
# Ricarica systemd
systemctl daemon-reload

# Avvia Daphne
systemctl start talkie-daphne
systemctl enable talkie-daphne

# Verifica
systemctl status talkie-daphne
```

### Step 2: Verifica Nginx Config per HTTPS

```bash
# Apri config nginx
nano /etc/nginx/sites-enabled/talkie
```

**Deve avere ENTRAMBI i blocchi server (HTTP e HTTPS):**

```nginx
# HTTP (redirect to HTTPS)
server {
    listen 80;
    server_name talkie.ovh www.talkie.ovh;
    return 301 https://$server_name$request_uri;
}

# HTTPS (main config)
server {
    listen 443 ssl http2;
    server_name talkie.ovh www.talkie.ovh;
    
    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/talkie.ovh/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/talkie.ovh/privkey.pem;
    
    client_max_body_size 20M;
    
    # STATIC FILES
    location /static/ {
        alias /opt/talkie/app/staticfiles/;
        expires 30d;
    }
    
    # MEDIA FILES
    location /media/ {
        alias /opt/talkie/app/media/;
        expires 30d;
    }
    
    # WEBSOCKET - IMPORTANTE!
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    # DJANGO APP
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Salva e testa:**
```bash
nginx -t
systemctl restart nginx
```

### Step 3: Verifica Redis

```bash
# Avvia Redis se non attivo
systemctl start redis
systemctl enable redis

# Test
redis-cli ping
# Deve rispondere: PONG
```

### Step 4: Verifica Logs

```bash
# Logs Daphne
journalctl -u talkie-daphne -f

# In un altro terminale, ricarica la pagina e guarda i logs
# Dovresti vedere connessioni WebSocket
```

---

## 🧪 Test Finale

### Test 1: Connessione Locale
```bash
# Sul server
curl -I http://127.0.0.1:8001/

# Deve rispondere (anche se 404 va bene)
```

### Test 2: WebSocket da Browser
1. Apri https://talkie.ovh
2. F12 → Console
3. Ricarica pagina
4. Cerca: `WebSocket connection to 'wss://talkie.ovh/ws/notifications/' succeeded`

### Test 3: Invia Messaggio
1. Vai in una chat
2. Invia messaggio
3. Deve arrivare in tempo reale

---

## 🔍 Troubleshooting Avanzato

### Problema: Daphne non si avvia

```bash
# Testa manualmente
cd /opt/talkie/app
source venv/bin/activate
daphne -b 127.0.0.1 -p 8001 talkie.asgi:application

# Guarda gli errori
# Possibili cause:
# - Porta 8001 già in uso
# - Errore in asgi.py
# - Redis non raggiungibile
```

### Problema: Nginx 502 Bad Gateway

```bash
# Verifica che Daphne sia in ascolto
netstat -tlnp | grep 8001

# Deve mostrare:
# tcp  0  0  127.0.0.1:8001  0.0.0.0:*  LISTEN  <pid>/python
```

### Problema: WebSocket si connette ma si disconnette subito

```bash
# Controlla ALLOWED_HOSTS in settings.py
grep ALLOWED_HOSTS /opt/talkie/app/talkie/settings.py

# Deve includere:
ALLOWED_HOSTS = ['talkie.ovh', 'www.talkie.ovh', 'localhost']
```

---

## 📋 Checklist Completa

- [ ] Daphne service creato in `/etc/systemd/system/talkie-daphne.service`
- [ ] Daphne attivo: `systemctl status talkie-daphne` → active (running)
- [ ] Porta 8001 in ascolto: `netstat -tlnp | grep 8001`
- [ ] Redis attivo: `redis-cli ping` → PONG
- [ ] Nginx ha blocco `location /ws/` nel server HTTPS (porta 443)
- [ ] Nginx config testata: `nginx -t` → OK
- [ ] Nginx riavviato: `systemctl restart nginx`
- [ ] Browser console: WebSocket connection succeeded
- [ ] Messaggi si inviano in tempo reale

---

## 🚀 Script Automatico

Esegui sul server:

```bash
bash FIX_WEBSOCKET.sh > websocket_debug.txt
cat websocket_debug.txt
```

Inviami l'output per diagnosi precisa.

---

**Una volta completata la checklist, WebSocket funzionerà! 🎉**
