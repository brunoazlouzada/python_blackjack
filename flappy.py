from graphics import *
import time
import random

# janela
LARGURA = 400
ALTURA = 600
win = GraphWin("Flappy Bird (Graphics.py)", LARGURA, ALTURA)
win.setBackground("skyblue")

# "passaro"
passaro = Circle(Point(100, ALTURA // 2), 15)
passaro.setFill("yellow")
passaro.draw(win)

gravidade = 0
impulso = -5

# canoas
cano_largura = 60
gap = 140
velocidade = 3

def criar_canos():
  topo = random.randint(80, 350)
  # cano superior
  cano_cima = Rectangle(Point(LARGURA, 0), Point(LARGURA + cano_largura, topo))
  cano_cima.setFill("green")
  # cano inferior
  cano_baixo = Rectangle(Point(LARGURA, topo + gap), Point(LARGURA + cano_largura, ALTURA))
  cano_baixo.setFill("green")
  return topo, cano_cima, cano_baixo

topo, cano_cima, cano_baixo = criar_canos()
cano_cima.draw(win)
cano_baixo.draw(win)

# pontucao
pontos = 0
texto = Text(Point(LARGURA // 2, 40), "0")
texto.setSize(24)
texto.draw(win)

# loop jogo
while True:

  # entrada
  tecla = win.checkKey()
  if tecla == "space":
    gravidade = impulso
  elif tecla == "Escape":
    break

  # física
  gravidade += 0.25
  passaro.move(0, gravidade)

  # mover canos
  cano_cima.move(-velocidade, 0)
  cano_baixo.move(-velocidade, 0)

  # pegar posições
  px = passaro.getCenter().getX()
  py = passaro.getCenter().getY()

  cc1x = cano_cima.getP1().getX()
  cc2x = cano_cima.getP2().getX()
  topo_cano = topo

  # reciclar cano
  if cc2x < 0:
    topo, cano_cima_new, cano_baixo_new = criar_canos()
    cano_cima.undraw()
    cano_baixo.undraw()
    cano_cima = cano_cima_new
    cano_baixo = cano_baixo_new
    cano_cima.draw(win)
    cano_baixo.draw(win)

    pontos += 1
    texto.setText(str(pontos))

  # colisão com bordas
  if py < 0 or py > ALTURA:
    break

  # colisão com canos (simples)
  if cc1x < px < cc2x:
    if py < topo_cano or py > topo_cano + gap:
      break

  time.sleep(0.02)

# fim de jogo
fim = Text(Point(LARGURA // 2, ALTURA // 2), "GAME OVER")
fim.setSize(30)
fim.setFill("red")
fim.draw(win)

win.getKey()
win.close()

print(pontos)