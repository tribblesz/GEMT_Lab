@echo off
setlocal

set "REPO_ROOT=%~dp0"

pushd "%REPO_ROOT%" >nul

call "%REPO_ROOT%clean_lab_log_writer.bat"
if errorlevel 1 (
  popd >nul
  exit /b 1
)

echo Starting Lab Log Writer...
call "%REPO_ROOT%tools\lab-log-writer\start_writer.bat"
set "EXIT_CODE=%ERRORLEVEL%"

popd >nul
exit /b %EXIT_CODE%
