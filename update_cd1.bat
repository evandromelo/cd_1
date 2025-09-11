@echo off
echo ========================================
echo  ATUALIZAR REPOSITORIO cd_1 NO GITHUB
echo  URL: https://github.com/evandromelo/cd_1
echo ========================================
echo.

REM 1. Configura identidade se ainda não existir
git config user.name >nul 2>&1
if errorlevel 1 (
    set /p gitname=Digite seu nome do GitHub: 
    git config --global user.name "%gitname%"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    set /p gitemail=Digite seu email do GitHub: 
    git config --global user.email "%gitemail%"
)

REM 2. Conecta ao repositório remoto
git remote remove origin >nul 2>&1
git remote add origin https://github.com/evandromelo/cd_1.git
echo Repositorio remoto configurado.

REM 3. Adiciona todos os arquivos modificados
git add .
echo Arquivos adicionados.

REM 4. Cria commit (se houver alterações)
set /p msg=Digite a mensagem do commit: 
if "%msg%"=="" set msg=Atualizacao automatica
git commit -m "%msg%" || echo Nenhuma alteracao para commitar.

REM 5. Envia para o GitHub
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  ATUALIZACAO CONCLUIDA!
echo ========================================
pause
