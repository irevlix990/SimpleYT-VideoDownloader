@echo off
REM Launcher YT Downloader

:check_python
where python >nul 2>&1
if %errorlevel% neq 0 (
	echo python tidak ditemukan! pastikan python sudah terinstall
	pause
	exit /b 1
)

:run_app
if not exist "yt_downloader.py" (
	echo file tidak ditemukan!
	pause
	exit /b 1
)

echo Menjalankan aplikasi...
python yt_downloader.py
pause