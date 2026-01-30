# 🚨 FIX RAPIDO 403 - Esegui Questi Comandi

## Step 1: Diagnosi
```bash
# Connettiti al server
ssh user@talkie.ovh

# Vai nella directory del progetto
cd ~/social  # o il percorso dove hai il progetto

# Esegui diagnosi
bash diagnose_403.sh

# COPIA TUTTO L'OUTPUT E INVIAMELO
```

---

## Step 2: Fix Immediato (prova questi in ordine)

### A. Verifica che i file esistano
```bash
cd ~/social
ls -la staticfiles/manifest.json
ls -la media/profile_pics/default.jpg
ls -la staticfiles/icons/

# Se NON esistono, esegui collectstatic:
source venv/bin/activate
python manage.py collectstatic --noinput
```

### B. Fix Permessi (più aggressivo)
```bash
# Dai permessi a TUTTI
sudo chmod -R 755 ~/social/staticfiles/
sudo chmod -R 755 ~/social/media/

# Cambia owner
sudo chown -R $USER:www-data ~/social/staticfiles/
sudo chown -R $USER:www-data ~/social/media/

# Verifica
ls -la staticfiles/
ls -la media/
```

### C. Verifica Config Nginx
```bash
# Mostra config attuale
cat /etc/nginx/sites-enabled/talkie

# Cerca queste righe e INVIAMELE:
# location /static/ {
#     alias ...
# }
```

### D. Test Diretto
```bash
# Prova ad accedere ai file direttamente
curl -I http://localhost/static/manifest.json
curl -I http://localhost/media/profile_pics/default.jpg

# Dovrebbero dare 200 OK, non 403
```

---

## Step 3: Fix Config Nginx (se ancora 403)

### Opzione 1: Config Semplificata
```nginx
server {
    listen 80;
    server_name talkie.ovh;
    
    root /home/TUOUSERNAME/social;  # ⚠️ CAMBIA TUOUSERNAME
    
    location /static {
        alias /home/TUOUSERNAME/social/staticfiles;  # ⚠️ CAMBIA
        try_files $uri $uri/ =404;
    }
    
    location /media {
        alias /home/TUOUSERNAME/social/media;  # ⚠️ CAMBIA
        try_files $uri $uri/ =404;
    }
    
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Applica:
```bash
# Modifica config
sudo nano /etc/nginx/sites-enabled/talkie

# Testa
sudo nginx -t

# Se OK, riavvia
sudo systemctl restart nginx
```

---

## Step 4: Se ANCORA 403 - Disabilita SELinux temporaneamente

```bash
# Controlla se SELinux è attivo
getenforce

# Se risponde "Enforcing", disabilita temporaneamente:
sudo setenforce 0

# Riprova ad accedere ai file
curl -I https://talkie.ovh/static/manifest.json

# Se ORA funziona, il problema è SELinux. Fix permanente:
sudo chcon -Rt httpd_sys_content_t ~/social/staticfiles/
sudo chcon -Rt httpd_sys_content_t ~/social/media/
sudo setenforce 1
```

---

## Step 5: Logs per Debug

```bash
# Guarda gli errori in tempo reale
sudo tail -f /var/log/nginx/error.log

# In un altro terminale, prova ad accedere:
curl https://talkie.ovh/static/manifest.json

# Cosa dice il log?
# - "Permission denied" → problema permessi
# - "No such file" → percorso sbagliato
# - "13: Permission denied" → SELinux
```

---

## 🎯 Soluzione Alternativa: Symlink

Se niente funziona, prova con symlink:

```bash
# Crea directory in /var/www (nginx ha sempre accesso)
sudo mkdir -p /var/www/talkie/static
sudo mkdir -p /var/www/talkie/media

# Copia i file
sudo cp -r ~/social/staticfiles/* /var/www/talkie/static/
sudo cp -r ~/social/media/* /var/www/talkie/media/

# Permessi
sudo chown -R www-data:www-data /var/www/talkie/
sudo chmod -R 755 /var/www/talkie/

# Aggiorna nginx config:
# location /static/ {
#     alias /var/www/talkie/static/;
# }
# location /media/ {
#     alias /var/www/talkie/media/;
# }

sudo systemctl restart nginx
```

---

## 📞 Inviami Questi Output

Per aiutarti meglio, inviami:

1. Output di `bash diagnose_403.sh`
2. Output di `cat /etc/nginx/sites-enabled/talkie`
3. Output di `ls -la ~/social/staticfiles/`
4. Output di `sudo tail -20 /var/log/nginx/error.log`
5. Il tuo username sul server (comando `whoami`)

Con questi dati posso darti la soluzione esatta! 🎯
