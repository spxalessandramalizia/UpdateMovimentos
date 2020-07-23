# update movimentos  
echo Ativando venv
CALL ..\venv\Scripts\activate.bat

echo Executando script
python ..\src\mainCode.py

echo Desativando venv
CALL ..\venv\Scripts\deactivate.bat