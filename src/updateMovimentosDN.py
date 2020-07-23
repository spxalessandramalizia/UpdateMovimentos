import pyodbc as db
import numpy as np
import pandas as pd
import utils
from datetime import datetime
from sqlalchemy import create_engine
import urllib

def update_fundo(codfund, mov):
    quoted = urllib.parse.quote_plus('Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;')
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
    engine.execute('delete Movimentacoes where CODFUND = {} AND COTIZACAO >= \'{}\' AND COTIZACAO <= \'{}\''.format(str(codfund), utils.data_to_string(datetime(2020,7,1)), utils.data_to_string(datetime(2020,7,16))))
    mov.to_sql('Movimentacoes', schema='dbo', con=engine, if_exists='append', index=False)

conn = db.connect('Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;Trusted_Connection=yes')

movimentos_query = 'select * from Movimentacoes where COTIZACAO >= \'{}\' AND COTIZACAO <= \'{}\''.format(utils.data_to_string(datetime(2020,7,1)), utils.data_to_string(datetime(2020,7,16)))
mov = pd.read_sql_query(movimentos_query, conn)

fundos = mov['CODFUND'].unique()
for codfund in fundos:
    datas = mov[mov.CODFUND==codfund].COTIZACAO.unique()
    mov_fundo = mov.loc[mov.CODFUND==codfund]
    for data in datas:
        cota = utils.get_cota(codfund, data, conn)
        resgates_totais = mov_fundo.loc[(mov_fundo.OPERACAO=='RT') & (mov_fundo.COTIZACAO==data), 'COTAS_PREVISTO'] * cota
        resgates_cota = mov_fundo.loc[(mov_fundo.OPERACAO=='RC') & (mov_fundo.COTIZACAO==data), 'COTAS_PREVISTO'] * cota
        
        if len(resgates_totais)!=0:
            print('atualizaou totais {}'.format(str(codfund)))
            mov_fundo.loc[(mov_fundo.OPERACAO=='RT') & (mov_fundo.COTIZACAO==data), 'FINANCEIRO'] = resgates_totais
            print(cota)
            print(resgates_totais)
            print(mov_fundo)

        if len(resgates_cota)!=0:
            mov_fundo.loc[(mov_fundo.OPERACAO=='RC') & (mov_fundo.COTIZACAO==data), 'FINANCEIRO'] = resgates_cota
            print('atualizaou cotas {}'.format(str(codfund)))
    update_fundo(codfund, mov_fundo)

conn.close()