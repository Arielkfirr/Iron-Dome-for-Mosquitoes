@echo off
echo 🐱 Iron Dome for Mosquitoes - Cat Detection Test
echo ================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run the test
echo Starting cat detection test...
python test_cat_detection.py

pause 