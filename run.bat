@echo off
cd /d %~dp0

echo Activando entorno virtual...
call venv32\Scripts\activate.bat

echo Iniciando servidor en http://localhost:3001 ...
uvicorn HostBase.api:app --port 3001 --reload

pause
