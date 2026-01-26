# Guida Installazione Zone4Love

## Setup Rapido

### 1. Crea ambiente virtuale
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Installa dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configura database PostgreSQL
Apri pgAdmin o psql e esegui:
```sql
CREATE DATABASE zone4love_db;
```

### 4. Configura variabili ambiente
```bash
copy .env.example .env
```
Modifica `.env` con le tue credenziali PostgreSQL.

### 5. Setup database Django
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Crea cartelle media e immagine default
```bash
python setup_media.py
python create_default_image.py
```

### 7. Avvia il server
```bash
python manage.py runserver
```

Visita: http://localhost:8000

## Risoluzione Problemi Comuni

### Errore: "No module named 'decouple'"
```bash
pip install python-decouple
```

### Errore: "relation does not exist"
```bash
python manage.py makemigrations social
python manage.py migrate
```

### Errore: "FATAL: password authentication failed"
Verifica le credenziali nel file `.env`

### Immagine profilo non visualizzata
Assicurati che `media/profile_pics/default.jpg` esista:
```bash
python create_default_image.py
```
