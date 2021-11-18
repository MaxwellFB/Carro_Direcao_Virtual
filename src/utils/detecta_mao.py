"""Baseado no MediaPipe, disponibilizado em: https://google.github.io/mediapipe/solutions/hands.html"""

import mediapipe as mp
import cv2
import pandas as pd


class DetectaMao:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def detectar(self, img):
        """Detecta mao e retorna coordenadas dedos. Recebe imagem BGR"""
        results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        return results.multi_hand_landmarks

    def desenhar(self, img, marcas):
        """Desenha os ligamentos da mao"""
        # Faz copia, caso contrario altera a imagem passada como parametro, influenciando em quem chamou
        imagem = img.copy()
        for marca in marcas:
            self.mp_drawing.draw_landmarks(
                image=imagem,
                landmark_list=marca,
                connections=self.mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_hand_landmarks_style(),
                connection_drawing_spec=self.mp_drawing_styles.get_default_hand_connections_style())

        return imagem

    def salvar_marcas_imagem(self, img, marcas, path_frame='frames', path_marca='marcas.csv'):
        """Salva todas marcas das maos em um arquivo csv"""
        for marca in marcas:
            file = pd.read_csv(path_marca, header=0, sep=';')
            dados = []
            # Pega todos coordedados dos pontos da mao
            for i in range(21):
                dados.append(marca.landmark[i].x)
                dados.append(marca.landmark[i].y)
                dados.append(marca.landmark[i].z)
            path_img = '{}/{}.jpg'.format(path_frame, len(file))
            cv2.imwrite(path_img, img)
            # Caminho e nome da imagem
            dados.append(path_img)
            # Informa que nao foi classificado a imagem
            dados.append(-1)
            df_dados = pd.DataFrame(
                [dados],
                columns=file.columns)
            file = file.append(df_dados, ignore_index=True)
            file.to_csv('marcas.csv', sep=';', index=False)
