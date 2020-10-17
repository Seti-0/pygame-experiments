@echo off
call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
call conda activate pygame
python server.py
PAUSE