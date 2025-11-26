import graphics as gf
import random
import time
import os

#organizaçao dos diretorios
dir_atual = os.path.dirname(__file__)
dir_backgrounds = os.path.join(dir_atual, 'images', 'backgrounds')
dir_imagens = os.path.join(dir_atual, 'images')

win = gf.GraphWin("Blackjack", 1200, 600)
centro = gf.Point(600, 300)

fundo = gf.Image(centro, os.path.join(dir_backgrounds, "blackjack1200x600.png"))
fundo.draw(win)

def criar_baralho():
  valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
  naipes = ["H", "D", "C", "S"]  # Hearts, Diamonds, Clubs, Spades

  baralho = []

  for v in valores:
    for n in naipes:
      nome_imagem = f"{v}{n}.png"   # exemplo: "10H.png"
      baralho.append(nome_imagem)

  return baralho

def calcular_pontos(cartas):
  total = 0
  ases = 0
  for valor, _ in cartas:
    if valor in ["J","Q","K"]:
      total += 10
    elif valor == "A":
      total += 11
      ases += 1
    else:
      total += int(valor)
  while total > 21 and ases > 0:
    total -= 10
    ases -= 1

  return total

def dividir_valor_naipe(nome):
  nome = nome.replace(".png", "")
  if nome[:-1] == "10":
    return ("10", nome[-1])   # último caractere é o naipe
  else:
    return (nome[0], nome[1]) # ex: "AH" → ("A","H")

def clicou(ret, x, y):
  p1 = ret.getP1()
  p2 = ret.getP2()
  return p1.x <= x <= p2.x and p1.y <= y <= p2.y

#criar e embalharar o baralho
baralho = criar_baralho()
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
x = 450
for nome in jogador:
  img = gf.Image(gf.Point(x, 400), os.path.join(dir_imagens, nome))
  img.draw(win)
  time.sleep(0.4)
  x += 90

#carta ABERTA do dealer
img_d1 = gf.Image(gf.Point(450, 200), os.path.join(dir_imagens, deal_c1))
img_d1.draw(win)
time.sleep(0.4)

#carta FECHADA do dealer
img_d2 = gf.Image(gf.Point(540, 200), os.path.join(dir_imagens, "back.png"))
img_d2.draw(win)
time.sleep(0.4)

#botão HIT
hit_ret = gf.Rectangle(gf.Point(900, 450), gf.Point(1050, 500))
hit_ret.setFill("lightgray")
hit_ret.draw(win)

hit_txt = gf.Text(gf.Point(975, 475), "HIT")
hit_txt.draw(win)

#botão STAND
stand_ret = gf.Rectangle(gf.Point(900, 520), gf.Point(1050, 570))
stand_ret.setFill("lightgray")
stand_ret.draw(win)

stand_txt = gf.Text(gf.Point(975, 545), "STAND")
stand_txt.draw(win)

pontos_jog = calcular_pontos([dividir_valor_naipe(jog_c1), dividir_valor_naipe(jog_c2)])

txt_jog = gf.Text(gf.Point(200, 500), f"Jogador: {pontos_jog} pontos")
txt_jog.setSize(20)
txt_jog.setFill("white")
txt_jog.draw(win)

#mostrar carta revelada do dealer
valor_d1, _ = dividir_valor_naipe(deal_c1)
if valor_d1 in ["J","Q","K"]:
  txt_deal = gf.Text(gf.Point(200, 100), "Dealer: 10")
  txt_deal.setSize(20)
  txt_deal.setFill("white")
  txt_deal.draw(win)
else:
  txt_deal = gf.Text(gf.Point(200, 100), f"Dealer: {valor_d1}")
  txt_deal.setSize(20)
  txt_deal.setFill("white")
  txt_deal.draw(win)

#LOOP DO JOGADOR
jogando = True
x_jog = 450 + 90*2  # posição inicial para cartas novas do jogador

while jogando:
  click = win.getMouse()
  cx, cy = click.getX(), click.getY()

  if clicou(hit_ret, cx, cy):  # jogador clicou HIT
    nova = baralho.pop()
    jogador.append(nova)

    img = gf.Image(gf.Point(x_jog, 400), os.path.join(dir_imagens, nova))
    img.draw(win)
    time.sleep(0.4)
    x_jog += 90

    #recalcular pontos
    pontos_jog = calcular_pontos([dividir_valor_naipe(c) for c in jogador])
    txt_jog.setText(f"Jogador: {pontos_jog} pontos")

    if pontos_jog > 21:
      jogando = False  # estourou
      break

  elif clicou(stand_ret, cx, cy):  # jogador clicou STAND
    jogando = False

#revelar carta do dealer
img_d2.undraw()
img_real = gf.Image(gf.Point(540, 200), os.path.join(dir_imagens, deal_c2))
img_real.draw(win)
time.sleep(0.4)

pontos_dealer = calcular_pontos([dividir_valor_naipe(c) for c in dealer])
x_deal = 540 + 90
txt_deal.setText(f"Dealer: {pontos_dealer}")

while pontos_dealer < 17:
  nova = baralho.pop()
  dealer.append(nova)

  img = gf.Image(gf.Point(x_deal, 200), os.path.join(dir_imagens, nova))
  img.draw(win)
  time.sleep(0.4)
  x_deal += 90

  pontos_dealer = calcular_pontos([dividir_valor_naipe(c) for c in dealer])
  txt_deal.setText(f"Dealer: {pontos_dealer}")

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
res_txt = gf.Text(gf.Point(600, 560), resultado)
res_txt.setSize(26)
res_txt.setFill("yellow")
res_txt.draw(win)

win.getMouse()
win.close()