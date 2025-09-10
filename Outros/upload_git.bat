@echo off
echo ========================================
echo  UPLOAD DE ARQUIVOS PARA O GITHUB
echo  Repositorio: https://github.com/evandromelo/python_intr_dados.git
echo ========================================
echo.

REM 1. Inicializa repositório (caso não exista)
if not exist ".git" (
    git init
    echo Repositorio Git inicializado.
)

REM 2. Define branch principal
git branch -M main

REM 3. Conecta ao repositório remoto
git remote remove origin >nul 2>&1
git remote add origin https://github.com/evandromelo/python_intr_dados.git
echo Repositorio remoto configurado.

REM 4. Adiciona todos os arquivos
git add .
echo Arquivos adicionados.

REM 5. Cria commit
git commit -m "Upload inicial das aulas e datasets"
echo Commit criado.

REM 6. Faz o push para o GitHub
git push -u origin main
echo.
echo ========================================
echo  UPLOAD CONCLUIDO!
echo ========================================
pause
