# update movimentos  
echo Ativando venv
CALL ..\venv\Scripts\activate.bat

echo Executando script
python ..\src\mainCode.py
python ..\src\build_movimentacoes.py

echo Desativando venv
CALL ..\venv\Scripts\deactivate.bat