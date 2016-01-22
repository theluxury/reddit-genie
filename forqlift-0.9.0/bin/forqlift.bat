@REM - - - - - - - - - - - - - - - - - - - -
@REM
@REM Copyright 2010-2012 Ethan McCallum, ExMachinaTech.net.
@REM
@REM Licensed under the Apache License, Version 2.0 (the "License");
@REM you may not use this file except in compliance with the License.
@REM You may obtain a copy of the License at
@REM
@REM      http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing, software
@REM distributed under the License is distributed on an "AS IS" BASIS,
@REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM See the License for the specific language governing permissions and
@REM limitations under the License.
@REM
@REM - - - - - - - - - - - - - - - - - - - -


@REM This script lifts a lot of material from the Maven ("mvn.bat") launch script.
@REM Thank you, Maven team!


@REM ----------------------------------------------------------------------------
@REM forqlift Start Up Batch script
@REM
@REM Required ENV vars:
@REM JAVA_HOME - location of a JDK home dir
@REM
@REM Optional ENV vars
@REM FORQLIFT_HOME - location of forqlift's installed home dir
@REM FORQLIFT_BATCH_ECHO - set to 'on' to enable the echoing of the batch commands
@REM FORQLIFT_BATCH_PAUSE - set to 'on' to wait for a key stroke before ending
@REM FORQLIFT_OPTS - parameters passed to the Java VM when running forqlift
@REM     e.g. to debug forqlift itself, use
@REM set FORQLIFT_OPTS=-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000
@REM ----------------------------------------------------------------------------

@REM Begin all REM lines with '@' in case FORQLIFT_BATCH_ECHO is 'on'
@echo off
@REM enable echoing my setting FORQLIFT_BATCH_ECHO to 'on'
@if "%FORQLIFT_BATCH_ECHO%" == "on"  echo %FORQLIFT_BATCH_ECHO%

@REM set %HOME% to equivalent of $HOME
if "%HOME%" == "" (set "HOME=%HOMEDRIVE%%HOMEPATH%")

@REM Execute a user defined script before this one
if exist "%HOME%\forqliftrc_pre.bat" call "%HOME%\forqliftrc_pre.bat"

set FORQLIFT_MAIN_CLASS="forqlift.ui.Driver"

set ERROR_CODE=0

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal
if "%OS%"=="WINNT" @setlocal

@REM ==== START VALIDATION ====
if not "%JAVA_HOME%" == "" goto OkJHome

echo.
echo ERROR: JAVA_HOME not found in your environment.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation
echo.
goto error

:OkJHome
if exist "%JAVA_HOME%\bin\java.exe" goto chkMHome

echo.
echo ERROR: JAVA_HOME is set to an invalid directory.
echo JAVA_HOME = "%JAVA_HOME%"
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation
echo.
goto error

:chkMHome
if not "%FORQLIFT_HOME%"=="" goto valMHome

if "%OS%"=="Windows_NT" SET "FORQLIFT_HOME=%~dp0.."
if "%OS%"=="WINNT" SET "FORQLIFT_HOME=%~dp0.."
if not "%FORQLIFT_HOME%"=="" goto valMHome

echo.
echo ERROR: FORQLIFT_HOME not found in your environment.
echo Please set the FORQLIFT_HOME variable in your environment to match the
echo location of the forqlift installation
echo.
goto error

:valMHome

:stripMHome
if not "_%FORQLIFT_HOME:~-1%"=="_\" goto checkMBat
set "FORQLIFT_HOME=%FORQLIFT_HOME:~0,-1%"
goto stripMHome

:checkMBat
if exist "%FORQLIFT_HOME%\bin\forqlift.bat" goto init

echo.
echo ERROR: FORQLIFT_HOME is set to an invalid directory.
echo FORQLIFT_HOME = "%FORQLIFT_HOME%"
echo Please set the FORQLIFT_HOME variable in your environment to match the
echo location of the forqlift installation
echo.
goto error
@REM ==== END VALIDATION ====

:init

@REM build up the classpath based on existing JARs
setLocal EnableDelayedExpansion
set CLASSPATH="%FORQLIFT_HOME%\conf"

for %%J in ("%FORQLIFT_HOME%"\lib.base\*.jar) do (
    set CLASSPATH=!CLASSPATH!;%%J%
)

for %%J in ("%FORQLIFT_HOME%"\lib.ext\*.jar) do (
    set CLASSPATH=!CLASSPATH!;%%J%
)


@REM Decide how to startup depending on the version of windows

@REM -- Windows NT with Novell Login
if "%OS%"=="WINNT" goto WinNTNovell

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

:WinNTNovell

@REM -- 4NT shell
if "%@eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set FORQLIFT_CMD_LINE_ARGS=%*
goto endInit

@REM The 4NT Shell from jp software
:4NTArgs
set FORQLIFT_CMD_LINE_ARGS=%$
goto endInit

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of agruments (up to the command line limit, anyway).
set FORQLIFT_CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto endInit
set FORQLIFT_CMD_LINE_ARGS=%FORQLIFT_CMD_LINE_ARGS% %1
shift
goto Win9xApp

@REM Reaching here means variables are defined and arguments have been captured
:endInit
SET FORQLIFT_JAVA_EXE="%JAVA_HOME%\bin\java.exe"

%FORQLIFT_JAVA_EXE% %FORQLIFT_OPTS% "-Dforqlift.home=%FORQLIFT_HOME%" %FORQLIFT_MAIN_CLASS% %FORQLIFT_CMD_LINE_ARGS%
if ERRORLEVEL 1 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
if "%OS%"=="WINNT" @endlocal
set ERROR_CODE=1

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT
if "%OS%"=="WINNT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set FORQLIFT_JAVA_EXE=
set FORQLIFT_CMD_LINE_ARGS=
goto postExec

:endNT
@endlocal & set ERROR_CODE=%ERROR_CODE%

:postExec
if exist "%HOME%\forqliftrc_post.bat" call "%HOME%\forqliftrc_post.bat"
@REM pause the batch file if FORQLIFT_BATCH_PAUSE is set to 'on'
if "%FORQLIFT_BATCH_PAUSE%" == "on" pause

if "%FORQLIFT_TERMINATE_CMD%" == "on" exit %ERROR_CODE%

cmd /C exit /B %ERROR_CODE%



