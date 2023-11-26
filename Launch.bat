@echo off
cd %~dp0
pip install --upgrade requests
cls
pip install --upgrade pygame
cls
python main.py