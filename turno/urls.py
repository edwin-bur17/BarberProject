from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views

app_name = "turno"

urlpatterns = [
    path("reserva/<int:id>/estado/", views.actualizar_estado, name="actualizar_estado"),
    path("panel-barbero/", views.panel_barbero, name="panel_barbero"),

    path("barbero/<int:id_barbero>/atender/<int:id_turno>/", views.atender_turno, name="atender_turno"),

    path("reservar/crear/", views.crear_reserva, name="crear_reserva"),
    # Dashboard de barberos
path("dashboard/b/turnos/<int:id_barbero>/", views.turnos_barbero, name="turnos_barbero"),
path("dashboard/b/atender/<int:id_barbero>/<str:cliente_nombre>/", views.atender_turno, name="atender_turno"),

    path("reserva_confirmada/<int:reserva_id>/", views.reserva_confirmada, name="reserva_confirmada"),

    # Redirige la raíz al login
    path("", RedirectView.as_view(url="/login/", permanent=False)),

    # Autenticación
    path("login/", auth_views.LoginView.as_view(template_name="turno/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Dashboard general
    path("dashboard/", views.dashboard, name="dashboard"),

    # Flujo de reservas (📌 quitamos seleccionar_barbero y formulario_reserva porque ya no se usan)
    path("reservar/cancelar/<int:reserva_id>/", views.cancelar_reserva, name="cancelar_reserva"),

    # Agenda por barbero
    path("agenda/<int:id_barbero>/", views.agenda_barbero, name="agenda_barbero"),

    # Dashboard de barberos
    path("dashboard/b/", views.barbero_dashboard, name="dashboard_barbero"),
    path("dashboard/b/turnos/<int:id_barbero>/", views.turnos_barbero, name="turnos_barbero"),
    path("dashboard/b/atender/<int:id_barbero>/<str:cliente_nombre>/", views.atender_turno, name="atender_turno"),
]
