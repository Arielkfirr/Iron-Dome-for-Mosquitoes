@echo off
echo 📱 Phone Link Setup for Iron Dome Mosquitoes
echo ============================================
echo.
echo Starting Phone Link setup...
echo.

cd /d "%~dp0"
python phone_link_cursor_setup.py

echo.
echo Setup completed!
pause 