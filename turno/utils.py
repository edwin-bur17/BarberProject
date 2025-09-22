from datetime import timedelta, datetime
from .models import Reservation
from datetime import time

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


def is_slot_available(barber, date, time_obj, duration_minutes=30):
    requested_start = datetime.combine(date, time_obj)
    requested_end = requested_start + timedelta(minutes=duration_minutes)
    reservations = Reservation.objects.filter(barber=barber, date=date).exclude(
        status="X"
    )
    for r in reservations:
        r_start = datetime.combine(r.date, r.time)
        r_end = r_start + timedelta(minutes=r.duration_minutes)
        if requested_start < r_end and r_start < requested_end:
            return False
    return True


def available_slots_for_barber(
    barber, date, start_time, end_time, interval_minutes=30, duration_minutes=30
):
    slots = []
    dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)
    while dt + timedelta(minutes=duration_minutes) <= end_dt:
        t = dt.time()
        if is_slot_available(barber, date, t, duration_minutes):
            slots.append(t)
        dt += timedelta(minutes=interval_minutes)
    return slots
