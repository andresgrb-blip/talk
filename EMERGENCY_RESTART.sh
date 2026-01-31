#!/bin/bash
# Emergency restart per Talkie quando il sito è down
# Esegui sul server come root

echo "🚨 EMERGENCY RESTART TALKIE"
echo "==========================="
echo ""

# 1. Verifica status servizi
echo "1. STATUS SERVIZI:"
echo ""
echo "Nginx:"
systemctl status nginx --no-pager | head -3
echo ""
echo "Gunicorn (talkie):"
systemctl status talkie --no-pager | head -3
echo ""
echo "Daphne (talkie-daphne):"
systemctl status talkie-daphne --no-pager | head -3
echo ""

# 2. Controlla errori recenti
echo "2. ULTIMI ERRORI:"
echo ""
echo "Gunicorn errors:"
journalctl -u talkie -n 20 --no-pager | tail -10
echo ""
echo "Nginx errors:"
tail -10 /var/log/nginx/error.log
echo ""

# 3. Riavvia tutto
echo "3. RIAVVIO SERVIZI..."
echo ""

echo "Riavvio Gunicorn..."
systemctl restart talkie
sleep 2

echo "Riavvio Daphne..."
systemctl restart talkie-daphne
sleep 2

echo "Riavvio Nginx..."
systemctl restart nginx
sleep 2

# 4. Verifica status finale
echo ""
echo "4. STATUS FINALE:"
echo ""
systemctl status talkie --no-pager | head -3
systemctl status talkie-daphne --no-pager | head -3
systemctl status nginx --no-pager | head -3
echo ""

# 5. Test connessione
echo "5. TEST CONNESSIONE:"
curl -I http://localhost:8000/ 2>&1 | head -5
echo ""

echo "=== FINE RESTART ==="
echo ""
echo "🧪 Testa nel browser: https://talkie.ovh"
echo ""
echo "Se ancora down, controlla:"
echo "  journalctl -u talkie -n 50"
echo "  journalctl -u talkie-daphne -n 50"
