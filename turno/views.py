from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Barbero, Reserva, ListaEspera
from datetime import datetime, time, timedelta
from .lista import reservas_memoria
from .cola import cola_memoria

# ========================
# DASHBOARD GENERAL
# ========================
def actualizar_estado(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in ["pendiente", "completado", "cancelado"]:
            reserva.estado = nuevo_estado
            reserva.save()

    return redirect("turno:panel_barbero")
@login_required
def panel_barbero(request):
    # Relacionar al usuario logueado con un barbero
    barbero = get_object_or_404(Barbero, usuario=request.user)

    fecha = timezone.localdate()

    # Reservas de ese barbero para hoy
    reservas = Reserva.objects.filter(
        barbero=barbero,
        fecha=fecha
    ).order_by("hora_inicio")

    return render(request, "turno/panel_barbero.html", {
        "barbero": barbero,
        "fecha": fecha,
        "reservas": reservas
    })

@login_required
def dashboard(request):
    barberos = Barbero.objects.all()
    return render(request, "turno/dashboard.html", {"barberos": barberos})


# ========================
# CREAR RESERVA
# ========================
@login_required
def crear_reserva(request):
    if request.method == "POST":
        fecha = request.POST.get("fecha")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fin = request.POST.get("hora_fin")
        id_barbero = request.POST.get("id_barbero")

        barbero = get_object_or_404(Barbero, id=id_barbero)

        # Crear la reserva
        reserva = Reserva.objects.create(
            cliente=request.user,
            barbero=barbero,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
        )

         # ✅ Guardar en memoria (lista enlazada)
        reservas_memoria.agregar({
            "id": reserva.id,
            "cliente": request.user.username,
            "barbero": barbero.nombre,
            "fecha": str(fecha),
            "hora_inicio": str(hora_inicio),
            "hora_fin": str(hora_fin),
            "estado": reserva.estado,
        })

        lista_reservas = reservas_memoria.obtener_todos()
        print("lista reservas -->", lista_reservas)

        return redirect("turno:reserva_confirmada", reserva_id=reserva.id)

    return redirect("turno:dashboard")


@login_required
def reserva_confirmada(request, reserva_id):
    """Muestra la confirmación de una reserva ya creada."""
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)
    return render(request, "turno/reserva_confirmada.html", {"reserva": reserva})


# ========================
# AGENDA POR BARBERO (vista cliente)
# ========================
@login_required
def agenda_barbero(request, id_barbero):
    barbero = get_object_or_404(Barbero, id=id_barbero)
    fecha = timezone.localdate()

    # Generar slots de 1h de 8 a 12
    slots = []
    inicio = time(8, 0)
    fin = time(12, 0)

    actual = datetime.combine(fecha, inicio)
    while actual.time() < fin:
        slot_inicio = actual.time()
        slot_fin = (actual + timedelta(hours=1)).time()

        existe_reserva = Reserva.objects.filter(
            barbero=barbero,
            fecha=fecha,
            hora_inicio=slot_inicio,
            hora_fin=slot_fin,
            estado="pendiente"      # solo reservas activas
        ).exists()

        slots.append({
            "inicio": slot_inicio,
            "fin": slot_fin,
            "disponible": not existe_reserva
        })
        actual += timedelta(hours=1)

    # verificar si el usuario ya tiene reserva con este barbero hoy
    reserva_usuario = Reserva.objects.filter(
        cliente=request.user,
        barbero=barbero,
        fecha=fecha,
        estado="pendiente"
    ).first()

    # todos ocupados?
    todos_ocupados = all(not s["disponible"] for s in slots)

    return render(request, "turno/agenda_barbero.html", {
        "barbero": barbero,
        "fecha": fecha,
        "slots": slots,
        "reserva_usuario": reserva_usuario,
        "todos_ocupados": todos_ocupados
    })

# ========================
# AGREGAR TURNO A LISTA DE ESPERA
# ========================
@login_required
def unirse_lista_espera(request, id_barbero):
    if request.method == "POST":
        barbero = get_object_or_404(Barbero, id=id_barbero)
        fecha = timezone.localdate()
        ListaEspera.objects.create(
            barbero=barbero,
            fecha=fecha,
            hora_inicio=time(8, 0), 
            cliente=
            request.user
        )

         #  Encolar en memoria (cola FIFO)
        cola_memoria.encolar({
            # "id": espera.id,
            "cliente": request.user.username,
            "barbero": barbero.nombre,
            "fecha": str(fecha),
            "hora_inicio": str(time(8, 0)),
        })

        # Obtener cola de espera
        cola_espera = cola_memoria.ver_todos()

        print("cola espera", cola_espera)

        return redirect("turno:dashboard")

# ========================
# CANCELAR RESERVA
# ========================
@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    if request.method == "POST":
        # Guardamos datos del turno antes de eliminarlo
        barbero = reserva.barbero
        fecha = reserva.fecha
        hora_inicio = reserva.hora_inicio
        hora_fin = reserva.hora_fin

        # Cancelar/eliminar la reserva actual
        reserva.delete()

        # Buscar en lista de espera para ese barbero y fecha
        en_espera = ListaEspera.objects.filter(
            barbero=barbero,
            fecha=fecha
        ).order_by("creado_en").first()

        if en_espera:
            # Crear nueva reserva para el primer usuario en espera
            Reserva.objects.create(
                cliente=en_espera.cliente,
                barbero=barbero,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado="pendiente"
            )
            # Eliminarlo de la lista de espera
            en_espera.delete()

        return redirect("turno:dashboard")

    return render(request, "turno/cancelar_reserva.html", {"reserva": reserva})



# ========================
# AGENDA DEL BARBERO (su vista interna)
# ========================
@login_required
def turnos_barbero(request, id_barbero):
    """Agenda del barbero: lista todas sus reservas (pendientes o atendidas)."""
    barbero = get_object_or_404(Barbero, id=id_barbero)
    turnos = Reserva.objects.filter(barbero=barbero).order_by("fecha", "hora_inicio")
    return render(request, "turno/turnos_barbero.html", {
        "barbero": barbero,
        "turnos": turnos,
    })


@login_required
def atender_turno(request, id_barbero, reserva_id):
    """Marcar una reserva como atendida."""
    barbero = get_object_or_404(Barbero, id=id_barbero)
    turno = get_object_or_404(Reserva, id=reserva_id, barbero=barbero)

    turno.atendido = True
    turno.save()

    return redirect("turno:turnos_barbero", id_barbero=barbero.id)


# ========================
# DASHBOARD DE BARBEROS (vista rápida)
# ========================
@login_required
def barbero_dashboard(request):
    barbero = get_object_or_404(Barbero, usuario=request.user)
    reservas = Reserva.objects.filter(barbero=barbero, fecha=timezone.localdate())
    return render(request, "turno/barbero_dashboard.html", {"reservas": reservas})
