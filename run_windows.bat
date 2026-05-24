@echo off
echo Starting Originality Studio Pro...
if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
python app.py
pause
