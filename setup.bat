@echo off
echo Criando ambiente virtual...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Erro ao criar ambiente virtual. Certifique-se de que o Python 3.12.0 está instalado.
    pause
    exit /b %ERRORLEVEL%
)

echo Ativando ambiente virtual...
call .\venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Erro ao ativar ambiente virtual.
    pause
    exit /b %ERRORLEVEL%
)

echo Instalando dependencias...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Erro ao instalar dependencias. Verifique o requirements.txt.
    pause
    exit /b %ERRORLEVEL%
)

echo Instalando navegadores do Playwright...
playwright install
if %ERRORLEVEL% neq 0 (
    echo Erro ao instalar navegadores do Playwright.
    pause
    exit /b %ERRORLEVEL%
)

echo Configuracao concluida! Execute o projeto com: python export_qlik_tables.py
pause