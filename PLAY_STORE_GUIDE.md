# Guida Pubblicazione Google Play Store - Talkie PWA

## ✅ Prerequisiti Completati

- [x] PWA manifest.json configurato
- [x] Service Worker implementato
- [x] Icone generate (72x72 fino a 512x512)
- [x] Meta tags PWA in base.html
- [x] HTTPS obbligatorio (già configurato su talkie.ovh)

---

## 📱 Step 1: Installare Bubblewrap CLI

Bubblewrap è lo strumento ufficiale Google per creare TWA (Trusted Web Activity) da PWA.

```bash
# Installa Node.js (se non ce l'hai)
# Scarica da: https://nodejs.org/

# Installa Bubblewrap globalmente
npm install -g @bubblewrap/cli

# Verifica installazione
bubblewrap --version
```

---

## 🔧 Step 2: Inizializzare il Progetto TWA

```bash
cd /Users/zion/Desktop/social

# Inizializza TWA (rispondi alle domande)
bubblewrap init --manifest https://talkie.ovh/static/manifest.json
```

### Domande che ti farà:

1. **Domain**: `talkie.ovh`
2. **Package name**: `com.talkie.app` (o quello che preferisci)
3. **App name**: `Talkie`
4. **Start URL**: `https://talkie.ovh/`
5. **Icon URL**: `https://talkie.ovh/static/icons/icon-512x512.png`
6. **Theme color**: `#db2777`
7. **Background color**: `#ffffff`
8. **Display mode**: `standalone`
9. **Orientation**: `portrait`

Questo creerà una cartella `twa-project/` con il progetto Android.

---

## 🔑 Step 3: Generare Keystore per Firma App

```bash
cd twa-project

# Genera keystore (SALVALO IN POSTO SICURO!)
keytool -genkey -v -keystore talkie-release-key.keystore \
  -alias talkie \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Ti chiederà:
# - Password (RICORDALA!)
# - Nome, Organizzazione, Città, Paese
```

**⚠️ IMPORTANTE**: Salva il file `.keystore` e la password in un posto sicuro. Se li perdi, non potrai più aggiornare l'app!

---

## 🏗️ Step 4: Buildare l'APK/AAB

```bash
# Build per Play Store (AAB - Android App Bundle)
bubblewrap build

# Questo genera:
# - app-release-signed.aab (per Play Store)
# - app-release-signed.apk (per test locale)
```

### Test locale prima di pubblicare:

```bash
# Installa APK sul tuo telefono Android
adb install app-release-signed.apk

# Oppure trasferisci il file APK via email/USB e installalo manualmente
```

---

## 📝 Step 5: Creare Account Google Play Console

1. Vai su: https://play.google.com/console
2. **Crea account sviluppatore** ($25 una tantum)
3. Compila informazioni fiscali e identità
4. Accetta termini e condizioni

---

## 🚀 Step 6: Creare Nuova App su Play Console

1. **Crea app** → Seleziona:
   - Nome: `Talkie`
   - Lingua predefinita: Italiano
   - App o gioco: App
   - Gratuita o a pagamento: Gratuita

2. **Dichiarazioni**:
   - Privacy policy URL: `https://talkie.ovh/privacy/` (devi crearlo!)
   - Categoria: Social
   - Target audience: 18+ (per dating/random chat)

---

## 📋 Step 7: Preparare Asset Grafici

### Screenshot richiesti (minimo 2 per tipo):

**Smartphone (obbligatorio)**:
- Dimensioni: 16:9 o 9:16
- Risoluzione minima: 320px
- Risoluzione massima: 3840px
- Formato: PNG o JPEG (24-bit)

**Tablet (opzionale ma consigliato)**:
- 7" e 10"
- Stesse specifiche degli smartphone

### Come creare screenshot:

```bash
# Opzione 1: Usa Chrome DevTools
# 1. Apri https://talkie.ovh in Chrome
# 2. F12 → Toggle device toolbar
# 3. Seleziona "Pixel 7" o altro device
# 4. Naviga nelle pagine principali (feed, random, chat, profile)
# 5. Screenshot → Capture screenshot

# Opzione 2: Usa telefono reale
# Installa APK e fai screenshot nativi
```

### Icona app (obbligatoria):

- **512x512 PNG** (già creata: `static/icons/icon-512x512.png`)
- Sfondo trasparente o colorato
- No bordi/ombre

### Feature Graphic (obbligatoria):

- **1024x500 PNG o JPEG**
- Banner promozionale per Play Store
- Deve includere nome app e visual accattivante

```bash
# Puoi crearla con Canva, Figma, o Photoshop
# Template: 1024x500px
# Testo: "Talkie - Incontra nuove persone"
# Colore brand: #db2777 (rosa)
```

---

## 📤 Step 8: Upload AAB su Play Console

1. **Production** → **Create new release**
2. **Upload** → Seleziona `app-release-signed.aab`
3. **Release name**: `1.0.0`
4. **Release notes** (italiano):
   ```
   Prima release di Talkie!
   
   ✨ Funzionalità:
   - Chat random 1v1 per nuovi incontri
   - Feed social con post e storie
   - Messaggi privati e videochiamate
   - Profili personalizzabili
   - Notifiche in tempo reale
   ```

---

## 📄 Step 9: Compilare Scheda Store

### Descrizione breve (80 caratteri max):
```
Incontra nuove persone con chat random e condividi momenti speciali
```

### Descrizione completa (4000 caratteri max):
```
🌟 Talkie - Il Social Network per Nuovi Incontri

Stanco dei soliti social? Talkie combina il meglio delle chat random con un social network moderno per aiutarti a incontrare persone nuove in modo autentico e divertente.

✨ CHAT RANDOM 1v1
Premi "Start" e vieni abbinato istantaneamente con qualcuno di nuovo. Non c'è feeling? Premi "Next" e trova un altro match. È veloce, spontaneo e sorprendente.

💬 MESSAGGI PRIVATI
Hai trovato qualcuno di interessante? Continua la conversazione in privato con chat testuali e videochiamate integrate.

📸 FEED & STORIE
Condividi momenti della tua giornata con post e storie che scompaiono dopo 24 ore. Metti like, commenta e interagisci con la community.

👤 PROFILO PERSONALIZZATO
Crea il tuo profilo con foto, bio e interessi. Mostra chi sei davvero.

🔔 NOTIFICHE REALTIME
Ricevi notifiche istantanee per nuovi messaggi, match e interazioni.

🎯 PERCHÉ TALKIE?
- 100% gratuito
- Interfaccia moderna e intuitiva
- Nessuna pubblicità invasiva
- Rispetto e sicurezza al primo posto

Scarica Talkie ora e inizia a incontrare persone nuove oggi stesso! 💕
```

### Categoria:
- **Social**

### Tag (fino a 5):
- chat
- incontri
- social
- amicizia
- random

---

## 🔒 Step 10: Questionario Sicurezza Dati

Google richiede dichiarazioni su:

1. **Raccolta dati**:
   - ✅ Email (per registrazione)
   - ✅ Nome utente
   - ✅ Foto profilo
   - ✅ Messaggi (chat)
   - ✅ Posizione (se implementi filtri geografici)

2. **Uso dati**:
   - Funzionalità app
   - Personalizzazione
   - Comunicazione tra utenti

3. **Condivisione dati**:
   - ❌ No condivisione con terze parti (se vero)

4. **Sicurezza**:
   - ✅ Dati criptati in transito (HTTPS)
   - ✅ Possibilità di eliminare account

---

## 🛡️ Step 11: Privacy Policy (OBBLIGATORIA)

Devi creare una pagina `/privacy/` su talkie.ovh. Esempio minimo:

```python
# In social/views.py
def privacy_policy(request):
    return render(request, 'social/privacy_policy.html')

# In social/urls.py
path('privacy/', views.privacy_policy, name='privacy_policy'),
```

Template `privacy_policy.html` deve includere:
- Quali dati raccogli
- Come li usi
- Come li proteggi
- Diritti utente (GDPR se EU)
- Contatto per richieste

---

## ✅ Step 12: Inviare per Revisione

1. **Review summary** → Controlla tutto
2. **Start rollout to Production**
3. **Conferma**

### Tempi di revisione:
- Prima app: **3-7 giorni**
- Aggiornamenti successivi: **1-3 giorni**

---

## 🎉 Step 13: App Pubblicata!

Una volta approvata:
- URL Play Store: `https://play.google.com/store/apps/details?id=com.talkie.app`
- Condividi il link sui social
- Monitora recensioni e crash reports

---

## 🔄 Aggiornamenti Futuri

Per pubblicare aggiornamenti:

```bash
cd twa-project

# Incrementa versione in twa-manifest.json
# "versionCode": 2,
# "versionName": "1.0.1"

# Rebuilda
bubblewrap build

# Upload nuovo AAB su Play Console → Production → New release
```

**IMPORTANTE**: Gli aggiornamenti al sito web (talkie.ovh) si riflettono automaticamente nell'app perché è una TWA! Devi rifare build solo per:
- Cambi manifest.json
- Cambi icone
- Cambi package name
- Cambi permessi Android

---

## 🆘 Troubleshooting

### Errore: "Digital Asset Links not verified"

Devi aggiungere un file `.well-known/assetlinks.json` al tuo sito:

```bash
# Bubblewrap lo genera automaticamente
bubblewrap fingerprint

# Output esempio:
# SHA256: AA:BB:CC:DD:...

# Crea file: static/.well-known/assetlinks.json
```

Contenuto:
```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.talkie.app",
    "sha256_cert_fingerprints": ["AA:BB:CC:DD:..."]
  }
}]
```

Servi questo file su: `https://talkie.ovh/.well-known/assetlinks.json`

### Errore: "App not installable"

- Verifica che HTTPS funzioni su talkie.ovh
- Verifica che manifest.json sia accessibile
- Verifica che tutte le icone esistano

### Errore: "Signature mismatch"

- Hai cambiato keystore? Devi usare sempre lo stesso
- Verifica fingerprint con: `keytool -list -v -keystore talkie-release-key.keystore`

---

## 📊 Monitoraggio Post-Lancio

### Google Play Console Dashboard:
- **Installs**: quante persone scaricano
- **Uninstalls**: quante disinstallano
- **Crashes**: errori app (TWA ha pochi crash)
- **Reviews**: recensioni utenti
- **Pre-launch reports**: test automatici Google

### Analytics (opzionale):
Aggiungi Google Analytics o Firebase al sito per tracciare:
- Utenti attivi
- Pagine più visitate
- Retention rate

---

## 🎯 Checklist Finale Pre-Pubblicazione

- [ ] HTTPS attivo su talkie.ovh
- [ ] Manifest.json accessibile
- [ ] Service Worker funzionante
- [ ] Tutte le icone generate
- [ ] Privacy policy pubblicata
- [ ] Screenshot preparati (min 2)
- [ ] Feature graphic 1024x500
- [ ] Icona 512x512
- [ ] Descrizioni scritte
- [ ] Keystore salvato in sicuro
- [ ] AAB buildato e testato
- [ ] Account Play Console creato ($25)
- [ ] Questionario sicurezza dati compilato
- [ ] Asset links verificati

---

## 💡 Tips Finali

1. **Testa l'APK prima**: installa su telefono reale e prova tutte le funzioni
2. **Rispondi alle recensioni**: engagement migliora ranking
3. **Aggiorna regolarmente**: anche solo bugfix mostrano app attiva
4. **Promuovi**: condividi link Play Store su Instagram, TikTok, etc.
5. **Monitora crash**: Play Console ti avvisa se ci sono problemi

---

## 📞 Supporto

- **Bubblewrap docs**: https://github.com/GoogleChromeLabs/bubblewrap
- **Play Console help**: https://support.google.com/googleplay/android-developer
- **TWA guide**: https://developer.chrome.com/docs/android/trusted-web-activity/

Buona fortuna con la pubblicazione! 🚀
