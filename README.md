# Zone4Love - Social Network

Un social network moderno costruito con Django, PostgreSQL e TailwindCSS.

## 🚀 Funzionalità

- **Autenticazione utente**: Registrazione, login e logout
- **Profili utente**: Profili personalizzabili con foto profilo, foto copertina, bio e informazioni personali
- **Post**: Crea, visualizza ed elimina post con supporto per immagini
- **Interazioni sociali**:
  - Like sui post
  - Commenti sui post
  - Sistema di follow/unfollow
- **Feed personalizzato**: Visualizza i post delle persone che segui
- **Esplora**: Scopri nuovi contenuti da tutti gli utenti
- **Notifiche Real-Time**: Ricevi notifiche istantanee via WebSocket per like, commenti e nuovi follower
- **Chat/Messaggistica**: Sistema di chat privata 1-a-1 con WebSocket
- **Ricerca**: Cerca utenti e post
- **Design responsive**: Interfaccia moderna con TailwindCSS

## 📋 Prerequisiti

- Python 3.10+
- PostgreSQL 12+
- Redis 6.0+ (per WebSocket)
- pip

## 🛠️ Installazione

### 1. Clona il repository

```bash
cd c:\Users\andre\Desktop\social
```

### 2. Crea un ambiente virtuale

```bash
python -m venv venv
venv\Scripts\activate  # Su Windows
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Installa e avvia Redis

**Windows:**
```bash
# Opzione 1: Docker
docker run -d -p 6379:6379 redis

# Opzione 2: WSL2
wsl
sudo apt-get install redis-server
sudo service redis-server start
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Mac:**
```bash
brew install redis
brew services start redis
```

Verifica che Redis funzioni:
```bash
redis-cli ping
# Dovrebbe rispondere: PONG
```

### 5. Configura PostgreSQL

Crea un database PostgreSQL:

```sql
CREATE DATABASE zone4love_db;
CREATE USER postgres WITH PASSWORD 'your_password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE zone4love_db TO postgres;
```

### 6. Configura le variabili d'ambiente

Copia il file `.env.example` in `.env` e modifica i valori:

```bash
copy .env.example .env
```

Modifica il file `.env` con le tue credenziali:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=zone4love_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 7. Esegui le migrazioni

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Crea un superutente

```bash
python manage.py createsuperuser
```

### 9. Crea le cartelle per i media e l'immagine default

```bash
python setup_media.py
python create_default_image.py
```

### 10. Avvia il server

```bash
python manage.py runserver
```

Oppure usa Daphne per migliori performance WebSocket:
```bash
daphne -b 0.0.0.0 -p 8000 zone4love.asgi:application
```

Visita http://localhost:8000 nel tuo browser!

**Nota:** Per le funzionalità WebSocket (notifiche real-time e chat), assicurati che Redis sia in esecuzione.

## 📁 Struttura del Progetto

```
social/
├── zone4love/              # Configurazione principale del progetto
│   ├── settings.py         # Impostazioni Django
│   ├── urls.py            # URL principali
│   └── wsgi.py            # WSGI config
├── social/                # App principale
│   ├── models.py          # Modelli del database
│   ├── views.py           # Logica delle views
│   ├── forms.py           # Form Django
│   ├── urls.py            # URL dell'app
│   └── admin.py           # Configurazione admin
├── templates/             # Template HTML
│   ├── base.html          # Template base
│   └── social/            # Template dell'app
├── media/                 # File caricati dagli utenti
├── static/                # File statici
├── requirements.txt       # Dipendenze Python
└── manage.py             # Script di gestione Django
```

## 🎨 Tecnologie Utilizzate

- **Backend**: Django 5.0.1
- **Database**: PostgreSQL
- **Real-Time**: Django Channels 4.0, Redis, WebSocket
- **ASGI Server**: Daphne 4.0
- **Frontend**: TailwindCSS, Font Awesome
- **Form Styling**: django-crispy-forms con crispy-tailwind
- **Image Processing**: Pillow
- **Configuration**: python-decouple

## 👤 Admin Panel

Accedi al pannello di amministrazione su http://localhost:8000/admin con le credenziali del superutente.

Da qui puoi:
- Gestire utenti
- Moderare post e commenti
- Visualizzare statistiche
- Gestire notifiche

## 🔒 Sicurezza

- Le password sono hashate con gli algoritmi di Django
- CSRF protection abilitato
- Validazione dei form lato server
- Protezione contro SQL injection tramite ORM Django

## 📝 Modelli del Database

- **User**: Utente Django standard
- **Profile**: Profilo utente esteso
- **Post**: Post pubblicati dagli utenti
- **Comment**: Commenti sui post
- **Like**: Like sui post
- **Follow**: Relazioni di follow tra utenti
- **Notification**: Notifiche per gli utenti
- **ChatRoom**: Stanze chat per messaggistica
- **Message**: Messaggi nelle chat

## 🚀 Deployment

Per il deployment in produzione:

1. Imposta `DEBUG=False` nel file `.env`
2. Configura `ALLOWED_HOSTS` in `settings.py`
3. Usa un server web production-ready (Gunicorn, uWSGI)
4. Configura un reverse proxy (Nginx, Apache)
5. Usa un servizio di hosting per i file statici e media
6. Configura HTTPS

## 📄 Licenza

Questo progetto è open source.

## 👨‍💻 Autore

Zone4Love Social Network
# talk
