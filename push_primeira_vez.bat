@echo off
REM =======================================================
REM Script para subir um diretório local ao GitHub (1ª vez)
REM Usuário: evandromelo
REM Email:   evandro.cm@gmail.com
REM Repo:    https://github.com/evandromelo/cd_2.git
REM =======================================================

echo.
echo === Configurando Git no repositório local ===
git init

git config user.name "evandromelo"
git config user.email "evandro.cm@gmail.com"

echo.
echo === Adicionando todos os arquivos ===
git add .

echo.
echo === Criando o primeiro commit ===
git commit -m "Primeiro commit - upload inicial do projeto"

echo.
echo === Definindo repositório remoto ===
git remote add origin https://github.com/evandromelo/cd_2.git

echo.
echo === Enviando arquivos para o GitHub (branch main) ===
git branch -M main
git push -u origin main

echo.
echo =======================================================
echo Projeto enviado com sucesso para o GitHub!
pause
