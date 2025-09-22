from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.base import RedirectView

app_name = "turno"

urlpatterns = [
    path("cancelar-turno/", views.cancelar_turno, name="cancelar_turno"),

     path('', RedirectView.as_view(url='/login/', permanent=False)),
    path(
        "login/", auth_views.LoginView.as_view(template_name="turno/login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reservar/", views.seleccionar_barbero, name="seleccionar_barbero"),
    path(
        "reservar/formulario/<int:id_barbero>/",
        views.formulario_reserva,
        name="formulario_reserva",
    ),
    path("reservar/confirmado/", views.reserva_confirmada, name="reserva_confirmada"),
    path("dashboard/b/", views.barbero_dashboard, name="dashboard_barbero"),
    path(
        "dashboard/b/turnos/<int:id_barbero>",
        views.turnos_barbero,
        name="turnos_barbero",
    ),
    path(
        "dashboard/b/atender/<int:id_barbero>/<str:cliente_nombre>/",
        views.atender_turno,
        name="atender_turno",
    ),
]
