@echo off
cd frontend

echo.
echo ====================================
echo Instalando dependencias...
echo ====================================
call npm install

echo.
echo ====================================
echo Iniciando servidor en http://localhost:3000 ...
echo ====================================
call npm run dev


pause
