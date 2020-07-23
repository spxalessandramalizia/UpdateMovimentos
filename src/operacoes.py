import resgatesTotais as rt
import numpy as np

def atualiza_resgates_cotas(cota, mov):
    mov.loc[mov.OPERACAO=='RC', 'FINANCEIRO'] = mov[mov.OPERACAO=='RC'].COTAS_SOLICITADO*cota
    # print('Resgates por cotas (financeiro): ')
    # print(mov[mov.OPERACAO=='RC'].FINANCEIRO)
    return

def atualiza_aplicacoes(cota, mov):
    mov.loc[mov.OPERACAO=='A', 'COTAS_PREVISTO'] = mov[mov.OPERACAO=='A'].FINANCEIRO/cota
    # print('Aplicações (cotas): ')
    # print(mov[mov.OPERACAO=='A'])
    return

def atualiza_resgates_financeiros(cota, mov):
    mov.loc[mov.OPERACAO=='R', 'COTAS_PREVISTO'] = mov[mov.OPERACAO=='R'].FINANCEIRO/cota
    # print('Resgates financeiros (cotas): ')
    # print(mov[mov.OPERACAO=='R'])
    return

def copia_cotas(data_ref, mov_origem, mov_destino):
    mov_origem.set_index(mov_destino[mov_destino.COTIZACAO>=data_ref].index, inplace=True)
    mov_destino.loc[mov_destino.COTIZACAO>=data_ref, 'COTAS_PREVISTO'] = mov_origem.COTAS_PREVISTO
    # print('mov_saldos atualizada:')
    # print(mov_destino)
    return

def recalcula_resgates_totais(mov, codfund, data_saldos, conn):
    resgates_totais = mov[(mov.OPERACAO=='RT') & (mov.COTIZACAO>=data_saldos) & (mov.CAUTELA==0)].copy()
    rt.compara_saldos(resgates_totais, codfund, conn)
    resgates_totais.set_index(mov[(mov.OPERACAO=='RT') & (mov.COTIZACAO>=data_saldos) & (mov.CAUTELA==0)].index, inplace=True)
    mov.loc[((mov.OPERACAO=='RT') & (mov.COTIZACAO>=data_saldos) & (mov.CAUTELA==0)),'COTAS_PREVISTO'] = resgates_totais.COTAS_PREVISTO
    return

def atualiza_resgates_totais(cota, mov, mov_saldos):
    resgates_totais = mov[(mov.OPERACAO=='RT') & (mov.CAUTELA==0)].copy()    
    rt.verifica_intervalo(resgates_totais, mov_saldos)
    rt.calcula_financeiro(cota, resgates_totais)

    resgates_totais.set_index(mov[(mov.OPERACAO=='RT') & (mov.CAUTELA==0)].index, inplace=True)
    mov.loc[((mov.OPERACAO=='RT') & (mov.CAUTELA==0)),'COTAS_PREVISTO'] = resgates_totais.COTAS_PREVISTO
    mov.loc[((mov.OPERACAO=='RT') & (mov.CAUTELA==0)),'FINANCEIRO'] = resgates_totais.FINANCEIRO
    
    # print('Resgates totais (cotas): ')
    # print(resgates_totais.COTAS_PREVISTO)
    # print(mov[(mov.OPERACAO=='RT') & (mov.CAUTELA==0)])    
    
    # print('Resgates totais (financeiro): ')
    # print(resgates_totais.FINANCEIRO)
    # print(mov[(mov.OPERACAO=='RT') & (mov.CAUTELA==0)])
    return

def atualiza_resgates_totais_por_cautela(): pass
    #compara resgates totais por cautela com saldo das cautelas
