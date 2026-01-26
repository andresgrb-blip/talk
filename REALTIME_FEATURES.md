# Funzionalità Real-Time di Zone4Love

## 🚀 Panoramica

Zone4Love include un sistema completo di notifiche real-time basato su WebSocket che mantiene gli utenti aggiornati su tutte le attività importanti.

## 📡 Tipi di Notifiche Real-Time

### 1. **Notifiche Standard** (Rosa)
- **Like sui post**: Ricevi notifica quando qualcuno mette like al tuo post
- **Commenti**: Notifica quando qualcuno commenta i tuoi post
- **Nuovi follower**: Avviso quando qualcuno inizia a seguirti

**Caratteristiche:**
- Badge contatore nella navbar
- Toast notification con icona campana
- Durata: 5 secondi
- Colore: Rosa (border-pink-600)

### 2. **Nuovi Post** (Blu)
Quando qualcuno che segui pubblica un nuovo post, ricevi una notifica istantanea.

**Contenuto notifica:**
- Nome dell'autore
- Anteprima del contenuto (primi 100 caratteri)
- Indicatore se contiene immagine
- Click per visitare il profilo dell'autore

**Caratteristiche:**
- Toast notification con icona plus-circle
- Durata: 8 secondi
- Colore: Blu (border-blue-600)
- Cliccabile per vedere il profilo

### 3. **Nuovi Commenti** (Verde)
Quando qualcuno commenta uno dei tuoi post, ricevi notifica immediata.

**Contenuto notifica:**
- Nome del commentatore
- Anteprima del commento (primi 50 caratteri)
- Click per vedere il post completo

**Caratteristiche:**
- Toast notification con icona commento
- Durata: 8 secondi
- Colore: Verde (border-green-600)
- Cliccabile per vedere il post

## 🎨 Design Toast Notifications

### Posizionamento
- **Posizione**: Top-right (top-20 right-4)
- **Z-index**: 50 (sopra tutti gli elementi)
- **Animazione**: Slide-in da destra

### Interattività
- **Hover**: Shadow aumentato per feedback visivo
- **Click**: Naviga alla risorsa correlata
- **Chiusura**: Pulsante X o auto-dismiss dopo timeout
- **Auto-fade**: Dissolvenza graduale prima della rimozione

### Stacking
Le notifiche si impilano verticalmente, con le più recenti in alto.

## 🔧 Implementazione Tecnica

### Backend (Django Channels)

**Consumer** (`social/consumers.py`):
```python
class NotificationConsumer(AsyncWebsocketConsumer):
    async def new_post(self, event):
        # Invia notifica nuovo post
        
    async def new_comment(self, event):
        # Invia notifica nuovo commento
```

**Signals** (`social/signals.py`):
```python
@receiver(post_save, sender=Post)
def notify_followers_new_post(sender, instance, created, **kwargs):
    # Notifica tutti i follower del nuovo post
    
@receiver(post_save, sender=Comment)
def notify_post_author_new_comment(sender, instance, created, **kwargs):
    # Notifica l'autore del post del nuovo commento
```

### Frontend (JavaScript)

**WebSocket Connection**:
```javascript
const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);
```

**Message Handling**:
```javascript
notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    if (data.type === 'new_post') {
        showNewPostToast(data.post);
    } else if (data.type === 'new_comment') {
        showNewCommentToast(data.comment);
    }
};
```

## 📊 Flusso delle Notifiche

### Nuovo Post
```
1. Utente A crea un post
2. Signal post_save viene attivato
3. Sistema recupera tutti i follower di Utente A
4. Per ogni follower:
   - Invia messaggio WebSocket al loro canale
   - Toast appare in tempo reale
5. Follower può cliccare per vedere il profilo
```

### Nuovo Commento
```
1. Utente B commenta post di Utente A
2. Signal post_save viene attivato
3. Sistema verifica che B ≠ A
4. Invia messaggio WebSocket al canale di A
5. Toast appare in tempo reale
6. A può cliccare per vedere il post
```

## 🎯 Casi d'Uso

### Scenario 1: Influencer con molti follower
Un utente con 100 follower pubblica un post:
- 100 notifiche WebSocket inviate simultaneamente
- Ogni follower online riceve toast istantaneo
- Redis gestisce efficacemente il carico

### Scenario 2: Conversazione attiva
Post con molti commenti:
- Autore riceve notifica per ogni commento
- Notifiche si impilano se multiple
- Auto-dismiss previene sovraccarico UI

### Scenario 3: Utente offline
- Notifiche WebSocket non ricevute
- Notifiche standard salvate nel database
- Visibili al prossimo login nella pagina notifiche

## 🔐 Sicurezza

- **Autenticazione**: Solo utenti autenticati possono connettersi
- **Autorizzazione**: Ogni utente riceve solo le proprie notifiche
- **Canali isolati**: `notifications_{user_id}` unico per utente
- **Validazione**: AllowedHostsOriginValidator previene CORS attacks

## ⚡ Performance

### Ottimizzazioni
- **Anteprima contenuto**: Solo primi 100/50 caratteri inviati
- **Dati minimali**: Solo informazioni essenziali nel payload
- **Redis**: Gestione efficiente di migliaia di connessioni
- **Async**: Operazioni non bloccanti

### Scalabilità
- Redis può gestire 10,000+ connessioni simultanee
- Channel layers distribuiti per load balancing
- Graceful degradation se WebSocket non disponibile

## 🧪 Testing

### Test Manuale

**Test Nuovo Post:**
1. Apri due browser/tab
2. Login con User A e User B
3. User B segue User A
4. User A crea un post
5. User B dovrebbe vedere toast blu istantaneo

**Test Nuovo Commento:**
1. User A crea un post
2. User B commenta il post
3. User A dovrebbe vedere toast verde istantaneo

### Debug

**Console Browser:**
```javascript
// Verifica connessione WebSocket
console.log(notificationSocket.readyState);
// 0 = CONNECTING, 1 = OPEN, 2 = CLOSING, 3 = CLOSED
```

**Django Logs:**
```python
# In signals.py, aggiungi:
print(f"Notifying {len(followers)} followers of new post")
```

## 📱 Responsive Design

- **Desktop**: Toast a destra, dimensione completa
- **Mobile**: Toast adattato, max-width ridotto
- **Touch**: Swipe per chiudere (futuro enhancement)

## 🚀 Future Enhancements

1. **Suoni**: Audio notification opzionale
2. **Vibrazione**: Haptic feedback su mobile
3. **Raggruppamento**: Multiple notifiche simili raggruppate
4. **Preferenze**: Utente può disabilitare certi tipi
5. **Desktop Notifications**: Browser native notifications
6. **Typing indicators**: "X sta scrivendo..." nelle chat
7. **Online status**: Indicatore utenti online
8. **Read receipts**: Conferma lettura messaggi

## 🎨 Personalizzazione

### Modificare Durata Toast
```javascript
// In base.html, modifica timeout:
setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
}, 8000); // Cambia 8000 in millisecondi desiderati
```

### Modificare Colori
```javascript
// Cambia border-blue-600 in:
border-purple-600  // Viola
border-orange-600  // Arancione
border-indigo-600  // Indaco
```

### Disabilitare Notifiche Specifiche
```javascript
notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    // Commenta per disabilitare
    // if (data.type === 'new_post') {
    //     showNewPostToast(data.post);
    // }
};
```

## 📖 Riferimenti

- Django Channels: https://channels.readthedocs.io/
- WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- Redis: https://redis.io/documentation
- TailwindCSS: https://tailwindcss.com/docs
