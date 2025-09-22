from django.shortcuts import render, redirect, get_object_or_404
from .models import Barbero, Reserva
from .forms import FormularioReserva
from .utils import available_slots_for_barber, is_slot_available, FRANJAS
from datetime import time, date as date_cls
from .estructura import ListaTurnos
from django.contrib.auth.decorators import login_required
from datetime import datetime

INICIO_TRABAJO = time(8, 0)
FIN_TRABAJO = time(17, 0)
RANGO_ATENCION = 60


@login_required()
def dashboard(request):
    barberos = Barbero.objects.all()  
    return render(request, "turno/dashboard.html", {'barberos': barberos})


# Instancia global (por ejemplo)
lista_turnos = ListaTurnos()

# Formulario seleccionar barbero
def seleccionar_barbero(request):
    if request.method == "POST":
        id_barbero = request.POST.get("barbero")
        if id_barbero:
            return redirect("turno:formulario_reserva", id_barbero=id_barbero)

    barberos = Barbero.objects.all()

    return render(request, "turno/seleccionar_barbero.html", {"barberos": barberos})

# Agenda del barbero
def agenda_barbero(request, id_barbero):
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    else:
        # Si no viene parámetro, usar hoy
        fecha = date_cls.today()

    barbero = Barbero.objects.get(id=id_barbero)

    # Reservas existentes
    reservas = Reserva.objects.filter(barbero=barbero, fecha=fecha)
    ocupados = {r.hora_inicio for r in reservas}

    # Generar lista con estado
    slots = []
    for inicio, fin in FRANJAS:
        slots.append({
            "inicio": inicio,
            "fin": fin,
            "disponible": inicio not in ocupados
        })

    return render(request, "turno/agenda_barbero.html", {
        "barbero": barbero,
        "fecha": fecha,
        "slots": slots
    })

# Formulario de hacer una reserva
def formulario_reserva(request, id_barbero):
    # Manejo seguro del barber_id
    barber = None
    if id_barbero and str(id_barbero).isdigit() and int(id_barbero) != 0:
        barber = Barbero.objects.filter(id=id_barbero).first()

    # Formulario:
    if request.method == "POST":
        form = FormularioReserva(request.POST)
        if form.is_valid():
            d = form.cleaned_data["fecha"]
            t = form.cleaned_data["hora"]
            nombre = form.cleaned_data["nombre_cliente"]
            correo = form.cleaned_data["correo_cliente"]

            if barber is None:
                # Buscar primer barbero disponible
                for b in Barbero.objects.all():
                    if is_slot_available(b, d, t, duration_minutes=RANGO_ATENCION):
                        barber = b
                        break
                if not barber:
                    return render(
                        request,
                        "turno/formulario_reserva.html",
                        {"form": form, "error": "No hay disponibilidad"},
                    )
            else:
                if not is_slot_available(barber, d, t, duration_minutes=RANGO_ATENCION):
                    return render(
                        request,
                        "turno/formulario_reserva.html",
                        {"form": form, "error": "No disponible"},
                    )

            #  Guardar en lista en memoria
            lista_turnos.agregar_turno(
                cliente=nombre,
                fecha=d,
                hora=t,
                correo=correo,
                id_barbero=id_barbero,
            )

            return redirect("turno:reserva_confirmada")
    else:
        form = FormularioReserva(initial={"date": date_cls.today()})

    slots = []
    if barber:
        today = date_cls.today()
        slots = available_slots_for_barber(
            barber, today, INICIO_TRABAJO, FIN_TRABAJO, RANGO_ATENCION, RANGO_ATENCION
        )

    return render(
        request,
        "turno/formulario_reserva.html",
        {"form": form, "barbero": barber, "slots": slots},
    )

# turnos por barbero
def turnos_barbero(request, id_barbero):
    barbero = get_object_or_404(Barbero, id=id_barbero)
    turnos = lista_turnos.mostrar_turnos_barbero(int(id_barbero))
    print("turnos -->", turnos)
    return render(
        request, "turno/ver_turnos_barbero.html", {"turnos": turnos, "barbero": barbero}
    )

# vista de reserva confirmada
def reserva_confirmada(request):
    return render(request, "turno/reserva_confirmada.html")

# tablero de los peluqueros
def barbero_dashboard(request):
    barberos = Barbero.objects.all()
    print("barberos -->", barberos)
    return render(request, "turno/barbero_dashboard.html", {"barberos": barberos})


# Marca un turno como atendido y lo elimina de la lista
def atender_turno(request, id_barbero, cliente_nombre):
    """
    Marca un turno como atendido y lo elimina de la lista
    """
    if request.method == "POST":
        # # Verificar que el barbero existe
        # barbero = get_object_or_404(Barbero, id=id_barbero)

        # Procesar el turno (marcar como atendido y eliminar)
        resultado = lista_turnos.atender_turno(cliente_nombre, int(id_barbero))

        if not resultado:
            pass

        return redirect("turno:turnos_barbero", id_barbero=id_barbero)

    # Si no es POST, redireccionar sin hacer nada
    return redirect("turno:turnos_barbero", id_barbero=id_barbero)
