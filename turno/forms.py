from django import forms
from .models import Barbero
import datetime

class SelectBarberForm(forms.Form):
    barber = forms.ModelChoiceField(
        queryset=Barbero.objects.all(),
        required=False,
        empty_label="Cualquiera",
        label="Barbero"
    )

# Formulario para hacer una reserva
class FormularioReserva(forms.Form):
    fecha = forms.DateField(
        label="Fecha:",
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )
    hora = forms.TimeField(
        label="Hora:",
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    nombre_cliente = forms.CharField(
        label="Nombre:",
        max_length=120
    )
    correo_cliente = forms.EmailField(
        label="Correo:",
        required=False
    )
