@echo off
setlocal enabledelayedexpansion

:: Get the directory of the batch script
set "script_dir=%~dp0"

:: Set the full path to the venv directory
set "venv_path=%script_dir%venv"

:: Check if the venv folder exists
if not exist "%venv_path%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv "%venv_path%"
) else (
    echo Virtual environment already exists.
)

:: Activate the virtual environment
call "%venv_path%\Scripts\activate.bat"

:: Install required dependencies (if any)
pip install --upgrade pip

:: Get the full path of the dropped file (the first argument)
set "file_path=%~1"
echo File path is "%file_path%"
:: Check if a file path was provided
if "%file_path%"=="" (
    echo No file was provided. Please drag and drop a file onto this batch file.
    goto :keepopen
)

:: Run the Python script with the file path as an argument
python "%script_dir%main.py" "%file_path%"

:keepopen
echo Script execution completed.
echo Press any key to exit...
pause >nul
exit /b