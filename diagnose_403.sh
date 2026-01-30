#!/bin/bash
# Script di diagnosi per errore 403 su static/media files
# Esegui questo sul server: bash diagnose_403.sh

echo "=== DIAGNOSI ERRORE 403 TALKIE ==="
echo ""

# 1. Percorso progetto
echo "1. PERCORSO PROGETTO:"
pwd
echo ""

# 2. Verifica esistenza directory
echo "2. DIRECTORY ESISTENTI:"
ls -la | grep -E "static|media"
echo ""

# 3. Permessi dettagliati
echo "3. PERMESSI STATICFILES:"
ls -la staticfiles/ 2>/dev/null || echo "❌ Directory staticfiles/ non trovata!"
echo ""

echo "4. PERMESSI MEDIA:"
ls -la media/ 2>/dev/null || echo "❌ Directory media/ non trovata!"
echo ""

# 4. File specifici che danno 403
echo "5. FILE SPECIFICI:"
echo "manifest.json:"
ls -la staticfiles/manifest.json 2>/dev/null || echo "❌ Non trovato"
echo ""
echo "default.jpg:"
ls -la media/profile_pics/default.jpg 2>/dev/null || echo "❌ Non trovato"
echo ""
echo "icon-192x192.png:"
ls -la staticfiles/icons/icon-192x192.png 2>/dev/null || echo "❌ Non trovato"
echo ""

# 5. Utente nginx
echo "6. UTENTE NGINX:"
ps aux | grep nginx | grep -v grep | head -3
echo ""

# 6. Config nginx attiva
echo "7. CONFIG NGINX PER TALKIE:"
if [ -f /etc/nginx/sites-enabled/talkie ]; then
    cat /etc/nginx/sites-enabled/talkie | grep -A 5 "location /static"
    echo ""
    cat /etc/nginx/sites-enabled/talkie | grep -A 5 "location /media"
else
    echo "❌ File /etc/nginx/sites-enabled/talkie non trovato"
    echo "File nginx disponibili:"
    ls -la /etc/nginx/sites-enabled/
fi
echo ""

# 7. Logs nginx recenti
echo "8. ULTIMI ERRORI NGINX:"
sudo tail -20 /var/log/nginx/error.log 2>/dev/null || echo "❌ Non posso leggere error.log (serve sudo)"
echo ""

# 8. SELinux
echo "9. SELINUX STATUS:"
getenforce 2>/dev/null || echo "SELinux non installato (OK)"
echo ""

# 9. Test accesso come nginx user
echo "10. TEST ACCESSO COME NGINX USER:"
NGINX_USER=$(ps aux | grep nginx | grep -v grep | grep worker | head -1 | awk '{print $1}')
echo "Nginx user: $NGINX_USER"
if [ ! -z "$NGINX_USER" ]; then
    echo "Test lettura manifest.json:"
    sudo -u $NGINX_USER cat staticfiles/manifest.json 2>&1 | head -1
    echo ""
    echo "Test lettura default.jpg:"
    sudo -u $NGINX_USER cat media/profile_pics/default.jpg 2>&1 | head -1
fi
echo ""

# 10. Percorsi assoluti
echo "11. PERCORSI ASSOLUTI:"
echo "Staticfiles: $(pwd)/staticfiles"
echo "Media: $(pwd)/media"
echo ""

echo "=== FINE DIAGNOSI ==="
echo ""
echo "📋 COPIA L'OUTPUT COMPLETO E INVIALO PER ANALISI"
