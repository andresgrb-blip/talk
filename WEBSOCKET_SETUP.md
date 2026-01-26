# Configurazione WebSocket per Zone4Love

## Prerequisiti

### 1. Installa Redis
Redis è necessario per gestire i canali WebSocket.

**Windows:**
- Scarica Redis da: https://github.com/microsoftarchive/redis/releases
- Oppure usa WSL2 e installa Redis con: `sudo apt-get install redis-server`
- Oppure usa Docker: `docker run -d -p 6379:6379 redis`

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Mac
brew install redis
brew services start redis
```

### 2. Verifica che Redis sia in esecuzione
```bash
redis-cli ping
# Dovrebbe rispondere: PONG
```

## Installazione Dipendenze

```bash
pip install -r requirements.txt
```

Le nuove dipendenze includono:
- `channels==4.0.0` - Django Channels per WebSocket
- `channels-redis==4.1.0` - Backend Redis per Channels
- `daphne==4.0.0` - Server ASGI

## Migrazioni Database

Esegui le migrazioni per creare le tabelle ChatRoom e Message:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Avvio del Server

Invece di `python manage.py runserver`, usa Daphne (server ASGI):

```bash
daphne -b 0.0.0.0 -p 8000 zone4love.asgi:application
```

Oppure continua a usare runserver (supporta ASGI automaticamente):

```bash
python manage.py runserver
```

## Funzionalità WebSocket Implementate

### 1. **Notifiche Real-Time**
- Connessione: `ws://localhost:8000/ws/notifications/`
- Ricevi notifiche istantanee per:
  - Nuovi like sui tuoi post
  - Nuovi commenti
  - Nuovi follower
- Toast notification automatico nell'interfaccia
- Badge contatore notifiche non lette

### 2. **Chat/Messaggistica Privata**
- Connessione: `ws://localhost:8000/ws/chat/<room_name>/`
- Chat 1-a-1 tra utenti
- Messaggi in tempo reale
- Storico conversazioni
- Interfaccia moderna tipo WhatsApp

## Test WebSocket

### Test Notifiche
1. Apri due browser/tab
2. Login con due utenti diversi
3. Utente A mette like a un post di Utente B
4. Utente B riceve notifica istantanea

### Test Chat
1. Vai al profilo di un utente
2. Clicca "Messaggio"
3. Scrivi un messaggio
4. L'altro utente riceve il messaggio in tempo reale

## Troubleshooting

### Redis non si connette
```
Error: connection to server at "localhost" (::1), port 6379 failed
```

**Soluzione:**
- Verifica che Redis sia in esecuzione: `redis-cli ping`
- Su Windows, avvia Redis manualmente o usa Docker

### WebSocket si disconnette
```
WebSocket connection closed
```

**Soluzione:**
- Verifica che il server sia avviato con Daphne o Django 5.0+
- Controlla che ASGI_APPLICATION sia configurato correttamente
- Verifica i log del server

### Errore CHANNEL_LAYERS
```
ImproperlyConfigured: Cannot find 'default' in CHANNEL_LAYERS
```

**Soluzione:**
- Verifica che `channels` e `channels-redis` siano installati
- Controlla la configurazione in `settings.py`

## Configurazione Produzione

Per produzione, usa un server ASGI production-ready:

```bash
# Installa
pip install uvicorn

# Avvia
uvicorn zone4love.asgi:application --host 0.0.0.0 --port 8000
```

Oppure con Daphne:

```bash
daphne -b 0.0.0.0 -p 8000 zone4love.asgi:application
```

### Nginx Configuration (Produzione)

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://django;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://django;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Architettura WebSocket

```
Client Browser
    ↓ WebSocket
ASGI Server (Daphne/Uvicorn)
    ↓
Django Channels
    ↓
Redis Channel Layer
    ↓
Consumers (NotificationConsumer, ChatConsumer)
    ↓
Database (PostgreSQL)
```

## API WebSocket

### Notifiche
**Connessione:**
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');
```

**Messaggi ricevuti:**
```json
{
    "type": "notification",
    "notification": {
        "id": 1,
        "type": "like",
        "sender": "username",
        "sender_id": 2,
        "message": "username ha messo mi piace al tuo post",
        "created_at": "2026-01-17T10:00:00Z"
    }
}
```

### Chat
**Connessione:**
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/chat/room_name/');
```

**Invia messaggio:**
```json
{
    "message": "Ciao!"
}
```

**Ricevi messaggio:**
```json
{
    "type": "message",
    "message": "Ciao!",
    "username": "sender_username",
    "user_id": 2
}
```

## Performance

- Redis gestisce migliaia di connessioni simultanee
- Ogni utente ha un canale dedicato per le notifiche
- Le chat room sono isolate per privacy
- Messaggi persistiti nel database PostgreSQL

## Sicurezza

- Autenticazione richiesta per tutte le connessioni WebSocket
- Middleware di autenticazione Django integrato
- CSRF protection mantenuto per richieste HTTP
- AllowedHostsOriginValidator per validare origini WebSocket
