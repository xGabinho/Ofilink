@echo off
title Ofilink - Servidor Flask
echo ====================================
echo     🚀 Iniciando entorno Ofilink...
echo ====================================

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Abrir navegador automáticamente
start http://127.0.0.1:5000

REM Ejecutar servidor Flask
echo Ejecutando servidor Flask...
python app.py

REM Mantener la ventana abierta si el servidor se detiene
pause