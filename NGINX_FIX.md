# 🔧 Fix Errore 403 Forbidden - Static e Media Files

## Problema
```
Failed to load resource: the server responded with a status of 403 (Forbidden)
- manifest.json
- default.jpg
- icons/icon-192x192.png
- Immagini profilo
```

## Causa
Nginx non ha i permessi corretti per accedere alle directory `/static/` e `/media/`.

---

## ✅ Soluzione Completa

### 1. Verifica Percorsi sul Server

```bash
# Connettiti al server
ssh user@talkie.ovh

# Vai nella directory del progetto
cd /path/to/social  # Sostituisci con il percorso reale

# Verifica che esistano le directory
ls -la staticfiles/
ls -la media/
```

### 2. Esegui collectstatic

```bash
# Attiva virtual environment
source venv/bin/activate

# Raccogli tutti i file static
python manage.py collectstatic --noinput

# Verifica che i file siano stati copiati
ls -la staticfiles/manifest.json
ls -la staticfiles/icons/
ls -la media/profile_pics/default.jpg
```

### 3. Correggi i Permessi

```bash
# Dai ownership a www-data (utente nginx/gunicorn)
sudo chown -R www-data:www-data /path/to/social/staticfiles/
sudo chown -R www-data:www-data /path/to/social/media/

# Imposta permessi corretti
sudo chmod -R 755 /path/to/social/staticfiles/
sudo chmod -R 755 /path/to/social/media/

# Verifica
ls -la staticfiles/
ls -la media/
```

**Output atteso:**
```
drwxr-xr-x  www-data www-data  staticfiles/
drwxr-xr-x  www-data www-data  media/
```

### 4. Aggiorna Configurazione Nginx

Modifica `/etc/nginx/sites-available/talkie` (o il nome del tuo config file):

```nginx
server {
    listen 80;
    server_name talkie.ovh www.talkie.ovh;
    
    # Importante: aumenta dimensione upload
    client_max_body_size 20M;
    
    # STATIC FILES - PERCORSO ASSOLUTO
    location /static/ {
        alias /home/zion/social/staticfiles/;  # ⚠️ MODIFICA CON IL TUO PERCORSO
        autoindex off;
        expires 30d;
        add_header Cache-Control "public, immutable";
        
        # Permetti accesso a tutti i file
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|json|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # MEDIA FILES - PERCORSO ASSOLUTO
    location /media/ {
        alias /home/zion/social/media/;  # ⚠️ MODIFICA CON IL TUO PERCORSO
        autoindex off;
        expires 30d;
        add_header Cache-Control "public";
        
        # Permetti accesso a immagini
        location ~* \.(jpg|jpeg|png|gif|webp)$ {
            expires 1y;
            add_header Cache-Control "public";
        }
    }
    
    # WebSocket
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;  # Daphne
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    # Django app
    location / {
        proxy_pass http://127.0.0.1:8000;  # Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**⚠️ IMPORTANTE**: 
- Sostituisci `/home/zion/social/` con il percorso REALE del tuo progetto
- Il percorso deve finire con `/` (slash finale)
- Usa `alias` NON `root`

### 5. Testa e Riavvia Nginx

```bash
# Testa la configurazione
sudo nginx -t

# Se OK, riavvia
sudo systemctl restart nginx

# Verifica status
sudo systemctl status nginx
```

### 6. Verifica Accesso Diretto ai File

```bash
# Testa da browser o curl
curl -I https://talkie.ovh/static/manifest.json
curl -I https://talkie.ovh/media/profile_pics/default.jpg
curl -I https://talkie.ovh/static/icons/icon-192x192.png

# Dovrebbero rispondere con "200 OK" non "403 Forbidden"
```

---

## 🔍 Troubleshooting Avanzato

### Se ancora 403 dopo i fix sopra:

#### A. Verifica SELinux (se attivo)

```bash
# Controlla se SELinux è attivo
getenforce

# Se risponde "Enforcing", dai permessi:
sudo chcon -Rt httpd_sys_content_t /path/to/social/staticfiles/
sudo chcon -Rt httpd_sys_content_t /path/to/social/media/

# Oppure disabilita SELinux (NON consigliato in produzione)
sudo setenforce 0
```

#### B. Verifica AppArmor

```bash
# Controlla status
sudo aa-status

# Se nginx è in modalità enforce, metti in complain:
sudo aa-complain /etc/apparmor.d/usr.sbin.nginx
```

#### C. Controlla Logs Nginx

```bash
# Errori dettagliati
sudo tail -f /var/log/nginx/error.log

# Cerca linee tipo:
# "Permission denied" → problema permessi
# "No such file or directory" → percorso sbagliato
```

#### D. Verifica Percorsi in settings.py

```python
# /path/to/social/talkie/settings.py

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Stampa i percorsi per debug
print(f"STATIC_ROOT: {STATIC_ROOT}")
print(f"MEDIA_ROOT: {MEDIA_ROOT}")
```

---

## 📋 Checklist Finale

- [ ] `collectstatic` eseguito
- [ ] Directory `staticfiles/` e `media/` esistono
- [ ] Ownership: `www-data:www-data`
- [ ] Permessi: `755` (drwxr-xr-x)
- [ ] Nginx config: percorsi assoluti corretti
- [ ] Nginx config: `alias` con slash finale
- [ ] `nginx -t` passa senza errori
- [ ] Nginx riavviato
- [ ] File accessibili via curl/browser (200 OK)
- [ ] SELinux/AppArmor non bloccano

---

## 🎯 Quick Fix (Copia-Incolla)

```bash
# 1. Vai nel progetto
cd /path/to/social  # ⚠️ MODIFICA

# 2. Collectstatic
source venv/bin/activate
python manage.py collectstatic --noinput

# 3. Fix permessi
sudo chown -R www-data:www-data staticfiles/ media/
sudo chmod -R 755 staticfiles/ media/

# 4. Testa nginx
sudo nginx -t

# 5. Riavvia
sudo systemctl restart nginx

# 6. Verifica
curl -I https://talkie.ovh/static/manifest.json
```

---

## 💡 Nota su Tailwind CDN

L'errore:
```
cdn.tailwindcss.com should not be used in production
```

È un warning, non blocca il sito. Per risolverlo:

1. **Opzione A - Ignora** (funziona comunque)
2. **Opzione B - Installa Tailwind localmente**:
   ```bash
   npm install -D tailwindcss
   npx tailwindcss init
   # Configura build process
   ```

Per ora concentrati sul fix 403, il warning Tailwind è secondario.

---

**Dopo aver applicato questi fix, le immagini profilo e tutti i file static dovrebbero caricare correttamente! 🎉**
