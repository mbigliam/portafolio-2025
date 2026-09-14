cd C:\Users\Mbiglia\Downloads\ia-security-gateway\ia-security-gateway

REM Eliminar duplicados de la raíz
del /Q index.html 2>nul
del /Q app.js 2>nul
del /Q config_fixed.py 2>nul
del /Q main_WITH_FRONTEND.py 2>nul

echo ✓ Duplicados eliminados

REM Verificar que los archivos correctos existen
if exist "public\index.html" echo ✓ public/index.html OK
if exist "public\app.js" echo ✓ public/app.js OK
if exist "app\main.py" echo ✓ app/main.py OK
if exist "app\core\config.py" echo ✓ app/core/config.py OK
if exist "app\services\compliance.py" echo ✓ app/services/compliance.py OK

echo.
echo ✓ PROYECTO LIMPIO Y ACTUALIZADO
