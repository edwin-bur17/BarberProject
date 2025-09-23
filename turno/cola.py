from threading import Lock

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ColaEspera:
    def __init__(self):
        self.frente = None
        self.final = None
        self._lock = Lock()

    def encolar(self, dato):
        """
        Agrega al final (O(1))
        """
        with self._lock:
            nuevo = Nodo(dato)
            if not self.frente:
                self.frente = nuevo
                self.final = nuevo
            else:
                self.final.siguiente = nuevo
                self.final = nuevo

    def desencolar(self):
        """
        Saca el primero (O(1)). Retorna el dato o None si está vacía.
        """
        with self._lock:
            if not self.frente:
                return None
            dato = self.frente.dato
            self.frente = self.frente.siguiente
            if not self.frente:
                self.final = None
            return dato

    def ver_todos(self):
        """
        Retorna todos los elementos en orden FIFO (solo para lectura).
        """
        elementos = []
        actual = self.frente
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def limpiar(self):
        with self._lock:
            self.frente = None
            self.final = None


# --- Singleton en memoria ---
cola_memoria = ColaEspera()
