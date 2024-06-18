@echo off
setlocal

REM Set variables
set PYINSTALLER=pyinstaller
set SPEC_FILE=test.spec
set DIST_DIR=dist
set EXECUTABLE=test.exe

REM Step 1: Clean previous builds (optional)
if exist %DIST_DIR% (
    echo Cleaning previous builds...
    rmdir /S /Q %DIST_DIR%
)

REM Step 2: Build the executable with PyInstaller using the .spec file
echo Building the executable...
%PYINSTALLER% %SPEC_FILE%

REM Step 3: Move to the distribution directory
echo Navigating to distribution directory...
cd %DIST_DIR%

REM Step 4: Run the executable
echo Running the executable...
%EXECUTABLE%

REM Step 5: Additional future steps can be added here
REM echo Running additional build steps...

endlocal
pause
