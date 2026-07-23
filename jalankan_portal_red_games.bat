@echo off
title PROMPT GEMINI - RED GAMES
cd /d "%~dp0"
echo Memulai server portal...
python -m streamlit run app.py --server.port 8505
pause