@echo off
python mcp.py
git add .
git commit -m "daily commit"
git pull origin main
git push origin main