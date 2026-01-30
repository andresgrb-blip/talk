#!/bin/bash
# Fix permessi nginx per static e media files
# Esegui sul server: bash FIX_NGINX_PERMISSIONS.sh

set -e

echo "🔧 FIX PERMESSI NGINX PER TALKIE"
echo "================================"
echo ""

# Vai nella directory del progetto
cd ~/social || { echo "❌ Directory ~/social non trovata. Modifica lo script con il percorso corretto."; exit 1; }

echo "📂 Directory progetto: $(pwd)"
echo ""

# 1. Identifica utente nginx
NGINX_USER=$(ps aux | grep nginx | grep worker | head -1 | awk '{print $1}')
if [ -z "$NGINX_USER" ]; then
    NGINX_USER="www-data"  # Default su Ubuntu/Debian
fi
echo "👤 Nginx user: $NGINX_USER"
echo ""

# 2. Collectstatic (assicurati che i file esistano)
echo "📦 Eseguo collectstatic..."
source venv/bin/activate
python manage.py collectstatic --noinput
echo "✅ Collectstatic completato"
echo ""

# 3. Fix permessi directory HOME (importante!)
echo "🔑 Fix permessi directory home..."
chmod 755 ~
echo "✅ Home directory ora accessibile"
echo ""

# 4. Fix permessi staticfiles
echo "📁 Fix permessi staticfiles/..."
chmod -R 755 staticfiles/
chown -R $USER:$NGINX_USER staticfiles/
echo "✅ Staticfiles permessi OK"
echo ""

# 5. Fix permessi media
echo "📁 Fix permessi media/..."
chmod -R 755 media/
chown -R $USER:$NGINX_USER media/
echo "✅ Media permessi OK"
echo ""

# 6. Fix permessi directory parent (percorso completo deve essere accessibile)
echo "🔐 Fix permessi percorso completo..."
CURRENT_DIR=$(pwd)
while [ "$CURRENT_DIR" != "/" ]; do
    chmod o+x "$CURRENT_DIR" 2>/dev/null || true
    CURRENT_DIR=$(dirname "$CURRENT_DIR")
done
echo "✅ Percorso completo accessibile"
echo ""

# 7. Test accesso come nginx user
echo "🧪 Test accesso come nginx user..."
echo ""

echo "Test 1: manifest.json"
sudo -u $NGINX_USER cat staticfiles/manifest.json > /dev/null 2>&1 && echo "✅ manifest.json leggibile" || echo "❌ manifest.json NON leggibile"

echo "Test 2: default.jpg"
sudo -u $NGINX_USER cat media/profile_pics/default.jpg > /dev/null 2>&1 && echo "✅ default.jpg leggibile" || echo "❌ default.jpg NON leggibile"

echo "Test 3: icon-192x192.png"
sudo -u $NGINX_USER cat staticfiles/icons/icon-192x192.png > /dev/null 2>&1 && echo "✅ icon-192x192.png leggibile" || echo "❌ icon-192x192.png NON leggibile"

echo ""

# 8. Riavvia nginx
echo "🔄 Riavvio nginx..."
sudo systemctl restart nginx
echo "✅ Nginx riavviato"
echo ""

# 9. Test finale
echo "🎯 TEST FINALE:"
echo "Prova questi URL nel browser:"
echo "  https://talkie.ovh/static/manifest.json"
echo "  https://talkie.ovh/media/profile_pics/default.jpg"
echo "  https://talkie.ovh/static/icons/icon-192x192.png"
echo ""
echo "Devono rispondere 200 OK, non 403 Forbidden"
echo ""

echo "✅ FATTO! Se ancora 403, esegui: sudo tail -f /var/log/nginx/error.log"
