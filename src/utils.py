

import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import urllib

def data_to_string(data):
    return data.strftime('%Y-%m-%d')

def get_data(codfund, conn):
    max_data_query = 'select max(DATA) from Cotas where CODFUND = {}'.format(str(codfund))
    data = pd.read_sql_query(max_data_query, conn)
    return pd.to_datetime(data.iloc[0])[0]

def get_cota(codfund, data, conn):    
    cota_query = 'select COTA from Cotas where CODFUND = {} and DATA = \'{}\''.format(str(codfund), data_to_string(data)) #data_to_string(data)
    cota = pd.read_sql_query(cota_query, conn)
    return cota.iloc[0]['COTA']

def get_movimentos(codfund, data, conn):
    movimentos_query = 'select * from Movimentacoes where CODFUND = {} AND COTIZACAO >= \'{}\''.format(str(codfund), data_to_string(data))
    mov = pd.read_sql_query(movimentos_query, conn)
    mov['COTIZACAO'] = pd.to_datetime(mov['COTIZACAO'])
    return mov

def get_saldos(cotistas, codfund, conn):
    #trocar para saldo até o dia de solicitação do resgate
    saldos_query = 'select CODCOT, DTLANCT, QNTCOTAS from Saldos2 where CODFUND = {} and TIPOREGISTRO = \'Simples\''.format(codfund)
    saldos = pd.read_sql_query(saldos_query, conn)
    saldos['DTLANCT'] = pd.to_datetime(saldos['DTLANCT'])
    # saldos = pd.Series(saldos.QNTCOTAS, name='COTAS_PREVISTO', index = saldos.index)
    return saldos

def get_data_saldos(conn):
    #retorna primeiro dia que não está sendo considerado na saldos
    query =  'select max(DTAPROCE) from saldos'
    data = pd.read_sql_query(query, conn)
    return pd.to_datetime(data.iloc[0])[0]

def get_cautelas(num_cautelas, conn): pass

def set_movimentos(codfund, data, mov):
    quoted = urllib.parse.quote_plus('Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;')
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
    engine.execute('delete Movimentacoes where CODFUND = {} AND COTIZACAO >= \'{}\''.format(str(codfund), data_to_string(data)))
    mov.to_sql('Movimentacoes', schema='dbo', con=engine, if_exists='append', index=False)
