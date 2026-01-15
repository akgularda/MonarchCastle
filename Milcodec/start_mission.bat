@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM MILCODEC MISSION LAUNCHER v2.0
REM Secure Communications Platform
REM ═══════════════════════════════════════════════════════════════════════════

title MILCODEC MISSION CONTROL

echo.
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                    MILCODEC SYSTEM v2.0                               ║
echo  ║              COVERT SIGNALING PLATFORM                                ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo  [1] Night Watch  - Receiver Terminal (Field Unit)
echo  [2] Glass Cockpit - Commander Terminal (C2)
echo  [3] Studio       - Audio Steganography Suite
echo  [4] Full Mission - Launch Receiver + Commander
echo  [5] Install Dependencies
echo  [Q] Exit
echo.

set /p choice="SELECT OPTION: "

if "%choice%"=="1" goto receiver
if "%choice%"=="2" goto commander
if "%choice%"=="3" goto studio
if "%choice%"=="4" goto full
if "%choice%"=="5" goto install
if /i "%choice%"=="Q" goto end
goto end

:receiver
echo.
echo [+] Launching Night Watch Receiver...
start "MILCODEC RECEIVER" python milcodec_receiver.py
goto end

:commander
echo.
echo [+] Launching Glass Cockpit Commander...
start "MILCODEC COMMANDER" python milcodec_commander.py
goto end

:studio
echo.
echo [+] Launching Milcodec Studio...
start "MILCODEC STUDIO" python milcodec_studio.py
goto end

:full
echo.
echo [+] Launching Full Mission Configuration...
echo [+] Starting Receiver...
start "MILCODEC RECEIVER" python milcodec_receiver.py
timeout /t 2 >nul
echo [+] Starting Commander...
start "MILCODEC COMMANDER" python milcodec_commander.py
echo.
echo [+] Mission deployed. Both terminals are active.
goto end

:install
echo.
echo [+] Installing Dependencies...
pip install -r requirements.txt
echo.
echo [+] Dependencies installed.
pause
goto end

:end
echo.
echo [+] MILCODEC Mission Control - Session Complete
