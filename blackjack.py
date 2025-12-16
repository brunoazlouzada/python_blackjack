import graphics as gf
import random
import time
import os
import funcoes_blackjack as fb

def jogar_partida(win, fichas):

  win.delete("all")

  # diretórios
  dir_atual = os.path.dirname(__file__)
  dir_backgrounds = os.path.join(dir_atual, 'images', 'backgrounds')
  dir_imagens = os.path.join(dir_atual, 'images')

  centro = gf.Point(600, 300)
  fundo = gf.Image(centro, os.path.join(dir_backgrounds, "blackjack1200x600.png"))
  fundo.draw(win)

  # apostas
  aposta = fb.tela_aposta(win, fichas)
  fichas -= aposta
  fb.salvar_fichas(fichas)

  # texto contador de fichas
  txt_fichas = gf.Text(gf.Point(1100, 30), f"Fichas: {fichas}")
  txt_fichas.setFill("white")
  txt_fichas.setSize(14)
  txt_fichas.draw(win)

  # baralho
  baralho = fb.criar_baralho()
  random.shuffle(baralho)

  jogador = []
  dealer = []

  jogador.extend([baralho.pop(), baralho.pop()])
  dealer.extend([baralho.pop(), baralho.pop()])

  # cartas jogador
  x, y = 590, 500
  for carta in jogador:
    img = gf.Image(gf.Point(x, y), os.path.join(dir_imagens, carta))
    img.draw(win)
    time.sleep(0.3)
    x += 30
    y -= 5

  # cartas dealer
  img_d1 = gf.Image(gf.Point(500, 150), os.path.join(dir_imagens, dealer[0]))
  img_d1.draw(win)

  img_d2 = gf.Image(gf.Point(550, 150), os.path.join(dir_imagens, "back.png"))
  img_d2.draw(win)

  # botões
  hit = gf.Circle(gf.Point(558, 570), 25)
  hit.setFill("lightgray")
  hit.draw(win)
  gf.Text(gf.Point(558, 570), "HIT").draw(win)

  stand = gf.Circle(gf.Point(640, 570), 25)
  stand.setFill("lightgray")
  stand.draw(win)
  gf.Text(gf.Point(640, 570), "STAND").draw(win)

  # pontos jogador
  pontos_jog = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in jogador])
  txt_jog = gf.Text(gf.Point(545, 450), pontos_jog)
  txt_jog.setSize(20)
  txt_jog.setFill("white")
  txt_jog.setStyle("bold")
  txt_jog.draw(win)

  # pontos dealer
  valor_d1, _ = fb.dividir_valor_naipe(dealer[0])
  if valor_d1 in ["J", "Q", "K"]:
    valor_dealer_txt = 10
  elif valor_d1 == "A":
    valor_dealer_txt = 11
  else:
    valor_dealer_txt = int(valor_d1)

  txt_deal = gf.Text(gf.Point(455, 100), valor_dealer_txt)
  txt_deal.setSize(20)
  txt_deal.setFill("white")
  txt_deal.setStyle("bold")
  txt_deal.draw(win)

  # loop jogador
  jogando = True
  x_jog, y_jog = 650, 490

  while jogando:
    click = win.getMouse()
    cx, cy = click.getX(), click.getY()

    if fb.clicou_circulo(hit, cx, cy):
      nova = baralho.pop()
      jogador.append(nova)

      img = gf.Image(gf.Point(x_jog, y_jog), os.path.join(dir_imagens, nova))
      img.draw(win)
      time.sleep(0.3)
      x_jog += 30
      y_jog -= 5

      pontos_jog = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in jogador])
      txt_jog.setText(pontos_jog)

      if pontos_jog > 21:
        jogando = False

    elif fb.clicou_circulo(stand, cx, cy):
      jogando = False

  # dealer
  img_d2.undraw()
  img_real = gf.Image(gf.Point(550, 150), os.path.join(dir_imagens, dealer[1]))
  img_real.draw(win)

  pontos_dealer = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in dealer])
  txt_deal.setText(pontos_dealer)

  x_deal = 605
  while pontos_dealer < 17:
    nova = baralho.pop()
    dealer.append(nova)

    img = gf.Image(gf.Point(x_deal, 150), os.path.join(dir_imagens, nova))
    img.draw(win)
    time.sleep(0.3)
    x_deal += 55

    pontos_dealer = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in dealer])
    txt_deal.setText(pontos_dealer)

  # resultado
  if pontos_jog > 21:
    resultado = "Você estourou!"
  elif pontos_dealer > 21 or pontos_jog > pontos_dealer:
    resultado = "Você venceu!"
    fichas += aposta * 2
  elif pontos_jog == pontos_dealer:
    resultado = "Empate!"
    fichas += aposta
  else:
    resultado = "Dealer venceu!"

  fb.salvar_fichas(fichas)
  txt_fichas.setText(f"Fichas: {fichas}")

  res = gf.Text(gf.Point(600, 400), resultado)
  res.setSize(26)
  res.setFill("yellow")
  res.draw(win)

  # final
  denovo = gf.Circle(gf.Point(500, 500), 40)
  denovo.setFill("lightgreen")
  denovo.draw(win)
  gf.Text(gf.Point(500, 500), "DE NOVO").draw(win)

  sair = gf.Circle(gf.Point(700, 500), 40)
  sair.setFill("lightcoral")
  sair.draw(win)
  gf.Text(gf.Point(700, 500), "SAIR").draw(win)

  while True:
    click = win.getMouse()
    cx, cy = click.getX(), click.getY()

    if fb.clicou_circulo(denovo, cx, cy):
      return fichas, True

    if fb.clicou_circulo(sair, cx, cy):
      return fichas, False


# loop principal
fichas = fb.carregar_fichas()
tentativas_flappy = 0

win = gf.GraphWin("Blackjack", 1200, 600)

rodando = True
while rodando:

  if fichas == 0:
    if tentativas_flappy < 3:
      win.close()

      ganho = fb.jogar_flappy_e_ganhar_fichas()
      fichas += ganho
      fb.salvar_fichas(fichas)

      tentativas_flappy += 1
      win = gf.GraphWin("Blackjack", 1200, 600)
      continue
    else:
      fichas = 5
      fb.salvar_fichas(fichas)
      tentativas_flappy = 0

  fichas, rodando = jogar_partida(win, fichas)

win.close()