@echo off
python mcp.py
git add .
PAUSE
git commit -m "daily commit"
git push origin main