@echo off
title ACC Academy Launcher
echo ==========================================================
echo           KHOI CHAY DU AN ACC ACADEMY
echo ==========================================================
echo.

echo 1. Dang khoi chay Backend (FastAPI) trong cua so moi...
start "ACC Academy - Backend" cmd /k "cd backend && call venv\Scripts\activate && uvicorn app.main:app --reload"

echo 2. Dang khoi chay Frontend (Vite) trong cua so moi...
start "ACC Academy - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================================
echo Da gui lenh khoi chay cho ca hai dich vu!
echo Vui long kiem tra 2 cua so Command Prompt moi mo ra.
echo ==========================================================
echo.
pause
