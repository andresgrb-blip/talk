# Installazione Redis su Windows

## Opzione 1: Docker (Consigliata)

### Prerequisiti
- Installa Docker Desktop: https://www.docker.com/products/docker-desktop/

### Avvio Redis
```bash
docker run -d --name redis-zone4love -p 6379:6379 redis
```

### Verifica
```bash
docker ps
redis-cli ping
```

### Comandi Utili
```bash
# Ferma Redis
docker stop redis-zone4love

# Avvia Redis
docker start redis-zone4love

# Rimuovi container
docker rm redis-zone4love
```

## Opzione 2: WSL2 (Windows Subsystem for Linux)

### Prerequisiti
1. Abilita WSL2: https://learn.microsoft.com/it-it/windows/wsl/install
2. Installa Ubuntu da Microsoft Store

### Installazione
```bash
# Apri WSL
wsl

# Installa Redis
sudo apt-get update
sudo apt-get install redis-server

# Avvia Redis
sudo service redis-server start

# Verifica
redis-cli ping
```

### Avvio Automatico
Aggiungi al file `~/.bashrc`:
```bash
sudo service redis-server start
```

## Opzione 3: Redis per Windows (Deprecata)

### Download
- https://github.com/microsoftarchive/redis/releases
- Scarica `Redis-x64-3.0.504.msi`

### Installazione
1. Esegui l'installer
2. Seleziona "Add to PATH"
3. Completa l'installazione

### Avvio
```bash
# Avvia Redis Server
redis-server

# In un altro terminale, verifica
redis-cli ping
```

## Verifica Connessione Django

Dopo aver avviato Redis, testa la connessione:

```bash
python manage.py shell
```

```python
from channels.layers import get_channel_layer
import asyncio

channel_layer = get_channel_layer()

async def test():
    await channel_layer.send('test_channel', {'type': 'test.message', 'text': 'Hello'})
    print("Redis funziona!")

asyncio.run(test())
```

## Troubleshooting

### Errore: "Connection refused"
- Verifica che Redis sia in esecuzione
- Controlla la porta 6379: `netstat -an | findstr 6379`

### Errore: "redis-cli not found"
- Aggiungi Redis al PATH di sistema
- Oppure usa il percorso completo: `C:\Program Files\Redis\redis-cli.exe`

### Performance su Windows
- Docker è più performante e stabile
- WSL2 è la seconda scelta migliore
- Redis nativo per Windows è deprecato ma funziona

## Configurazione Produzione

Per produzione su Windows Server, usa:
1. Redis in Docker con restart policy
2. Oppure Redis su Linux server separato
3. Configura firewall per porta 6379

```bash
# Docker con restart automatico
docker run -d --name redis-zone4love --restart unless-stopped -p 6379:6379 redis
```
