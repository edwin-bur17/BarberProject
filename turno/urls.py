from django.urls import path
from . import views

app_name = 'turno'

urlpatterns = [
    path('', views.home, name='home'),
    path('reservar/', views.seleccionar_barbero, name='seleccionar_barbero'),
    path('reservar/formulario/<int:id_barbero>/', views.formulario_reserva, name='formulario_reserva'),
    path('reservar/confirmado/', views.reserva_confirmada, name='reserva_confirmada'),
    path('dashboard/b/', views.barbero_dashboard, name='dashboard_barbero'),
    path('dashboard/b/turnos/<int:id_barbero>', views.turnos_barbero, name='turnos_barbero'),
    path('dashboard/b/atender/<int:id_barbero>/<str:cliente_nombre>/', views.atender_turno, name='atender_turno'),

]
