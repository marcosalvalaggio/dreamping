@echo off

:: Change to the home directory
cd /d %HOMEDRIVE%%HOMEPATH%

:: Check Python version
powershell -Command "python --version" > nul 2>&1

if %errorlevel% neq 0 (
    echo Python is not installed in the home directory.
) else (
    echo Python is installed in the home directory.
)

:: Clone the repository
git clone --depth=1 https://github.com/marcosalvalaggio/dreamping.git 
