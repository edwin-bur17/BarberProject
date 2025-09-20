class NodoTurno:
    def __init__(self, cliente, fecha, hora, correo, id_barbero, estado="Pendiente"):
        self.cliente = cliente
        self.fecha = fecha
        self.hora = hora
        self.correo = correo
        self.id_barbero = id_barbero
        self.estado = estado
        self.next = None


class ListaTurnos:
    def __init__(self):
        self.head = None

    def agregar_turno(self, cliente, fecha, hora, correo, id_barbero):
        nuevo = NodoTurno(cliente, fecha, hora, correo, id_barbero)
        if not self.head:
            self.head = nuevo
        else:
            actual = self.head
            while actual.next:
                actual = actual.next
            actual.next = nuevo

    def mostrar_turnos(self):
        turnos = []
        actual = self.head
        while actual:
            turnos.append({
                "cliente": actual.cliente,
                "fecha": actual.fecha,
                "hora": actual.hora,
                "correo": actual.correo,
                "estado": actual.estado
            })
            actual = actual.next
        return turnos
    
    def mostrar_turnos_barbero(self, id_barbero):
        turnos = []
        actual = self.head
        while actual:
            if actual.id_barbero == id_barbero: 
                turnos.append({
                    "cliente": actual.cliente,
                    "fecha": actual.fecha,
                    "hora": actual.hora,
                    "correo": actual.correo,
                    "estado": actual.estado
                })
            actual = actual.next
        return turnos
   
    def eliminar_turno(self, cliente, id_barbero=None):
        """
        Elimina un turno de la lista. 
        Si se proporciona id_barbero, busca específicamente ese turno.
        """
        actual = self.head
        anterior = None
        
        while actual:
            # Si se proporciona id_barbero, validar ambos campos
            if id_barbero is not None:
                condicion = (actual.cliente == cliente and actual.id_barbero == id_barbero)
            else:
                condicion = (actual.cliente == cliente)
            
            if condicion:
                if anterior:
                    anterior.next = actual.next
                else:
                    self.head = actual.next
                return True
            anterior = actual
            actual = actual.next
        return False

    def atender_turno(self, cliente, id_barbero):
        """
        Marca un turno como atendido y lo elimina de la lista.
        Esta es la función principal para procesar turnos atendidos.
        """
        # Primero verificar que el turno existe
        actual = self.head
        while actual:
            if actual.cliente == cliente and actual.id_barbero == id_barbero:
                # Marcar como atendido (opcional, para logging antes de eliminar)
                actual.estado = "Atendido"
                # Eliminar de la lista
                return self.eliminar_turno(cliente, id_barbero)
            actual = actual.next
        return False