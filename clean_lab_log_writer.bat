@echo off
setlocal

set "REPO_ROOT=%~dp0"
set "PS_SCRIPT=%REPO_ROOT%clean_lab_log_writer.ps1"

echo Cleaning stale Lab Log Writer server instances...

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

if errorlevel 1 (
  echo Failed to clean one or more server instances.
  exit /b 1
)

echo Cleanup complete.
exit /b 0
