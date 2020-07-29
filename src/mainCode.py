import updateMovimentos as up
import pyodbc as db
import pandas as pd

conn = db.connect('Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;Trusted_Connection=yes')
fundos = pd.read_sql_query('select CODFUND from FIQs', conn)


for codfund in fundos.CODFUND:
    print('Atualizando {}'.format(codfund))
    up.update_movimentos(codfund)

movimentos = pd.read_sql_query('select * from Movimentacoes', conn)
movimentos = movimentos.sort_values(['COTIZACAO', 'CODFUND'], ascending = (True,True))
movimentos.to_csv('O:\CAIXAS\FLUXO\Movimentacoes - Gerencial.csv', index=False)
conn.close()
