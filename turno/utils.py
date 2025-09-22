from datetime import timedelta, datetime, time
from .models import Reserva

FRANJAS = [
    (time(8, 0), time(9, 0)),
    (time(9, 0), time(10, 0)),
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    # Salto de almuerzo de 12pm a 1pm
    (time(13, 0), time(14, 0)),
    (time(14, 0), time(15, 0)),
    (time(15, 0), time(16, 0)),
    (time(16, 0), time(17, 0)),
]


def is_slot_available(barbero, fecha, hora_inicio, hora_fin):
    """
    Verifica si un barbero tiene libre la franja [hora_inicio, hora_fin] en una fecha.
    """
    reservas = Reserva.objects.filter(barbero=barbero, fecha=fecha)

    for r in reservas:
        # Si hay cruce de horarios, el slot NO está disponible
        if hora_inicio < r.hora_fin and r.hora_inicio < hora_fin:
            return False
    return True


def available_slots_for_barber(barbero, fecha):
    """
    Retorna una lista de slots disponibles para un barbero en una fecha específica.
    Cada slot es un diccionario con inicio, fin y disponibilidad.
    """
    slots = []
    for inicio, fin in FRANJAS:
        disponible = is_slot_available(barbero, fecha, inicio, fin)
        slots.append({
            "inicio": inicio,
            "fin": fin,
            "disponible": disponible,
        })
    return slots
