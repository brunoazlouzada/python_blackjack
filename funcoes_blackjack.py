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

def clicou_circulo(circle, x, y):
  cx = circle.getCenter().x
  cy = circle.getCenter().y
  r = circle.getRadius()
  return (x - cx)**2 + (y - cy)**2 <= r**2