#!/bin/bash
# Diagnosi completa problema form non funzionanti

echo "🔍 DIAGNOSI FORM TALKIE"
echo "======================"
echo ""

cd /opt/talkie/app

echo "1. VERIFICA SETTINGS.PY:"
echo "CSRF_COOKIE_HTTPONLY:"
grep CSRF_COOKIE_HTTPONLY talkie/settings.py || echo "❌ NON TROVATO"
echo ""
echo "CSRF_COOKIE_SECURE:"
grep CSRF_COOKIE_SECURE talkie/settings.py || echo "❌ NON TROVATO"
echo ""
echo "CSRF_TRUSTED_ORIGINS:"
grep -A 7 CSRF_TRUSTED_ORIGINS talkie/settings.py
echo ""

echo "2. STATUS GUNICORN:"
systemctl status talkie --no-pager | head -5
echo ""

echo "3. ULTIMI ERRORI GUNICORN:"
journalctl -u talkie -n 30 --no-pager | grep -i error
echo ""

echo "4. TEST CSRF TOKEN:"
echo "Esegui nel browser console:"
echo "  document.cookie"
echo ""
echo "Deve contenere: csrftoken=..."
echo ""

echo "5. TEST FORM POST:"
echo "Prova a creare un post e guarda console browser per errori"
echo ""

echo "=== FINE DIAGNOSI ==="
