cd C:\Users\Michael\Desktop\Coding\marketsupreme.github.io
@echo off
git pull origin main
python mcp.py
git add .
git commit -m "hourly commit"
git push origin main