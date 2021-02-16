@echo off
python mcp.py
git add .
PAUSE
git commit -m "daily commit"
PAUSE
git pull origin main
git push origin main
PAUSE