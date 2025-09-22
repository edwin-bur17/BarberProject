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
        actual = self.head
        anterior = None
        
        while actual:
            condicion = (actual.cliente == cliente and (id_barbero is None or actual.id_barbero == id_barbero))
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
        actual = self.head
        while actual:
            if actual.cliente == cliente and actual.id_barbero == id_barbero:
                actual.estado = "Atendido"
                return self.eliminar_turno(cliente, id_barbero)
            actual = actual.next
        return False

    # ✅ NUEVO MÉTODO - Buscar turno por correo
    def buscar_turno_por_correo(self, correo):
        actual = self.head
        while actual:
            if actual.correo == correo:
                return {
                    "cliente": actual.cliente,
                    "fecha": actual.fecha,
                    "hora": actual.hora,
                    "correo": actual.correo,
                    "id_barbero": actual.id_barbero,
                    "estado": actual.estado
                }
            actual = actual.next
        return None

    # ✅ NUEVO MÉTODO - Eliminar turno por correo
    def eliminar_turno_por_correo(self, correo):
        actual = self.head
        anterior = None
        while actual:
            if actual.correo == correo:
                if anterior:
                    anterior.next = actual.next
                else:
                    self.head = actual.next
                return True
            anterior = actual
            actual = actual.next
        return False
