@echo off
echo ========================================
echo  UPLOAD DE ARQUIVOS PARA UM REPOSITORIO GITHUB
echo  Usuario: evandromelo
echo ========================================
echo.

REM Solicita o nome do repositório
set /p repo=Digite o nome do repositorio (ex.: python_intr_dados): 

REM 1. Inicializa repositório (caso não exista)
if not exist ".git" (
    git init
    echo Repositorio Git inicializado.
)

REM 2. Define branch principal
git branch -M main

REM 3. Conecta ao repositório remoto
git remote remove origin >nul 2>&1
git remote add origin https://github.com/evandromelo/%repo%.git
echo Repositorio remoto configurado: https://github.com/evandromelo/%repo%.git

REM 4. Adiciona todos os arquivos
git add .
echo Arquivos adicionados.

REM 5. Cria commit
set /p msg=Digite a mensagem do commit: 
if "%msg%"=="" set msg=Upload inicial
git commit -m "%msg%" || echo Nenhuma alteracao para commitar.

REM 6. Faz o push para o GitHub
git push -u origin main

echo.
echo ========================================
echo  UPLOAD CONCLUIDO!
echo ========================================
pause
