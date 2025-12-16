from graphics import *
import time
import random
import math
import os

# diretório de imagens relativo a este arquivo
dir_atual = os.path.dirname(__file__)
dir_images = os.path.join(dir_atual, "images")

# janela
LARGURA = 400
ALTURA = 600
win = GraphWin("Flappy Jack", LARGURA, ALTURA)
fundo = Image(Point(LARGURA // 2, ALTURA // 2), os.path.join(dir_images, "fundo_mesa.png"))
fundo.draw(win)

passaro = Image(Point(100, ALTURA // 2), os.path.join(dir_images, "flappy_ficha.png"))
# reduzir escala se muito grande
MAX_BIRD_DIM = 40
bw = passaro.getWidth(); bh = passaro.getHeight()
factor = max(1, math.ceil(max(bw, bh) / MAX_BIRD_DIM))
if factor > 1:
  passaro.img = passaro.img.subsample(factor)
# recalcular dimensões e raio para colisão
bw = passaro.getWidth(); bh = passaro.getHeight()
raio_passaro = max(bw, bh) / 2
passaro.draw(win)
using_image = True

gravidade = 0
impulso = -5

# canos
cano_largura = 60
# espaçamento fixo entre canos
gap = max(100, 2 * raio_passaro + 4)
velocidade = 3

# imagem usada para os canos
pipe_pixmap = Image(Point(0,0), os.path.join(dir_images, "back.png"))
carta_w = pipe_pixmap.getWidth()
carta_h = pipe_pixmap.getHeight()
cano_largura = carta_w  # ajustar largura do cano para a largura do tile

def criar_canos():
  # garantir que o topo seja gerado com espaço suficiente para o gap
  upper = max(80, ALTURA - gap - carta_h)
  topo = random.randint(80, upper)
  cano_x = LARGURA
  # cano superior
  top_tiles = []
  # usar ceil e alinhar para que a base dos tiles superiores fique exatamente em `topo`
  num_top = math.ceil(topo / carta_h)
  shift_top = num_top * carta_h - topo
  for i in range(num_top):
    y = i * carta_h + carta_h/2 - shift_top
    tile = Image(Point(cano_x + carta_w/2, y), os.path.join(dir_images, "back.png"))
    top_tiles.append(tile)
  # cano inferior (com cartas)
  bottom_tiles = []
  bottom_height = ALTURA - (topo + gap)
  # usar ceil para garantir que o topo das tiles inferiores comece exatamente em topo+gap
  num_bottom = math.ceil(bottom_height / carta_h)
  for i in range(num_bottom):
    y = topo + gap + i * carta_h + carta_h/2
    tile = Image(Point(cano_x + carta_w/2, y), os.path.join(dir_images, "back.png"))
    bottom_tiles.append(tile)
  return topo, top_tiles, bottom_tiles, cano_x

topo, cano_cima, cano_baixo, cano_x = criar_canos()
for t in cano_cima: t.draw(win)
for t in cano_baixo: t.draw(win)

# pontuacao
pontos = 0
texto = Text(Point(LARGURA // 2, 40), "0")
texto.setSize(24)
texto.setFill("white")
texto.draw(win)

def circulo_colide_retangulo_coords(cx, cy, r, esq, dir, top, bot):
  nearest_x = max(esq, min(cx, dir))
  nearest_y = max(top, min(cy, bot))
  dx = cx - nearest_x
  dy = cy - nearest_y
  return (dx*dx + dy*dy) <= (r*r)

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

  # mover canos (mover todos as cartas e atualizar posição x)
  for t in cano_cima: t.move(-velocidade, 0)
  for t in cano_baixo: t.move(-velocidade, 0)
  cano_x -= velocidade

  # pegar posições do pássaro (imagem)
  px = passaro.getAnchor().getX()
  py = passaro.getAnchor().getY()

  esq_cano = cano_x
  dir_cano = cano_x + carta_w
  topo_cano = topo

  # calcular hit boxes reais das cartas (para colisão visual precisa)
  def hit_boxes(cartas):
    if not cartas:
      return None
    left = min(t.getAnchor().getX() - t.getWidth()/2 for t in cartas)
    right = max(t.getAnchor().getX() + t.getWidth()/2 for t in cartas)
    top = min(t.getAnchor().getY() - t.getHeight()/2 for t in cartas)
    bottom = max(t.getAnchor().getY() + t.getHeight()/2 for t in cartas)
    return (left, right, top, bottom)

  hit_box_top = hit_boxes(cano_cima)
  hit_box_bot = hit_boxes(cano_baixo)

  # reciclar cano quando todo o cano saiu da tela
  if dir_cano < 0:
    for t in cano_cima: t.undraw()
    for t in cano_baixo: t.undraw()
    topo, cano_cima, cano_baixo, cano_x = criar_canos()
    for t in cano_cima: t.draw(win)
    for t in cano_baixo: t.draw(win)

    pontos += 1
    texto.setText(str(pontos))

  # colisão com bordas (considerando o raio do pássaro)
  if py - raio_passaro < 0 or py + raio_passaro > ALTURA:
    break

  # colisão com canos
  if (hit_box_top is not None and circulo_colide_retangulo_coords(px, py, raio_passaro, *hit_box_top)) or (hit_box_bot is not None and circulo_colide_retangulo_coords(px, py, raio_passaro, *hit_box_bot)):
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