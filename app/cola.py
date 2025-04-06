from collections import deque
from app.models import Mision

class ColaMisiones:
    def __init__(self):
        self.cola = deque()
    
    def agregar_mision(self, mision: Mision):
        """Agregar una mision al final de la cola"""
        self.cola.append(mision)
    
    def obtener_siguiente_mision(self):
        """Remover y retorna la primera mision en la cola"""
        if self.esta_vacia():
            return None
        return self.cola.popleft()
    
    def ver_siguiente_mision(self):
        """devuelve la proxima mision sin sacarla de la cola"""
        if self.esta_vacia():
            return None
        return self.cola[0]

    def esta_vacia(self):
        return len(self.cola) == 0
    
    def obtener_todas(self):
        """devuelve todas las misiones en la cola como lista"""
        return list(self.cola)