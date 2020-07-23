import pyodbc as db
import utils
import sys
import operacoes as op


def update_movimentos(codfund):
    conn = db.connect('Driver={SQL Server};Server=EQNSQL02\\HOMOLOGASPXBANCO;Database=RIMovimentos;Trusted_Connection=yes')

    data_ref = utils.get_data(codfund, conn) #recupera data da ultima cota do fundo
    print('data_ref: {}'.format(data_ref))

    cota = utils.get_cota(codfund, data_ref, conn) #recupera valor da ultima cota do fundo
    print('cota: {}'.format(cota))
    
    data_saldos = utils.get_data_saldos(conn)
    mov_saldos = utils.get_movimentos(codfund, data_saldos, conn) #recupera todas as movimentações com cotização >= data_saldos
    mov = utils.get_movimentos(codfund, data_ref, conn) #recupera todas as movimentações com cotização >= data_ref
    
    op.atualiza_resgates_cotas(cota, mov)
    op.atualiza_aplicacoes(cota, mov)
    op.atualiza_resgates_financeiros(cota, mov)
    op.atualiza_resgates_financeiros(cota, mov_saldos.loc[mov_saldos.COTIZACAO>=data_ref])
    # op.copia_cotas(data_ref, mov.copy(), mov_saldos)
    op.recalcula_resgates_totais(mov, codfund, data_saldos, conn)
    op.recalcula_resgates_totais(mov_saldos.loc[mov_saldos.COTIZACAO>=data_ref], codfund, data_saldos, conn)
    op.atualiza_resgates_totais(cota, mov, mov_saldos)
    # op.atualiza_resgates_totais_por_cautela()

    utils.set_movimentos(codfund, data_ref, mov)
    conn.close()


if len(sys.argv)==2:
    codfund = sys.argv[1]
else:
    codfund = None

if __name__=='__main__' and codfund:
    update_movimentos(codfund)