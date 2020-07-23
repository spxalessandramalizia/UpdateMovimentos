import utils
import pandas as pd

def get_cotas_saldos(codcot, solicitacao, cautelas):
    cotas = cautelas[(cautelas.CODCOT==codcot) & (cautelas.DTLANCT<=solicitacao)].QNTCOTAS.sum()
    return cotas

#recalcula resgates totais com saldo dos cotistas até a solicitação do resgate
def compara_saldos(resgates, codfund, conn):
    cotistas = resgates.CODCOT.unique()
    cautelas = utils.get_saldos(cotistas, codfund, conn)
    cotas_saldos = [get_cotas_saldos(codcot, solicitacao, cautelas) for codcot, solicitacao in zip(resgates.CODCOT, resgates.SOLICITACAO)]
    idx = pd.MultiIndex.from_arrays([resgates.CODCOT, resgates.SOLICITACAO])
    saldos = pd.DataFrame(cotas_saldos, columns=['COTAS_PREVISTO'], index=idx)

    resgates.set_index(['CODCOT', 'SOLICITACAO'], inplace=True)
    resgates['COTAS_PREVISTO'] = saldos.COTAS_PREVISTO
    resgates.reset_index(inplace=True)
    return

def get_cotas_intervalo(codcot, solicitacao, movimentos):
    cotas = movimentos[(movimentos.SOLICITACAO < solicitacao) & (movimentos.CODCOT==codcot)].COTAS_PREVISTO.sum()
    cotas += movimentos[(movimentos.SOLICITACAO == solicitacao) & (movimentos.CODCOT==codcot) & (movimentos.OPERACAO != 'RT')].COTAS_PREVISTO.sum()
    return cotas

#busca soma de resgates cotizando entre a data de atualizacao do saldo e cotização dos totais
def verifica_intervalo(resgates, mov_saldos):
    cotas_pendentes = [get_cotas_intervalo(codcot, solicitacao, mov_saldos) for codcot, solicitacao in zip(resgates.CODCOT, resgates.SOLICITACAO)]
    idx = pd.MultiIndex.from_arrays([resgates.CODCOT, resgates.SOLICITACAO])
    resgates_pendentes = pd.DataFrame(cotas_pendentes, columns=['COTAS_PREVISTO'], index=idx)
    
    resgates.set_index(['CODCOT', 'SOLICITACAO'], inplace=True)
    resgates['COTAS_PREVISTO'] = resgates.COTAS_PREVISTO.sub(resgates_pendentes.COTAS_PREVISTO)
    resgates.reset_index(inplace=True)
    return

#atualiza financeiro
def calcula_financeiro(cota, resgates):
    resgates['FINANCEIRO'] = resgates.COTAS_PREVISTO * cota
    return