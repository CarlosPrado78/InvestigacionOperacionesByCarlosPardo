@echo off
REM Genera el ejecutable de Windows:
REM   dist\Investigación de Operaciones By Carlos Pardo.exe
setlocal
cd /d "%~dp0"
chcp 65001 >nul

where py >nul 2>nul
if %errorlevel%==0 (
  set "PYTHON=py -3"
) else (
  set "PYTHON=python"
)

if not exist ".venv-build" (
  %PYTHON% -m venv .venv-build
)
call ".venv-build\Scripts\activate.bat"

python -m pip install --upgrade pip
python -m pip install "pyinstaller>=6.10"

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller --noconfirm --clean --windowed --onefile --name "InvestigacionOperaciones" main.py

if not exist "dist\InvestigacionOperaciones.exe" (
  echo La compilacion no genero el ejecutable.
  exit /b 1
)

REM Renombrar con el nombre visible de la aplicacion. El nombre esta en un
REM archivo UTF-8, asi la consola no interviene.
python tools\rename_exe.py
if errorlevel 1 (
  echo No se pudo renombrar el ejecutable.
  exit /b 1
)
pause
