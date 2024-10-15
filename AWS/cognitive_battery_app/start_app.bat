@ECHO OFF
call .\..\config.bat
SET PORT=8080

cd cognitive-battery-app-frontend

start npm run electron:serve 8080


