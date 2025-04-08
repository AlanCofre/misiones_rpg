from collections import deque

class ColaMisiones:
    def __init__(self):
        self.cola = deque()
    
    # Enqueue
    def agregar_mision(self, mision_id: int):
        self.cola.append(mision_id)
    
    # Dequeue
    def obtener_siguiente_mision(self):
        if self.esta_vacia():
            return None
        return self.cola.popleft()
    
    # First
    def ver_siguiente_mision_id(self):
        if self.esta_vacia():
            return None
        return self.cola[0]

    # Is_empty
    def esta_vacia(self):
        return len(self.cola) == 0
    
    
    def obtener_todos_los_ids(self):
        return list(self.cola)
    
    # Size
    def obtener_tamano(self):
        return len(self.cola)