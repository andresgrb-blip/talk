#!/bin/bash
# Comandi diretti per fix permessi - /opt/talkie/app
# Sei già root, quindi non serve sudo

cd /opt/talkie/app

echo "🔧 FIX PERMESSI NGINX - COMANDI DIRETTI"
echo "========================================"
echo ""

# 1. Collectstatic
echo "1. Collectstatic..."
source venv/bin/activate
python manage.py collectstatic --noinput
echo ""

# 2. Permessi directory parent
echo "2. Permessi directory /opt/talkie..."
chmod 755 /opt
chmod 755 /opt/talkie
chmod 755 /opt/talkie/app
echo ""

# 3. Permessi staticfiles
echo "3. Permessi staticfiles/..."
chmod -R 755 staticfiles/
chown -R root:www-data staticfiles/
echo ""

# 4. Permessi media
echo "4. Permessi media/..."
chmod -R 755 media/
chown -R root:www-data media/
echo ""

# 5. Test accesso
echo "5. Test accesso come www-data..."
su -s /bin/bash -c "cat /opt/talkie/app/staticfiles/manifest.json" www-data > /dev/null 2>&1 && echo "✅ manifest.json OK" || echo "❌ manifest.json FAIL"
su -s /bin/bash -c "cat /opt/talkie/app/media/profile_pics/default.jpg" www-data > /dev/null 2>&1 && echo "✅ default.jpg OK" || echo "❌ default.jpg FAIL"
echo ""

# 6. Riavvia nginx
echo "6. Riavvio nginx..."
systemctl restart nginx
echo "✅ Nginx riavviato"
echo ""

echo "🎯 FATTO! Testa nel browser:"
echo "   https://talkie.ovh/static/manifest.json"
echo "   https://talkie.ovh/media/profile_pics/default.jpg"
