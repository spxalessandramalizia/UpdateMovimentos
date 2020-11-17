import pandas as pd
import pyodbc as db
import numpy as np
import sqlalchemy as sql

### Config ###
full_data_path = "O:\CAIXAS\FLUXO\Movimentacoes - Gerencial.csv"
ri_data_path = "O:\CAIXAS\FLUXO\Movimentações Histórica.xlsm"
sql_server_string = "Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;Trusted_Connection=yes"
mysql_string = "malizia:1234@192.168.1.57/irdb"

### Controle Data ###
raw_data = pd.read_csv(full_data_path)[['CODFUND','SOLICITACAO','COTIZACAO','OPERACAO','FINANCEIRO','ALOCADOR']]

### RI Data ###
data = pd.read_excel(ri_data_path,skiprows = 1)
data = data[['CODIGO.1','MASTER','SOLICITAÇÃO','QUOTIZAÇÃO','OP','FINANCEIRO','ALOCADOR']]
data.rename(columns = {'CODIGO.1':'CODFUND','SOLICITAÇÃO':'SOLICITACAO','QUOTIZAÇÃO':'COTIZACAO','OP':'OPERACAO'},inplace = True)
data.SOLICITACAO = data.SOLICITACAO.apply(lambda x: x.strftime("%Y-%m-%d"))
data.COTIZACAO = data.COTIZACAO.apply(lambda x: x.strftime("%Y-%m-%d"))

### Dicionario FUNDO -> MASTER ###
conn = db.connect(sql_server_string)
masters = {61921:'PATRIOT',61922:'FALCON',61923:'APACHE',61981:'NIMITZ',61984:'RAPTOR',63056:'LANCER',64480:'SEAHAWK'}

map_funds = data.copy()[['CODFUND','MASTER']].set_index('CODFUND')['MASTER'].to_dict()
map_funds_2 = pd.read_sql("SELECT CODFUND, CODMASTER FROM FIQS", conn).set_index('CODFUND').loc[:,'CODMASTER'].apply(lambda x: masters[x]).to_dict()
map_funds.update(map_funds_2)

### Merge Databases ###
data_max = data.COTIZACAO.max()
data_min = data.COTIZACAO.min()

### Dados da base bruta anterior a 2016 e posterior a ultima data da base validada 
raw_data = raw_data[(raw_data.COTIZACAO < data_min) | (raw_data.COTIZACAO > data_max)]
raw_data['MASTER'] = raw_data.CODFUND.apply(lambda x: map_funds[x])

### Concat databases ###
merge_data = pd.concat([data,raw_data],sort=True).groupby(['COTIZACAO','SOLICITACAO','MASTER','ALOCADOR','OPERACAO'])[["FINANCEIRO"]].sum().reset_index()
merge_data.loc[merge_data.OPERACAO != 'A','OPERACAO'] = 'RESGATE'
merge_data.loc[merge_data.OPERACAO == 'A','OPERACAO'] = 'APLICACAO'

### Pivot Data ###
pivot_table = pd.pivot_table(merge_data, values='FINANCEIRO', index=['COTIZACAO','SOLICITACAO','MASTER','ALOCADOR'],columns=['OPERACAO'], aggfunc=np.sum)/1000000
pivot_table = pivot_table.round(3).reset_index().fillna(0)
pivot_table = pivot_table[~((pivot_table.APLICACAO == 0) & (pivot_table.RESGATE == 0))]
pivot_table['NET'] = pivot_table['APLICACAO'] - pivot_table['RESGATE']


### Conect MySQL / Replace Data ###
connection = sql.create_engine(f"mysql+pymysql://{mysql_string}").connect()
connection.execute("DELETE FROM master_mov")
pivot_table.to_sql(name = 'master_mov',con = connection,index = False,if_exists = 'append')