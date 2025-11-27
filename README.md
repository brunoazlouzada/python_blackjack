#python blackjack

Este repositório contém um jogo completo de Blackjack (21) desenvolvido em Python para a disciplina Algoritmos e Estruturas de Dados (AED).
O objetivo do projeto é praticar lógica de programação, modularização e manipulação de estruturas de dados através da implementação de um jogo clássico de cartas.

Funcionalidades:
- Baralho padrão de 52 cartas totalmente embaralhado
- Sistema de mãos com cálculo automático de valores (Ás = 1 ou 11)
- Regras tradicionais de Blackjack
- Jogo contra o dealer (computador)
- Apostas com gerenciamento de fichas

Tecnologias utilizadas:
- Python 3
- Lógica e estrutura de dados implementadas sem bibliotecas externas

Escolha o valor da aposta:
- Decida entre hit (comprar carta) ou stand (parar)
- Tente vencer o dealer sem ultrapassar 21!

Como jogar novamente:
- Ao final de cada rodada, você verá dois botões na janela: "Sim" para jogar outra rodada, e "Sair" para fechar o jogo.
	Basta clicar em "Sim" para reiniciar a partida sem precisar reiniciar o programa.

Sistema de fichas e apostas:
- Você começa com 1000 fichas.
- Antes das cartas serem distribuídas, escolha a sua aposta usando os botões "-10", "-5", "+5" e "+10" e clique em "Jogar" para iniciar a rodada.
- A aposta fica reservada no momento de começar a rodada. Se você vencer, receberá 2x a aposta (sua aposta de volta + ganho do mesmo valor). Se empatar, a aposta é devolvida. Se perder, a aposta é subtraída do seu total.
- O total de fichas aparece no canto superior direito durante o jogo.
