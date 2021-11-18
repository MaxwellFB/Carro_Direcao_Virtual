"""
Monitora teclado
"""

from pynput.keyboard import Listener


class CapturaTeclado:
    """Monitora algumas teclas do teclado"""

    def __init__(self):
        self.tecla = 0

    def escuta_teclado(self):
        """Escuta teclas"""
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _on_press(self, key):
        """Pega tecla pressionada"""
        # Neutro
        if str(key) == "'0'":
            self.tecla = 0
            return False
        # Pouco direita
        elif str(key) == "'1'":
            self.tecla = 1
            return False
        # Muito direita
        elif str(key) == "'2'":
            self.tecla = 2
            return False
        # Pouco esquerda
        elif str(key) == "'3'":
            self.tecla = 3
            return False
        # Muito esquerda
        elif str(key) == "'4'":
            self.tecla = 4
            return False
        # Marca como informação nao utilizavel
        elif str(key) == "'d'":
            self.tecla = 666
            return False
        # Envia comando para encerrar
        elif str(key) == 'Key.esc':
            self.tecla = 42
            return False
