@echo off
echo ========================================
echo  ATUALIZAR REPOSITORIO GITHUB EXISTENTE
echo  Usuario: evandromelo
echo ========================================
echo.

REM Solicita o nome do repositório
set /p repo=Digite o nome do repositorio (ex.: cd_1): 

REM 1. Conecta ao repositório remoto
git remote remove origin >nul 2>&1
git remote add origin https://github.com/evandromelo/%repo%.git
echo Repositorio remoto configurado: https://github.com/evandromelo/%repo%.git

REM 2. Adiciona todos os arquivos modificados
git add .
echo Arquivos adicionados.

REM 3. Cria commit (se houver alterações)
set /p msg=Digite a mensagem do commit: 
if "%msg%"=="" set msg=Atualizacao automatica
git commit -m "%msg%" || echo Nenhuma alteracao para commitar.

REM 4. Envia para o GitHub
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  ATUALIZACAO CONCLUIDA!
echo ========================================
pause
