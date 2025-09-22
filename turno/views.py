from django.shortcuts import render, redirect, get_object_or_404
from .models import Barbero
from .forms import FormularioReserva
from .utils import available_slots_for_barber, is_slot_available
from datetime import time, date as date_cls
from .estructura import ListaTurnos
from django.contrib.auth.decorators import login_required

INICIO_TRABAJO = time(8, 0)
FIN_TRABAJO = time(17, 0)
RANGO_ATENCION = 60

# Instancia global
lista_turnos = ListaTurnos()

@login_required
def dashboard(request):
    """
    Muestra el dashboard del usuario.
    Si el usuario ya tiene un turno, se pasa al template para mostrar la opción de cancelarlo.
    """
    turno_usuario = lista_turnos.buscar_turno_por_correo(request.user.email)

    context = {
        "turno_usuario": turno_usuario,
    }
    return render(request, "turno/dashboard.html", context)

def seleccionar_barbero(request):
    if request.method == "POST":
        id_barbero = request.POST.get("barbero")
        if id_barbero:
            return redirect("turno:formulario_reserva", id_barbero=id_barbero)

    barberos = Barbero.objects.all()
    return render(request, "turno/seleccionar_barbero.html", {"barberos": barberos})

def formulario_reserva(request, id_barbero):
    # Si el usuario ya tiene turno, redirigirlo al dashboard
    turno_existente = lista_turnos.buscar_turno_por_correo(request.user.email)
    if turno_existente:
        return redirect("turno:dashboard")

    barber = None
    if id_barbero and str(id_barbero).isdigit() and int(id_barbero) != 0:
        barber = Barbero.objects.filter(id=id_barbero).first()

    if request.method == "POST":
        form = FormularioReserva(request.POST)
        if form.is_valid():
            d = form.cleaned_data["fecha"]
            t = form.cleaned_data["hora"]
            nombre = form.cleaned_data["nombre_cliente"]
            correo = form.cleaned_data["correo_cliente"]

            if barber is None:
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

            # Guardar en lista en memoria
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

def turnos_barbero(request, id_barbero):
    barbero = get_object_or_404(Barbero, id=id_barbero)
    turnos = lista_turnos.mostrar_turnos_barbero(int(id_barbero))
    return render(
        request, "turno/ver_turnos_barbero.html", {"turnos": turnos, "barbero": barbero}
    )

def reserva_confirmada(request):
    return render(request, "turno/reserva_confirmada.html")

def barbero_dashboard(request):
    barberos = Barbero.objects.all()
    return render(request, "turno/barbero_dashboard.html", {"barberos": barberos})

@login_required
def cancelar_turno(request):
    """
    Cancela el turno del usuario logueado y lo redirige al dashboard.
    """
    if request.method == "POST":
        lista_turnos.eliminar_turno_por_correo(request.user.email)
        return redirect("turno:dashboard")
    return redirect("turno:dashboard")

def atender_turno(request, id_barbero, cliente_nombre):
    if request.method == "POST":
        lista_turnos.atender_turno(cliente_nombre, int(id_barbero))
        return redirect("turno:turnos_barbero", id_barbero=id_barbero)
    return redirect("turno:turnos_barbero", id_barbero=id_barbero)
