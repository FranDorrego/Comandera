@echo off

echo.
echo ====================================
echo Activando entorno virtual...
echo ====================================
call HostBase\venv32\Scripts\activate.bat

echo.
echo ====================================
echo Iniciando servidor en http://localhost:3001 ...
echo ====================================
call uvicorn HostBase.api:app --port 3001 --reload

pause
