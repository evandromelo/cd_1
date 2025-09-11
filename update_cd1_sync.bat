@echo off
echo ========================================
echo  ATUALIZAR REPOSITORIO GITHUB (SINCRONIZADO)
echo  Usuario: evandromelo
echo  Email:   evandro.cm@gmail.com
echo ========================================
echo.

REM 1. Configura identidade (global, caso ainda não esteja definida)
git config --global user.name "evandromelo"
git config --global user.email "evandro.cm@gmail.com"

REM 2. Conecta ao repositório remoto
git remote remove origin >nul 2>&1
git remote add origin https://github.com/evandromelo/cd_1.git
echo Repositorio remoto configurado: https://github.com/evandromelo/cd_1.git

REM 3. Adiciona todos os arquivos modificados
git add .
echo Arquivos adicionados.

REM 4. Cria commit (se houver alterações)
set /p msg=Digite a mensagem do commit: 
if "%msg%"=="" set msg=Atualizacao automatica
git commit -m "%msg%" || echo Nenhuma alteracao para commitar.

REM 5. Faz pull com rebase para sincronizar antes de enviar
echo Sincronizando com GitHub...
git pull origin main --rebase

REM 6. Envia para o GitHub
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  ATUALIZACAO CONCLUIDA!
echo ========================================
pause
