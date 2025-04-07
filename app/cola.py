from collections import deque

class ColaMisiones:
    def __init__(self):
        self.cola = deque()
    
    def agregar_mision(self, mision_id: int):
        """Agregar una mision al final de la cola"""
        self.cola.append(mision_id)
    
    def obtener_siguiente_mision(self):
        """Remover y retorna el ID de una mision al final de la cola"""
        if self.esta_vacia():
            return None
        return self.cola.popleft()
    
    def ver_siguiente_mision_id(self):
        """devuelve el ID de la proxima mision sin sacarla de la cola"""
        if self.esta_vacia():
            return None
        return self.cola[0]

    def esta_vacia(self):
        return len(self.cola) == 0
    
    def obtener_todos_los_ids(self):
        """devuelve todas los IDs de las misiones en la cola como lista"""
        return list(self.cola)