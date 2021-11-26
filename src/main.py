"""
Executa Airsim e comeca as previsoes para o movimento da direcao do carro
"""

import cv2
import torch
from threading import Thread
from airgym.envs.car_env import AirSimCarEnv
from utils.detecta_mao import DetectaMao
from utils.captura_mouse import CapturaMouse


def main():
    sistema = Sistema()
    sistema.iniciar()


class Sistema:
    def __init__(self):
        self.mao = DetectaMao()

        try:
            self.model = self._carregar_model('model.pth')
        except FileNotFoundError:
            raise Exception('Model nao encontrado! Verifique se o caminho para o model esta correto.')

        try:
            # Localhost: ip_address="127.0.0.1"
            self.car_env = AirSimCarEnv(ip_address="127.0.0.1")
        except Exception:
            raise Exception(
                'Ambiente Airsim nao encontrado! Verifique se o ambiente foi inicializado e se o endereco esta correto.'
            )

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception('Camera nao encontrada! Verifique se a camera esta ativada e se o endereco esta correto.')

        # Cria thread para escutar mouse
        self.cap_mouse = CapturaMouse()
        threads = [Thread(target=self.cap_mouse.escuta_mouse)]
        for thread in threads:
            thread.start()

    def iniciar(self):
        """Inicia sistema"""
        while self.cap.isOpened():
            success, frame = self.cap.read()
            # Deixa a imagem como se fosse um espelho
            frame = cv2.flip(frame, 1)
            frame_original = frame.copy()

            marcas_mao = self.mao.detectar(frame_original)
            direcao = 0
            # Se detectou a mao desenha e pega comando da direcao
            if marcas_mao:
                frame = self.mao.desenhar(frame_original, marcas_mao)
                direcao = self._prever_acao(marcas_mao)

            acelerador = self.cap_mouse.acelerador

            cv2.putText(frame, str(direcao) + '-' + str(acelerador), (frame.shape[1] - 180, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

            cv2.imshow('You!', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            self.car_env.step([direcao, acelerador])

        self.encerrar()

    def _prever_acao(self, marcas):
        """Utiliza um modelo ja carregado para prever a acao baseado nas coordenadas das marcas da mao"""
        for marca in marcas:
            dados = []
            # Pega todas coordenadas dos pontos da mao
            for i in range(21):
                dados.append(marca.landmark[i].x)
                dados.append(marca.landmark[i].y)
                dados.append(marca.landmark[i].z)

            dados = torch.Tensor(dados)
            dados = dados.unsqueeze(0)
            previsao = self.model(dados)
            top_p, top_class = previsao.topk(k=1, dim=1)

            return top_class.detach().numpy()[0][0]

    def _carregar_model(self, path='model.pth'):
        """Carrega model treinado"""
        model = torch.nn.Sequential(
            torch.nn.Linear(in_features=63, out_features=64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 5),
            torch.nn.Softmax(dim=1)
        )
        state_dict = torch.load(path)
        model.load_state_dict(state_dict)
        return model

    def encerrar(self):
        """Encerra todo sistema"""
        self.cap.release()
        cv2.destroyAllWindows()

        self.cap_mouse.encerrar()


if __name__ == '__main__':
    main()
