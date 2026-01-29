#!/usr/bin/env python3
"""
Script per creare il primo post del blog: annuncio lancio Talkie
Esegui dopo aver fatto le migrazioni del database
"""

import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talkie.settings')
django.setup()

from django.contrib.auth.models import User
from social.models import BlogPost
from django.utils.text import slugify

# Crea o ottieni utente admin
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@talkie.ovh',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f'✓ Utente admin creato')
else:
    print(f'✓ Utente admin già esistente')

# Contenuto del post di lancio
title = "🎉 Benvenuti su Talkie: Il Futuro degli Incontri Online è Qui!"
slug = slugify(title)

content = """
Oggi è un giorno speciale: **Talkie è ufficialmente live!** 🚀

Dopo mesi di sviluppo, test e perfezionamenti, siamo entusiasti di presentarvi una piattaforma completamente nuova per incontrare persone, fare connessioni autentiche e vivere esperienze uniche online.

## Cos'è Talkie?

Talkie non è il solito social network. È un mix perfetto tra la spontaneità delle chat random (ricordate Chatroulette?) e le funzionalità moderne di un social network completo.

**In poche parole:** è il posto dove puoi essere te stesso, incontrare persone nuove senza filtri, e costruire relazioni autentiche.

## Le Funzionalità Principali

### 🎲 Random Chat 1v1
La nostra funzione stella! Premi "Start" e vieni abbinato istantaneamente con qualcuno di nuovo da tutto il mondo. Non c'è feeling? Nessun problema: premi "Next" e trova un altro match. È veloce, spontaneo e sorprendentemente divertente.

**Perché è diverso?**
- Nessun profilo da scorrere all'infinito
- Nessun giudizio basato solo sulle foto
- Conversazioni autentiche, faccia a faccia (o tastiera a tastiera!)
- Possibilità di passare alla videochiamata se c'è chimica

### 📱 Social Network Completo
Non siamo solo chat random. Talkie è anche un social network dove puoi:
- **Pubblicare post** e condividere i tuoi pensieri
- **Creare storie** che scompaiono dopo 24 ore
- **Chattare in privato** con le persone che hai incontrato
- **Seguire utenti** interessanti
- **Reagire e commentare** i contenuti della community
- **Partecipare a gruppi** di interesse

### 🎥 Videochiamate WebRTC
Hai trovato qualcuno di interessante in chat? Passa alla videochiamata con un click! La nostra tecnologia WebRTC garantisce:
- Connessioni peer-to-peer sicure
- Qualità video HD
- Bassa latenza
- Nessun software da installare

### 🔔 Notifiche Realtime
Non perdere mai un messaggio, un like o un nuovo follower. Le nostre notifiche in tempo reale ti tengono sempre aggiornato.

## Perché Abbiamo Creato Talkie?

Siamo stanchi dei social network tradizionali dove tutto è:
- ✗ Filtrato e perfetto
- ✗ Basato su like e follower
- ✗ Superficiale e poco autentico
- ✗ Pieno di pubblicità invasive

Volevamo creare qualcosa di diverso. Un posto dove:
- ✓ Le persone possono essere se stesse
- ✓ Le connessioni sono genuine
- ✓ La spontaneità è celebrata
- ✓ La privacy è rispettata

## Sicurezza e Privacy al Primo Posto

La vostra sicurezza è la nostra priorità assoluta:
- **Crittografia HTTPS** per tutte le comunicazioni
- **Strumenti di blocco e report** sempre disponibili
- **Moderazione attiva** contro abusi e spam
- **Privacy policy GDPR compliant**
- **Nessuna vendita di dati** a terze parti

## Mobile-First e PWA

Talkie è progettato per essere perfetto su smartphone:
- Interfaccia mobile-first ottimizzata
- Installabile come PWA (Progressive Web App)
- Presto disponibile su **Google Play Store**
- Funziona anche offline (grazie al service worker)

## Cosa Aspettarsi nei Prossimi Mesi

Questo è solo l'inizio! Ecco cosa abbiamo in programma:

**Q1 2025:**
- 🎯 Filtri per Random Chat (età, genere, interessi, distanza)
- 🌍 Supporto multilingua
- 🎨 Temi personalizzabili (dark mode avanzato)
- 📊 Dashboard statistiche personali

**Q2 2025:**
- 🎮 Gamification e achievement
- 🎁 Sistema di regali virtuali
- 🎤 Chat vocali di gruppo
- 📹 Streaming live

**Q3 2025:**
- 🤖 Moderazione AI avanzata
- 🔍 Ricerca avanzata utenti
- 💬 Traduzione messaggi in tempo reale
- 🎭 Eventi virtuali e speed dating

## Come Iniziare

È semplicissimo:

1. **Registrati** con email e username
2. **Completa il profilo** (opzionale ma consigliato)
3. **Esplora il feed** per vedere cosa condivide la community
4. **Premi "Random"** per la tua prima chat casuale
5. **Divertiti** e fai nuove connessioni!

## Unisciti alla Community

Talkie è fatto dalla community, per la community. Vogliamo sentire la tua voce:
- 💡 Hai un'idea per una nuova funzionalità? Scrivici!
- 🐛 Hai trovato un bug? Segnalacelo su GitHub
- ❤️ Ti piace Talkie? Condividilo con gli amici!

## Ringraziamenti

Un enorme grazie a tutti i beta tester che hanno provato Talkie in anteprima e ci hanno dato feedback preziosissimi. Questo lancio è anche merito vostro!

## Pronti a Tuffarvi?

Non vediamo l'ora di vedere cosa costruirete su Talkie. Che siate qui per:
- Trovare l'amore ❤️
- Fare nuove amicizie 🤝
- Praticare una lingua straniera 🌍
- Semplicemente passare il tempo 🎮

...c'è un posto per voi qui.

**Benvenuti su Talkie. Benvenuti a casa.** 🏠

---

*P.S. Seguiteci sul blog per aggiornamenti settimanali, tutorial e storie dalla community!*

**Il Team Talkie**  
📧 support@talkie.ovh  
🌐 https://talkie.ovh  
💬 Inizia ora: [Random Chat](/random/)
"""

excerpt = "Oggi è un giorno speciale: Talkie è ufficialmente live! Scopri come funziona il nuovo social network per incontri autentici attraverso chat random, videochiamate e molto altro."

# Crea o aggiorna il post
post, created = BlogPost.objects.update_or_create(
    slug=slug,
    defaults={
        'title': title,
        'author': admin_user,
        'content': content,
        'excerpt': excerpt,
        'published': True,
        'published_at': datetime.now()
    }
)

if created:
    print(f'✓ Post di lancio creato: {post.title}')
else:
    print(f'✓ Post di lancio aggiornato: {post.title}')

print(f'\n🎉 Fatto! Visita /blog/ per vedere il post.')
