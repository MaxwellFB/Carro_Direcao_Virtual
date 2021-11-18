"""
Inicia a webcam e grava frames em disco quando a mao eh detectada
"""

import sys
sys.path.append('../')

from utils.detecta_mao import DetectaMao
import cv2

# A cada quantos frames ira salvar em disco (para nao ficar muitos frames semelhantes)
frequencia_salva_frame = 10

mao = DetectaMao()

cap = cv2.VideoCapture(0)
cont = 0
print('Iniciando webcam. Pressione ESC para encerrar')
while cap.isOpened():
    success, frame = cap.read()
    # Deixa a imagem como se fosse um espelho
    frame = cv2.flip(frame, 1)
    frame_original = frame.copy()

    marcas_mao = mao.detectar(frame_original)
    if marcas_mao:
        frame = mao.desenhar(frame_original, marcas_mao)

        # Para nao gravar muito seguido
        if cont > frequencia_salva_frame:
            mao.salvar_marcas_imagem(frame, marcas_mao)
            cont = 0
        cont += 1

    cv2.imshow('Coletando dados', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
