"""
Monitora mouse
"""

from pynput.mouse import Listener
import time


class CapturaMouse:
    """Monitora acoes realizadas no mouse"""

    def __init__(self):
        # -1 = frear/ré, 0 = nada, 1 = acelerar
        self.acelerador = 0
        self.isEncerrar = False

    def escuta_mouse(self):
        """Escuta acoes"""
        # Quando uma das funcoes retornar False o Listener eh encerrado
        with Listener(on_click=self._on_click):
            while True:
                time.sleep(1)
                if self.isEncerrar:
                    return False

    def _on_click(self, x, y, button, pressed):
        """Pega clicks"""
        if str(button) == 'Button.left':
            if pressed:
                self.acelerador = 1
            else:
                self.acelerador = 0
        elif str(button) == 'Button.right':
            if pressed:
                self.acelerador = -1
            else:
                self.acelerador = 0
        elif str(button) == 'Button.middle':
            if pressed:
                self.acelerador = 42
            else:
                self.acelerador = 0

    def encerrar(self):
        """Encerra escuta"""
        self.isEncerrar = True
