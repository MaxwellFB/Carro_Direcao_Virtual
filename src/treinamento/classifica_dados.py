"""
Mostra o frame e ao apertar o teclado informa qual o target para salvar no arquivo csv
"""

import sys

sys.path.append('../')

from utils.captura_teclado import CapturaTeclado
import cv2
import pandas as pd

try:
    file = pd.read_csv('marcas.csv', header=0, sep=';')
except FileNotFoundError:
    raise Exception(
        'Arquivo de marcas nao encontrado! Para criar o arquivo de marcas eh necessario rodar "coleta_dados.py"'
    )

cap_teclado = CapturaTeclado()

print('Opções para classificar os frames:\n'
      '0 = Neutro\n'
      '1 = Pouco direita\n'
      '2 = Muito direita\n'
      '3 = Pouco esquerda\n'
      '4 = Muito esquerda\n'
      'd = Não utilizar arquivo para treinamento (codigo: 666)\n'
      'ESC = Encerrar prematuramente'
      )

for i in range(len(file)):
    path_img = file.iloc[i]['path_img']
    img = cv2.imread(path_img)
    cv2.imshow('Frame', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break

    cap_teclado.escuta_teclado()
    tecla = cap_teclado.tecla
    if tecla == 42:
        print('Encerrando!')
        cv2.destroyAllWindows()
        break
    file.at[i, 'target'] = tecla

    cv2.destroyAllWindows()
    cv2.waitKey(5)

    # Salva alterações no arquivo
    file.to_csv('marcas.csv', sep=';', index=False)
print('Todos dados classificados com sucesso!')
