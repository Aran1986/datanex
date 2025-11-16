@echo off
title Stop DataNex
color 0C

echo.
echo Stopping DataNex...
echo.

cd /d "%~dp0"

docker-compose down
taskkill /FI "WindowTitle eq DataNex Backend*" /F >nul 2>&1
taskkill /FI "WindowTitle eq DataNex Frontend*" /F >nul 2>&1

echo.
echo DataNex stopped!
echo.
pause
