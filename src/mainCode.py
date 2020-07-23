import UpdateMovimentos as up
import pyodbc as db
import pandas as pd

conn = db.connect('Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;Trusted_Connection=yes')

fundos = pd.read_sql_query('select CODFUND from FIQs', conn)
for codfund in fundos.values:
    #imprimir log
    update_movimentos(codfund)