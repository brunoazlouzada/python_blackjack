import graphics as gf
import random
import time
import os

import funcoes_blackjack as fb

#organizaçao dos diretorios
dir_atual = os.path.dirname(__file__)
dir_backgrounds = os.path.join(dir_atual, 'images', 'backgrounds')
dir_imagens = os.path.join(dir_atual, 'images')

win = gf.GraphWin("Blackjack", 1200, 600)
centro = gf.Point(600, 300)

fundo = gf.Image(centro, os.path.join(dir_backgrounds, "blackjack1200x600.png"))
fundo.draw(win)

#criar e embalharar o baralho
baralho = fb.criar_baralho()
random.shuffle(baralho)

#maos jogador e dealer
jogador = []
dealer = []

#jogador recebe 2 cartas
jog_c1 = baralho.pop()
jog_c2 = baralho.pop()
jogador.append(jog_c1)
jogador.append(jog_c2)

#dealer recebe 1 carta aberta e 1 fechada
deal_c1 = baralho.pop()   #aberta
deal_c2 = baralho.pop()   #fechada
dealer.append(deal_c1)
dealer.append(deal_c2)

#desenhar cartas do jogador
x = 590
y = 500
for nome in jogador:
  img = gf.Image(gf.Point(x, y), os.path.join(dir_imagens, nome))
  img.draw(win)
  time.sleep(0.4)
  x += 30
  y -= 5

#carta ABERTA do dealer
img_d1 = gf.Image(gf.Point(500, 150), os.path.join(dir_imagens, deal_c1))
img_d1.draw(win)
time.sleep(0.4)

#carta FECHADA do dealer
img_d2 = gf.Image(gf.Point(550, 150), os.path.join(dir_imagens, "back.png"))
img_d2.draw(win)
time.sleep(0.4)

#botão HIT
hit_circle = gf.Circle(gf.Point(558, 570), 25)
hit_circle.setFill("lightgray")
hit_circle.draw(win)

hit_txt = gf.Text(gf.Point(558, 570), "HIT")
hit_txt.setSize(10)
hit_txt.draw(win)

#botão STAND
stand_circle = gf.Circle(gf.Point(640, 570), 25)
stand_circle.setFill("lightgray")
stand_circle.draw(win)

stand_txt = gf.Text(gf.Point(640, 570), "STAND")
stand_txt.setSize(10)
stand_txt.draw(win)

pontos_jog = fb.calcular_pontos([fb.dividir_valor_naipe(jog_c1), fb.dividir_valor_naipe(jog_c2)])

txt_jog = gf.Text(gf.Point(545, 450), pontos_jog)
txt_jog.setSize(20)
txt_jog.setFill("white")
txt_jog.setStyle("bold")
txt_jog.draw(win)

#mostrar carta revelada do dealer
valor_d1, _ = fb.dividir_valor_naipe(deal_c1)
if valor_d1 in ["J","Q","K"]:
  txt_deal = gf.Text(gf.Point(455, 100), 10)
  txt_deal.setSize(20)
  txt_deal.setFill("white")
  txt_deal.setStyle("bold")
  txt_deal.draw(win)
elif valor_d1 == "A":
  txt_deal = gf.Text(gf.Point(455, 100), 11)
  txt_deal.setSize(20)
  txt_deal.setFill("white")
  txt_deal.setStyle("bold")
  txt_deal.draw(win)
else:
  txt_deal = gf.Text(gf.Point(455, 100), valor_d1)
  txt_deal.setSize(20)
  txt_deal.setFill("white")
  txt_deal.setStyle("bold")
  txt_deal.draw(win)

#LOOP DO JOGADOR
jogando = True
x_jog = 590 + 30*2  # posição inicial para cartas novas do jogador
y_jog = 500 - 5*2

while jogando:
  click = win.getMouse()
  cx, cy = click.getX(), click.getY()

  if fb.clicou_circulo(hit_circle, cx, cy):  # jogador clicou HIT
    nova = baralho.pop()
    jogador.append(nova)

    img = gf.Image(gf.Point(x_jog, y_jog), os.path.join(dir_imagens, nova))
    img.draw(win)
    time.sleep(0.4)
    x_jog += 30
    y_jog -= 5

    #recalcular pontos
    pontos_jog = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in jogador])
    txt_jog.setText(pontos_jog)

    if pontos_jog > 21:
      jogando = False  # estourou
      break

  elif fb.clicou_circulo(stand_circle, cx, cy):  # jogador clicou STAND
    jogando = False

#revelar carta do dealer
img_d2.undraw()
img_real = gf.Image(gf.Point(550, 150), os.path.join(dir_imagens, deal_c2))
img_real.draw(win)
time.sleep(0.4)

pontos_dealer = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in dealer])
x_deal = 550 + 55
txt_deal.setText(pontos_dealer)

while pontos_dealer < 17:
  nova = baralho.pop()
  dealer.append(nova)

  img = gf.Image(gf.Point(x_deal, 150), os.path.join(dir_imagens, nova))
  img.draw(win)
  time.sleep(0.4)
  x_deal += 55

  pontos_dealer = fb.calcular_pontos([fb.dividir_valor_naipe(c) for c in dealer])
  txt_deal.setText(pontos_dealer)

resultado = ""

if pontos_jog > 21:
  resultado = "Você estourou! Dealer vence."
elif pontos_dealer > 21:
  resultado = "Dealer estourou! Você venceu!"
elif pontos_jog > pontos_dealer:
  resultado = "Você venceu!"
elif pontos_jog < pontos_dealer:
  resultado = "Dealer venceu!"
else:
  resultado = "Empate!"

time.sleep(0.5)
res_txt = gf.Text(gf.Point(600, 400), resultado)
res_txt.setSize(26)
res_txt.setFill("yellow")
res_txt.draw(win)

win.getMouse()
win.close()