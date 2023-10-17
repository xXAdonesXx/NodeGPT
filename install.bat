@echo off

REM Erstelle eine virtuelle Umgebung namens 'venv'
python -m venv venv

REM Aktiviere die virtuelle Umgebung
venv\Scripts\activate

REM Installiere die Abhängigkeiten aus 'requirements.txt'
pip install -r requirements.txt

REM Deaktiviere die virtuelle Umgebung
deactivate

pause
