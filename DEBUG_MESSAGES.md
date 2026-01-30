# 🐛 Debug: Messaggi Non Si Inviano

## Informazioni Necessarie

Per capire il problema, ho bisogno di sapere:

### 1. **Dove non funzionano i messaggi?**
- [ ] Chat privata (`/chat/<room_name>/`)
- [ ] Random Chat (`/random/`)
- [ ] Entrambi

### 2. **Cosa succede quando provi a inviare?**
- [ ] Il messaggio scompare ma non arriva
- [ ] Il form non si invia
- [ ] Errore visibile nella pagina
- [ ] Nessuna reazione

### 3. **Errori nella Console Browser** (IMPORTANTE)

Apri la console del browser (F12 → Console) e cerca errori:

```
Possibili errori:
- WebSocket connection failed
- 403 Forbidden
- 500 Internal Server Error
- Mixed Content (http/https)
```

**Copia e inviami gli errori dalla console!**

---

## 🔍 Diagnosi Sul Server

Esegui questi comandi sul server per verificare:

### A. Verifica Daphne (WebSocket server)

```bash
# È in esecuzione?
systemctl status talkie-daphne
# o
ps aux | grep daphne

# Logs
journalctl -u talkie-daphne -n 50
```

**Output atteso:** Daphne deve essere "active (running)"

### B. Verifica Redis (message broker)

```bash
# È in esecuzione?
systemctl status redis
# o
redis-cli ping
# Deve rispondere "PONG"
```

### C. Verifica Nginx Config per WebSocket

```bash
cat /etc/nginx/sites-enabled/talkie | grep -A 10 "location /ws"
```

**Deve avere:**
```nginx
location /ws/ {
    proxy_pass http://127.0.0.1:8001;  # Daphne
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### D. Test WebSocket Diretto

```bash
# Installa wscat se non ce l'hai
npm install -g wscat

# Testa connessione WebSocket
wscat -c ws://localhost:8001/ws/chat/test/
# Oppure
wscat -c wss://talkie.ovh/ws/chat/test/
```

---

## 🚨 Problemi Comuni e Fix

### Problema 1: Daphne Non Avviato

```bash
# Avvia Daphne
systemctl start talkie-daphne
systemctl enable talkie-daphne

# Verifica
systemctl status talkie-daphne
```

### Problema 2: Redis Non Funziona

```bash
# Avvia Redis
systemctl start redis
systemctl enable redis

# Test
redis-cli ping
```

### Problema 3: Nginx Non Inoltra WebSocket

Verifica che nginx config abbia:

```nginx
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
```

Poi:
```bash
nginx -t
systemctl restart nginx
```

### Problema 4: Mixed Content (HTTP/HTTPS)

Se il sito è HTTPS ma WebSocket usa WS (non WSS), il browser blocca.

**Verifica in console browser:**
```
Mixed Content: The page at 'https://talkie.ovh' was loaded over HTTPS,
but attempted to connect to 'ws://talkie.ovh/ws/...'
```

**Fix:** Assicurati che il JavaScript usi `wss://` per HTTPS:

```javascript
const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(wsScheme + '://' + window.location.host + '/ws/...');
```

### Problema 5: CSRF Token Mancante

Se i messaggi POST falliscono con 403:

```bash
# Verifica settings.py
grep CSRF_TRUSTED_ORIGINS /opt/talkie/app/talkie/settings.py
```

Deve includere:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://talkie.ovh',
    'http://talkie.ovh',
]
```

---

## 🧪 Script di Test Completo

```bash
#!/bin/bash
echo "=== TEST MESSAGGI TALKIE ==="
echo ""

echo "1. DAPHNE STATUS:"
systemctl status talkie-daphne --no-pager | head -5
echo ""

echo "2. REDIS STATUS:"
redis-cli ping 2>&1
echo ""

echo "3. NGINX WEBSOCKET CONFIG:"
grep -A 10 "location /ws" /etc/nginx/sites-enabled/talkie
echo ""

echo "4. DAPHNE LOGS (ultimi 20):"
journalctl -u talkie-daphne -n 20 --no-pager
echo ""

echo "5. GUNICORN LOGS (ultimi 20):"
journalctl -u talkie -n 20 --no-pager
echo ""

echo "=== FINE TEST ==="
```

Salva come `test_messages.sh` ed esegui:
```bash
bash test_messages.sh > debug_output.txt
cat debug_output.txt
```

---

## 📋 Checklist Debug

- [ ] Daphne è in esecuzione (`systemctl status talkie-daphne`)
- [ ] Redis risponde PONG (`redis-cli ping`)
- [ ] Nginx config ha location /ws/ corretto
- [ ] WebSocket usa wss:// su HTTPS
- [ ] Console browser non mostra errori WebSocket
- [ ] CSRF_TRUSTED_ORIGINS include il dominio
- [ ] Logs Daphne non mostrano errori

---

## 🎯 Prossimi Step

1. **Inviami:**
   - Errori dalla console browser (F12)
   - Output di `systemctl status talkie-daphne`
   - Output di `redis-cli ping`
   - Screenshot del problema (opzionale)

2. **Esegui sul server:**
   ```bash
   systemctl status talkie-daphne
   redis-cli ping
   journalctl -u talkie-daphne -n 50
   ```

Con queste info posso darti la soluzione esatta! 🚀
