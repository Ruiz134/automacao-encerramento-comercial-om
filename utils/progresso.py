import sys
import shutil


def exibir_barra(etapa, total, msg, contador=True):
    if total <= 0:
        total = 1

    largura_barra = 40
    progresso = min(etapa / total, 1)
    preenchido = int(largura_barra * progresso)
    barra = "▰" * preenchido + "▱" * (largura_barra - preenchido)
    percentual = progresso

    # Remove quebras de linha escondidas
    msg = str(msg).replace("\n", " ").replace("\r", " ").strip()

    if contador:
        texto = f" {msg} ❭ [{etapa}/{total}] |{barra}| {percentual:.1%}"
    else:
        texto = f" {msg} ❭ |{barra}| {percentual:.1%}"

    # Evita wrap no terminal
    largura_terminal = shutil.get_terminal_size((120, 20)).columns
    if len(texto) > largura_terminal - 1:
        texto = texto[:largura_terminal - 4] + "..."

    sys.stdout.write("\r\033[K" + texto)
    sys.stdout.flush()

    # Quebra linha no final
    if etapa >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()