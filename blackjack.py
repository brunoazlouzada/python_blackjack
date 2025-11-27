import graphics as gf
import random
import time
import os

import funcoes_blackjack as fb

#organizaçao dos diretorios
dir_atual = os.path.dirname(__file__)
dir_backgrounds = os.path.join(dir_atual, 'images', 'backgrounds')
dir_imagens = os.path.join(dir_atual, 'images')

def play_round(fichas: int):
  #Serve para poder jogar de novo em um novo GraphWin quando acabar, mantendo as fichas atualizadas
  win = gf.GraphWin("Blackjack", 1200, 600)
  centro = gf.Point(600, 300)

  fundo = gf.Image(centro, os.path.join(dir_backgrounds, "blackjack1200x600.png"))
  fundo.draw(win)

  # Mostrar total de fichas no canto superior direito
  rect_bank = None
  txt_bank = None
  def total_fichas(valor):
    nonlocal rect_bank, txt_bank
    content = f"Fichas: {valor}"
    # aproxima largura com base no número de caracteres
    pixel_carac = 12
    pixel_pad = 26
    max_w = 300
    width = min(max_w, max(80, len(content) * pixel_carac + pixel_pad))
    height = 28
    cx, cy = 1080, 30
    if rect_bank:
      try:
        rect_bank.undraw()
      except Exception:
        pass
    if txt_bank:
      try:
        txt_bank.undraw()
      except Exception:
        pass
    rect_bank = gf.Rectangle(gf.Point(cx - width/2, cy - height/2), gf.Point(cx + width/2, cy + height/2))
    rect_bank.setFill("black")
    rect_bank.setOutline("white")
    rect_bank.draw(win)
    txt_bank = gf.Text(gf.Point(cx, cy), content)
    txt_bank.setSize(16)
    txt_bank.setFill("white")
    txt_bank.draw(win)

  total_fichas(fichas)

  # Seleção de aposta (antes de distribuir as cartas)
  # valores e botões para ajuste
  min_aposta = 5
  if fichas < min_aposta:
    # sem fichas — mostra mensagem e espera clique para sair
    aviso = gf.Text(gf.Point(600, 300), "Você ficou sem fichas!")
    aviso.setSize(24)
    aviso.setFill("red")
    aviso.draw(win)
    win.getMouse()
    win.close()
    return False, fichas

  passo_aposta = 5
  aposta = min_aposta if fichas >= min_aposta else fichas

  # widget de aposta: desenha um fundo preto atrás do texto e redimensiona conforme necessário
  fundo_aposta = None
  txt_aposta = None
  def atualizar_exibicao_aposta(valor):
    nonlocal fundo_aposta, txt_aposta
    content = f"Aposta: {valor}"
    # estima largura baseada no número de caracteres (aprox. 12px por caractere)
    pixel_carac = 12
    pixel_pad = 20 
    max_w = 500
    width = min(max_w, max(80, len(content) * pixel_carac + pixel_pad))
    height = 34
    cx, cy = 600, 60
    if fundo_aposta:
      try:
        fundo_aposta.undraw()
      except Exception:
        pass
    if txt_aposta:
      try:
        txt_aposta.undraw()
      except Exception:
        pass
    fundo_aposta = gf.Rectangle(gf.Point(cx - width/2, cy - height/2), gf.Point(cx + width/2, cy + height/2))
    fundo_aposta.setFill("black")
    fundo_aposta.setOutline("white")
    fundo_aposta.draw(win)
    txt_aposta = gf.Text(gf.Point(cx, cy), content)
    txt_aposta.setSize(18)
    txt_aposta.setFill("white")
    txt_aposta.draw(win)

  atualizar_exibicao_aposta(aposta)

  # botões: -10, -5, +5, +10 para ajustar aposta (valores múltiplos de 5)
  btn_menos10 = gf.Circle(gf.Point(520, 100), 18)
  btn_menos10.setFill("lightcoral")
  btn_menos10.draw(win)
  txt_menos10 = gf.Text(gf.Point(520, 100), "-10")
  txt_menos10.setSize(10)
  txt_menos10.draw(win)

  btn_menos5 = gf.Circle(gf.Point(560, 100), 18)
  btn_menos5.setFill("lightcoral")
  btn_menos5.draw(win)
  txt_menos5 = gf.Text(gf.Point(560, 100), "-5")
  txt_menos5.setSize(10)
  txt_menos5.draw(win)

  btn_mais5 = gf.Circle(gf.Point(640, 100), 18)
  btn_mais5.setFill("lightgreen")
  btn_mais5.draw(win)
  txt_mais5 = gf.Text(gf.Point(640, 100), "+5")
  txt_mais5.setSize(10)
  txt_mais5.draw(win)

  btn_mais10 = gf.Circle(gf.Point(680, 100), 18)
  btn_mais10.setFill("lightgreen")
  btn_mais10.draw(win)
  txt_mais10 = gf.Text(gf.Point(680, 100), "+10")
  txt_mais10.setSize(10)
  txt_mais10.draw(win)

  # botão para começar a rodada
  btn_jogar = gf.Circle(gf.Point(1000, 100), 24)
  btn_jogar.setFill("lightblue")
  btn_jogar.draw(win)
  txt_jogar = gf.Text(gf.Point(1000, 100), "Jogar") # texto do botão para começar a rodada
  txt_jogar.setSize(12)
  txt_jogar.draw(win)

  # Fase de seleção: aguarda clique no botão Jogar ou ajuste de aposta
  selecionar = True
  while selecionar:
    click = win.getMouse()
    cx, cy = click.getX(), click.getY()
    if fb.clicou_circulo(btn_mais5, cx, cy):
      # aumento em 5; cap no maior múltiplo de 5 <= fichas
      max_aposta_permitida = (fichas // 5) * 5
      aposta = min(max_aposta_permitida, aposta + 5)
      atualizar_exibicao_aposta(aposta)
    elif fb.clicou_circulo(btn_mais10, cx, cy):
      max_aposta_permitida = (fichas // 5) * 5
      aposta = min(max_aposta_permitida, aposta + 10)
      atualizar_exibicao_aposta(aposta)
    elif fb.clicou_circulo(btn_menos5, cx, cy):
      aposta = max(min_aposta, aposta - 5)
      atualizar_exibicao_aposta(aposta)
    elif fb.clicou_circulo(btn_menos10, cx, cy):
      aposta = max(min_aposta, aposta - 10)
      atualizar_exibicao_aposta(aposta)
    elif fb.clicou_circulo(btn_jogar, cx, cy):
      # checa aposta válida
      if aposta <= 0 or aposta > fichas:
        # mensagem rápida: aposta inválida
        warn = gf.Text(gf.Point(600, 90), "Aposta inválida")
        warn.setSize(12)
        warn.setFill("yellow")
        warn.draw(win)
        time.sleep(0.8)
        warn.undraw()
      else:
        selecionar = False

  # tirar elementos de seleção antes de distribuir (mantemos txt_aposta visível durante a rodada)
  btn_menos10.undraw(); txt_menos10.undraw()
  btn_menos5.undraw(); txt_menos5.undraw()
  btn_mais5.undraw(); txt_mais5.undraw()
  btn_mais10.undraw(); txt_mais10.undraw()
  btn_jogar.undraw(); txt_jogar.undraw()

  # reservar (subtrair) a aposta do total — ela será contabilizada ao final
  # efetiva a aposta (a quantia fica reservada até o fim)
  fichas -= aposta
  total_fichas(fichas)

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

  #botão PEDIR (comprar carta)
  btn_pedir = gf.Circle(gf.Point(558, 570), 25)
  btn_pedir.setFill("lightgray")
  btn_pedir.draw(win)

  txt_pedir = gf.Text(gf.Point(558, 570), "PEDIR")
  txt_pedir.setSize(10)
  txt_pedir.draw(win)

  #botão FICAR (parar)
  btn_ficar = gf.Circle(gf.Point(640, 570), 25)
  btn_ficar.setFill("lightgray")
  btn_ficar.draw(win)

  txt_ficar = gf.Text(gf.Point(640, 570), "FICAR")
  txt_ficar.setSize(10)
  txt_ficar.draw(win)

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

  jogando = True
  #LOOP DO JOGADOR
  jogando = True
  x_jog = 590 + 30*2  # posição inicial para cartas novas do jogador
  y_jog = 500 - 5*2

  while jogando:
    click = win.getMouse()
    cx, cy = click.getX(), click.getY()

    if fb.clicou_circulo(btn_pedir, cx, cy):  # jogador clicou HIT
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

    elif fb.clicou_circulo(btn_ficar, cx, cy):  # jogador clicou STAND
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

  # pedir para jogar novamente
  time.sleep(1.5)
  res_txt.undraw()
  dnv_txt = gf.Text(gf.Point(600, 420), 'Jogar novamente?')
  dnv_txt.setSize(26)
  dnv_txt.setFill("yellow")
  dnv_txt.draw(win)

  sim_circle = gf.Circle(gf.Point(520, 480), 28)
  sim_circle.setFill("lightgreen")
  sim_circle.draw(win)
  sim_txt = gf.Text(gf.Point(520, 480), "Sim")
  sim_txt.setSize(12)
  sim_txt.draw(win)

  nao_circle = gf.Circle(gf.Point(680, 480), 28)
  nao_circle.setFill("lightcoral")
  nao_circle.draw(win)
  nao_txt = gf.Text(gf.Point(680, 480), "Não")
  nao_txt.setSize(12)
  nao_txt.draw(win)

  # atualizar fichas com base no resultado da rodada
  # resultado já avaliado em 'resultado', e a aposta (aposta) foi subtraída antes
  if "Você venceu!" in resultado or "Dealer estourou!" in resultado:
    # jogador vence => recebe de volta sua aposta e o ganho equivalente (pagamento 1:1)
    fichas += aposta * 2
  elif "Empate" in resultado:
    # push — devolve a aposta
    fichas += aposta
  else:
    # jogador perde — aposta já retirada
    pass

  total_fichas(fichas)

  while True:
    click = win.getMouse()
    cx, cy = click.getX(), click.getY()
    if fb.clicou_circulo(sim_circle, cx, cy):
      win.close()
      return True, fichas
    elif fb.clicou_circulo(nao_circle, cx, cy):
      win.close()
      return False, fichas


def saldo():
  # loop principal: executa rodadas até o usuário sair
  fichas = 1000  # saldo inicial de fichas
  while True:
    again, fichas = play_round(fichas)
    if not again:
      break
    # se acabou as fichas, encerrar
    if fichas <= 0:
      # mostrar mensagem final
      win = gf.GraphWin("Blackjack - Fim", 600, 150)
      mensagem = gf.Text(gf.Point(300, 75), "Você ficou sem fichas. Obrigado por jogar!")
      mensagem.setSize(14)
      mensagem.draw(win)
      win.getMouse()
      win.close()
      break


if __name__ == "__main__":
  saldo()
    