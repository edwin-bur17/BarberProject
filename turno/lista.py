from threading import Lock


class Nodo:
    def __init__(self, dato):
        self.dato = dato   # puede ser dict, id de Reserva, etc.
        self.siguiente = None


class ListaReservas:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._lock = Lock()

    def agregar(self, dato):
        """
        Agrega al final de la lista (O(1)).
        """
        with self._lock:
            nuevo = Nodo(dato)
            if not self.primero:
                self.primero = nuevo
                self.ultimo = nuevo
            else:
                self.ultimo.siguiente = nuevo
                self.ultimo = nuevo

    def obtener_todos(self):
        """
        Retorna los datos de todos los nodos en una lista de Python.
        (Solo para consultar, no para guardar)
        """
        elementos = []
        actual = self.primero
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def limpiar(self):
        """
        Vacía la lista.
        """
        with self._lock:
            self.primero = None
            self.ultimo = None

# --- Singleton en memoria ---
reservas_memoria = ListaReservas()
