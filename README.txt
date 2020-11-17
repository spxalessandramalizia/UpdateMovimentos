UpdateMovimentos – Documentação

Objetivo

Criação de um script que possa rodar automaticamente todos os dias para manter a base de movimentações do RI atualizada. A atualização deve incluir todas as movimentações pendentes de cotização, de forma que o total financeiro dos resgates seja exatamente o valor liquidado após a cotização.

Repositório
•	https://github.com/spxalessandramalizia/UpdateMovimentos.git

Arquivos
•	.\src\utils.py
Script em python com funções de getters e setters das tabelas Cotas, Movimentações e Saldos da base de dados RIMovimentos.
•	.\src\resgatesTotais.py
Script em python encapsulando todas as funções usadas na atualização de resgates totais.
•	.\src\operacoes.py
Script em python com as principais etapas de atualização das movimentações: 
•	.\src\updateMovimentos.py
Script em python com uma função de atualização das movimentações por fundo e uma chamada main com argumento da linha de comando.
•	.\src\mainCode.py
Script em python que recupera todos os fundos e chama o script updateMovimentos.py para cada um dos fundos. Pode ser alterado para atualizar apenas os fundos cuja cota já foi liberada.
•	.\scripts\UpdateMovimentos.bat
Script em batch para chamada do mainCode.py em um ambiente virtual. Pode rodar diariamente com o agendador de tarefas do Windows ou mais de uma vez ao dia para chamar todas os scripts de atualização.

Funcionamento – updateMovimentos.py

1.	O sistema recupera os últimos dados1 disponíveis.
2.	O sistema calcula o valor financeiro dos resgates por cotas usando a cota mais recente
3.	O sistema calcula a quantidade de cotas das aplicações usando a cota mais recente
4.	O sistema calcula a quantidade de cotas dos resgates financeiros a cotizar usando a cota mais recente
5.	O sistema calcula a quantidade de cotas dos resgates totais a cotizar usando o saldo atualizado das cautelas lançadas até o dia de solicitação do resgate
6.	O sistema ajusta a quantidade de cotas dos resgates totais subtraindo a quantidade de cotas atualizada de todos os resgates com cotização maior ou igual à data de processamento da base de saldos e solicitação menor ou igual à data de solicitação do resgate total seguindo a regra de negócio2
7.	O sistema calcula o valor financeiro dos resgates totais atualizados usando a cota mais recente
8.	O sistema apaga da base todas as movimentações com cotização maior ou igual à data da última cota e salva as movimentações atualizadas.
1 Dados
•	data da última cota disponível para o fundo e o valor da cota
•	data de processamento da base de saldos (primeiro dia que não está sendo considerado no saldo do cotista)
•	todas as movimentações com cotização maior ou igual à data da última cota
•	todas as movimentações com cotização maior ou igual à data de processamento da base de saldos
2 Regra de negócio
•	NÃO PODEM SER BOLETADOS MAIS DE UM RESGATE TOTAL POR DIA PARA O MESMO COTISTA E FUNDO.
