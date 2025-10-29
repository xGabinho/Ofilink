@echo off
title Ofilink - Servidor Flask
echo ====================================
echo     🚀 Iniciando entorno Ofilink...
echo ====================================

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Abrir navegador directamente en el login
start http://127.0.0.1:5000/login

REM Ejecutar servidor Flask
python app.py

pause