#!/bin/bash
# Fix WebSocket per Talkie - Verifica e Risoluzione
# Esegui sul server come root

echo "🔍 DIAGNOSI WEBSOCKET TALKIE"
echo "============================"
echo ""

# 1. Verifica Daphne
echo "1. DAPHNE STATUS:"
systemctl status talkie-daphne --no-pager | head -10
echo ""

# 2. Verifica se Daphne ascolta sulla porta 8001
echo "2. DAPHNE PORTA 8001:"
netstat -tlnp | grep 8001 || ss -tlnp | grep 8001
echo ""

# 3. Verifica Redis
echo "3. REDIS STATUS:"
redis-cli ping 2>&1
echo ""

# 4. Nginx config per WebSocket
echo "4. NGINX WEBSOCKET CONFIG:"
grep -A 15 "location /ws" /etc/nginx/sites-enabled/talkie 2>/dev/null || echo "❌ Config non trovata"
echo ""

# 5. Test connessione locale a Daphne
echo "5. TEST CONNESSIONE LOCALE DAPHNE:"
curl -I http://127.0.0.1:8001/ 2>&1 | head -5
echo ""

# 6. Logs Daphne recenti
echo "6. LOGS DAPHNE (ultimi 30):"
journalctl -u talkie-daphne -n 30 --no-pager
echo ""

# 7. Nginx error log
echo "7. NGINX ERROR LOG (ultimi 20):"
tail -20 /var/log/nginx/error.log
echo ""

echo "=== FINE DIAGNOSI ==="
echo ""
echo "📋 Se Daphne non è attivo, esegui:"
echo "   systemctl start talkie-daphne"
echo "   systemctl enable talkie-daphne"
