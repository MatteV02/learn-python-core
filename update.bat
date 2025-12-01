@echo off
setlocal enabledelayedexpansion

:: URL del repository Git (ZIP)
set "repoUrl=https://github.com/MatteV02/learn-python-core/archive/refs/heads/master.zip"
:: Nome del file ZIP scaricato
set "zipFile=%~dp0repo_update_temp.zip"
:: Cartella di estrazione temporanea
set "tempDir=%~dp0repo_update_temp"

:: 1. Scarica il repository come ZIP usando curl
echo Scaricamento del repository...
curl -L -o "%zipFile%" "%repoUrl%"
if %errorlevel% neq 0 (
    echo Errore durante il download del repository.
    pause
    exit /b 1
)

:: 2. Estrai il contenuto del ZIP usando PowerShell
echo Estrazione del repository...
powershell -command "Expand-Archive -Path '%zipFile%' -DestinationPath '%tempDir%' -Force"
if %errorlevel% neq 0 (
    echo Errore durante l'estrazione del repository.
    pause
    exit /b 1
)

:: 3. Trova la cartella principale all'interno dell'archivio
set "extractedDir="
for /d %%d in ("%tempDir%\*") do (
    set "extractedDir=%%d"
    goto :foundDir
)
:foundDir
if not defined extractedDir (
    echo Nessuna cartella trovata nell'archivio.
    pause
    exit /b 1
)

:: 4. Verifica se esiste una nuova versione dello script
set "newScriptPath=%extractedDir%\update_repo.bat"
if exist "!newScriptPath!" (
    :: Confronta i file: se sono diversi, aggiorna lo script
    fc /b "%~f0" "!newScriptPath!" >nul
    if !errorlevel! equ 1 (
        echo Trovata una versione aggiornata dello script. Autoaggiornamento in corso...
        copy /Y "!newScriptPath!" "%~f0" >nul
        echo Script autoaggiornato. Riavvia lo script per applicare le modifiche.
        pause
        exit /b 0
    )
)

:: 5. Estrai il contenuto del ZIP usando PowerShell
echo Estrazione del repository...
powershell -command "Expand-Archive -Path '%zipFile%' -DestinationPath '%tempDir%' -Force"
if %errorlevel% neq 0 (
    echo Errore durante l'estrazione del repository.
    pause
    exit /b 1
)

:: 6. Trova la cartella principale all'interno dell'archivio
set "extractedDir="
for /d %%d in ("%tempDir%\*") do (
    set "extractedDir=%%d"
    goto :foundDir2
)
:foundDir2
if not defined extractedDir (
    echo Nessuna cartella trovata nell'archivio.
    pause
    exit /b 1
)

:: 7. Copia i file nella cartella corrente (sovrascrivendo)
echo Aggiornamento dei file...
xcopy "!extractedDir!\*" "%~dp0" /E /Y /Q
if %errorlevel% neq 0 (
    echo Errore durante la copia dei file.
    pause
    exit /b 1
)

:: 8. Pulizia dei file temporanei
echo Pulizia dei file temporanei...
del /f /q "%zipFile%" >nul 2>&1
rmdir /s /q "%tempDir%" >nul 2>&1

:: 9. Fine
echo Aggiornamento completato con successo!
pause
