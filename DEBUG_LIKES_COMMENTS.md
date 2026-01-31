# 🐛 Debug: Like e Commenti Non Si Salvano

## Diagnosi Necessaria

Apri il browser, vai su https://talkie.ovh/feed/ e:

### 1. Apri Console (F12 → Console)

### 2. Prova a mettere Like a un post

Guarda nella console, cerca errori tipo:
```
❌ 403 Forbidden
❌ CSRF token missing
❌ Failed to fetch
❌ Network error
```

### 3. Guarda la Tab Network (F12 → Network)

Quando clicchi Like:
- Cerca la richiesta a `/post/123/like/`
- Clicca sulla richiesta
- Guarda:
  - **Status Code**: deve essere 200 OK
  - **Response**: cosa risponde il server
  - **Headers**: c'è X-CSRFToken?

### 4. Verifica CSRF Cookie

Nella console esegui:
```javascript
document.cookie
```

Deve contenere `csrftoken=...`

Se NON c'è, il problema è lì.

---

## 🔧 Fix Comuni

### Fix 1: CSRF Token Mancante

Sul server, verifica settings.py:

```bash
grep CSRF_COOKIE /opt/talkie/app/talkie/settings.py
```

Deve avere:
```python
CSRF_COOKIE_SECURE = True  # Se HTTPS
CSRF_COOKIE_HTTPONLY = False  # Importante! Deve essere False per JavaScript
CSRF_TRUSTED_ORIGINS = ['https://talkie.ovh', 'http://talkie.ovh']
```

Se manca `CSRF_COOKIE_HTTPONLY = False`, aggiungilo e riavvia:
```bash
echo "CSRF_COOKIE_HTTPONLY = False" >> /opt/talkie/app/talkie/settings.py
systemctl restart talkie
```

### Fix 2: View Django Non Risponde

Testa direttamente:
```bash
# Sul server
cd /opt/talkie/app
source venv/bin/activate
python manage.py shell

# Nella shell Python:
from social.models import Post
Post.objects.first()
# Deve mostrare un post
```

### Fix 3: URL Non Corretta

Verifica che l'URL esista:
```bash
grep "like_post" /opt/talkie/app/social/urls.py
```

Deve avere:
```python
path('post/<int:post_id>/like/', views.like_post, name='like_post'),
```

---

## 🧪 Test Manuale

Nella console browser, esegui:

```javascript
// Test funzione likePost
likePost(1)  // Sostituisci 1 con un post_id reale

// Guarda la risposta nella console
```

---

## 📋 Checklist

- [ ] Console browser mostra errori quando clicco Like
- [ ] Network tab mostra richiesta POST a `/post/X/like/`
- [ ] Status code della richiesta (200 OK o errore?)
- [ ] `document.cookie` contiene `csrftoken`
- [ ] `CSRF_COOKIE_HTTPONLY = False` in settings.py
- [ ] URL `like_post` esiste in urls.py
- [ ] View `like_post` funziona (no errori in logs)

---

## 🚨 Se Ancora Non Funziona

Inviami:
1. Screenshot console browser con errori
2. Output di `document.cookie` dalla console
3. Output di:
```bash
journalctl -u talkie -n 50 | grep -i error
```

Con queste info posso darti la soluzione esatta!
