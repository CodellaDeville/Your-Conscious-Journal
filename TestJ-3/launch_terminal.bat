@echo off
echo Starting Daily Journaling Coach in a new terminal...
start cmd /k "cd /d %~dp0 && python -m streamlit run journal_app.py"
echo Second terminal launched successfully!