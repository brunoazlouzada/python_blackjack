import graphics as gf
import os
import subprocess
import sys

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
    return (nome[0], nome[1])

def clicou(ret, x, y):
  p1 = ret.getP1()
  p2 = ret.getP2()
  return p1.x <= x <= p2.x and p1.y <= y <= p2.y

def clicou_circulo(circle, x, y):
  cx = circle.getCenter().x
  cy = circle.getCenter().y
  r = circle.getRadius()
  return (x - cx)**2 + (y - cy)**2 <= r**2

def pode_apostar(fichas, aposta, valor):
  return aposta + valor <= fichas

def tela_aposta(win, fichas):

  aposta = 0
  objetos = []

  txt_fichas = gf.Text(gf.Point(600, 160), f"Fichas: {fichas}")
  txt_fichas.setSize(20)
  txt_fichas.setFill("white")
  txt_fichas.draw(win)
  objetos.append(txt_fichas)

  titulo = gf.Text(gf.Point(600, 200), "FAÇA SUA APOSTA")
  titulo.setSize(30)
  titulo.setFill("white")
  titulo.draw(win)
  objetos.append(titulo)

  txt_aposta = gf.Text(gf.Point(600, 260), f"Aposta: {aposta}")
  txt_aposta.setSize(22)
  txt_aposta.setFill("yellow")
  txt_aposta.draw(win)
  objetos.append(txt_aposta)

  valores = [1000, 100, 10, 5]
  fichas_btn = []

  x = 350
  for v in valores:
    ficha = gf.Circle(gf.Point(x, 360), 30)
    ficha.setFill("gold")
    ficha.draw(win)

    txt = gf.Text(gf.Point(x, 360), str(v))
    txt.setSize(12)
    txt.draw(win)

    fichas_btn.append((ficha, v))
    objetos.extend([ficha, txt])

    x += 150

  # ALL-IN
  allin = gf.Circle(gf.Point(450, 460), 40)
  allin.setFill("red")
  allin.draw(win)
  txt_allin = gf.Text(gf.Point(450, 460), "ALL-IN")
  txt_allin.setSize(10)
  txt_allin.draw(win)
  objetos.extend([allin, txt_allin])

  # CONFIRMAR
  confirmar = gf.Circle(gf.Point(750, 460), 40)
  confirmar.setFill("lightgreen")
  confirmar.draw(win)
  txt_conf = gf.Text(gf.Point(750, 460), "OK")
  txt_conf.draw(win)
  objetos.extend([confirmar, txt_conf])

  while True:
    click = win.getMouse()
    cx, cy = click.getX(), click.getY()

    for ficha, valor in fichas_btn:
      if clicou_circulo(ficha, cx, cy):
        if pode_apostar(fichas, aposta, valor):
          aposta += valor
          txt_aposta.setText(f"Aposta: {aposta}")

    if clicou_circulo(allin, cx, cy):
      aposta = fichas
      txt_aposta.setText(f"Aposta: {aposta}")

    if clicou_circulo(confirmar, cx, cy) and aposta > 0:
      for obj in objetos:
        obj.undraw()
      return aposta

def _caminho_save():
  return os.path.join(os.path.dirname(__file__), "save.txt")


def carregar_fichas(valor_inicial=5000):
  caminho = _caminho_save()

  if not os.path.exists(caminho):
    with open(caminho, "w") as f:
      f.write(str(valor_inicial))
    return valor_inicial

  with open(caminho, "r") as f:
    conteudo = f.read().strip()

    if conteudo.isdigit():
      return int(conteudo)
    else:
      return valor_inicial


def salvar_fichas(fichas):
  caminho = _caminho_save()

  with open(caminho, "w") as f:
    f.write(str(fichas))


def jogar_flappy_e_ganhar_fichas():
  caminho_flappy = os.path.join(
    os.path.dirname(__file__),
    "flappy.py"
  )

  resultado = subprocess.run(
    [sys.executable, caminho_flappy],
    capture_output=True,
    text=True
  )

  try:
    pontos = int(resultado.stdout.strip())
  except:
    pontos = 0

  return pontos * 5