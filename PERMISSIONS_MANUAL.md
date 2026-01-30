# 🔐 Fix Manuale Permessi Nginx

## Problema
Nginx non può leggere i file in `staticfiles/` e `media/` perché:
1. La directory home (`~`) non è accessibile
2. I file non hanno permessi di lettura per "others"
3. L'owner/group non include nginx user

---

## ✅ Soluzione Step-by-Step

### 1. Identifica Nginx User
```bash
ps aux | grep nginx | grep worker

# Output esempio:
# www-data  1234  ... nginx: worker process
#
# L'utente è "www-data" (prima colonna)
```

### 2. Rendi Home Directory Accessibile
```bash
# IMPORTANTE: nginx deve poter attraversare la tua home
chmod 755 ~

# Verifica
ls -ld ~
# Output deve essere: drwxr-xr-x (il 5 finale è cruciale)
```

**Perché?** Se la tua home è `drwx------` (700), nginx non può accedere a `~/social/staticfiles/` anche se i file hanno permessi 755.

### 3. Fix Permessi Staticfiles
```bash
cd ~/social

# Permessi lettura per tutti
chmod -R 755 staticfiles/

# Owner: tu, Group: nginx user
sudo chown -R $USER:www-data staticfiles/

# Verifica
ls -la staticfiles/
# Deve essere: drwxr-xr-x  user  www-data
```

### 4. Fix Permessi Media
```bash
chmod -R 755 media/
sudo chown -R $USER:www-data media/

# Verifica
ls -la media/
# Deve essere: drwxr-xr-x  user  www-data
```

### 5. Fix Percorso Completo
```bash
# Ogni directory nel percorso deve essere attraversabile (x)
# Esempio: se il percorso è /home/zion/social/staticfiles/
# Allora /home, /home/zion, /home/zion/social devono avere x

chmod o+x /home
chmod o+x /home/zion  # Sostituisci con il tuo username
chmod o+x /home/zion/social
```

### 6. Test Accesso come Nginx User
```bash
# Prova a leggere i file come nginx user
sudo -u www-data cat ~/social/staticfiles/manifest.json

# Se funziona: ✅ Permessi OK
# Se errore "Permission denied": ❌ Ancora problemi
```

### 7. Riavvia Nginx
```bash
sudo systemctl restart nginx
```

### 8. Verifica nel Browser
```
https://talkie.ovh/static/manifest.json
https://talkie.ovh/media/profile_pics/default.jpg
```

Devono dare **200 OK**, non 403.

---

## 🔍 Troubleshooting

### Se ancora 403 dopo i fix sopra:

#### A. Controlla Logs Nginx
```bash
sudo tail -f /var/log/nginx/error.log

# Cerca errori tipo:
# "Permission denied" → permessi insufficienti
# "stat() failed (13: Permission denied)" → directory parent non accessibile
```

#### B. Debug Percorso Completo
```bash
# Testa ogni livello del percorso
namei -l ~/social/staticfiles/manifest.json

# Output mostra permessi di ogni directory nel percorso
# Cerca righe con "---" (no permessi) o "Permission denied"
```

#### C. SELinux (se su CentOS/RHEL)
```bash
# Controlla
getenforce

# Se "Enforcing", dai permessi:
sudo chcon -Rt httpd_sys_content_t ~/social/staticfiles/
sudo chcon -Rt httpd_sys_content_t ~/social/media/
```

#### D. AppArmor (se su Ubuntu)
```bash
# Controlla se nginx è ristretto
sudo aa-status | grep nginx

# Se sì, metti in complain mode:
sudo aa-complain /etc/apparmor.d/usr.sbin.nginx
sudo systemctl restart nginx
```

---

## 🎯 Soluzione Alternativa: Sposta Files in /var/www

Se niente funziona, sposta i file in una directory che nginx può sempre leggere:

```bash
# Crea directory
sudo mkdir -p /var/www/talkie/static
sudo mkdir -p /var/www/talkie/media

# Copia files
sudo cp -r ~/social/staticfiles/* /var/www/talkie/static/
sudo cp -r ~/social/media/* /var/www/talkie/media/

# Permessi
sudo chown -R www-data:www-data /var/www/talkie/
sudo chmod -R 755 /var/www/talkie/

# Aggiorna nginx config:
# location /static/ {
#     alias /var/www/talkie/static/;
# }
# location /media/ {
#     alias /var/www/talkie/media/;
# }

sudo systemctl restart nginx
```

Poi ogni volta che fai `collectstatic`, ricopia:
```bash
sudo cp -r ~/social/staticfiles/* /var/www/talkie/static/
```

---

## 📋 Checklist Finale

- [ ] Home directory ha permessi 755 (`chmod 755 ~`)
- [ ] Staticfiles ha permessi 755 ricorsivi
- [ ] Media ha permessi 755 ricorsivi
- [ ] Owner/group corretto (user:www-data)
- [ ] Percorso completo attraversabile (ogni dir ha +x)
- [ ] Test `sudo -u www-data cat file` funziona
- [ ] Nginx riavviato
- [ ] Browser mostra 200 OK, non 403
- [ ] Logs nginx senza errori "Permission denied"

---

**Una volta completata la checklist, il 403 sarà risolto! 🎉**
