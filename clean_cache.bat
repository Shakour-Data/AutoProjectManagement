@echo off
echo ========================================
echo      CACHE CLEANER FOR WINDOWS
echo ========================================
echo.
echo This script will clean common cache files
echo that are safe to remove from your C: drive
echo.
echo WARNING: Running as Administrator recommended
echo.
pause

echo.
echo Cleaning Temporary Files...
echo.

:: Clean Windows Temp folder
if exist "C:\Windows\Temp\*" (
    echo Cleaning Windows Temp folder...
    del /q /f /s "C:\Windows\Temp\*"
    for /d %%x in ("C:\Windows\Temp\*") do rd /s /q "%%x"
)

:: Clean User Temp folder
if exist "%TEMP%\*" (
    echo Cleaning User Temp folder...
    del /q /f /s "%TEMP%\*"
    for /d %%x in ("%TEMP%\*") do rd /s /q "%%x"
)

:: Clean Prefetch files (safe to clean)
if exist "C:\Windows\Prefetch\*" (
    echo Cleaning Prefetch files...
    del /q /f /s "C:\Windows\Prefetch\*"
)

:: Clean Internet Explorer cache
if exist "%LOCALAPPDATA%\Microsoft\Windows\INetCache\*" (
    echo Cleaning IE Cache...
    del /q /f /s "%LOCALAPPDATA%\Microsoft\Windows\INetCache\*"
    for /d %%x in ("%LOCALAPPDATA%\Microsoft\Windows\INetCache\*") do rd /s /q "%%x"
)

:: Clean Windows Update cache
if exist "C:\Windows\SoftwareDistribution\Download\*" (
    echo Cleaning Windows Update cache...
    del /q /f /s "C:\Windows\SoftwareDistribution\Download\*"
)

:: Clean Thumbnail cache
if exist "%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db" (
    echo Cleaning Thumbnail cache...
    del /q /f "%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db"
)

echo.
echo Cleaning Browser Caches...
echo.

:: Chrome cache
if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\*" (
    echo Cleaning Chrome cache...
    del /q /f /s "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\*"
    for /d %%x in ("%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\*") do rd /s /q "%%x"
)

:: Firefox cache
if exist "%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*\cache2\*" (
    echo Cleaning Firefox cache...
    del /q /f /s "%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*\cache2\*"
    for /d %%x in ("%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*\cache2\*") do rd /s /q "%%x"
)

:: Edge cache
if exist "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\*" (
    echo Cleaning Edge cache...
    del /q /f /s "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\*"
    for /d %%x in ("%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\*") do rd /s /q "%%x"
)

echo.
echo Cleaning Application Caches...
echo.

:: Adobe cache
if exist "%LOCALAPPDATA%\Adobe\Common\Media Cache\*" (
    echo Cleaning Adobe cache...
    del /q /f /s "%LOCALAPPDATA%\Adobe\Common\Media Cache\*"
    for /d %%x in ("%LOCALAPPDATA%\Adobe\Common\Media Cache\*") do rd /s /q "%%x"
)

:: Spotify cache
if exist "%LOCALAPPDATA%\Spotify\Data\*" (
    echo Cleaning Spotify cache...
    del /q /f /s "%LOCALAPPDATA%\Spotify\Data\*"
)

echo.
echo Running Disk Cleanup...
echo.

:: Run built-in Windows Disk Cleanup for system files
cleanmgr /sagerun:1

echo.
echo ========================================
echo      CACHE CLEANUP COMPLETED
echo ========================================
echo.
echo Summary of cleaned locations:
echo - Windows Temp folders
echo - User Temp folders  
echo - Prefetch files
echo - Browser caches (Chrome, Firefox, Edge)
echo - Windows Update cache
echo - Thumbnail cache
echo - Application caches
echo - System files via Disk Cleanup
echo.
echo Note: Some files may be in use and couldn't be deleted.
echo       You may need to restart and run again.
echo.
pause
