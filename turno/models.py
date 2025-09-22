from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Barbero(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=200)

    class Meta:
        db_table = 'barbero'

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ("barbero", "fecha", "hora_inicio")


class ListaEspera(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creado_en"]


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("P", "Pendiente"),
        ("C", "Confirmado"),
        ("X", "Cancelado"),
        ("F", "Finalizado"),
    ]

    barber = models.ForeignKey(
        Barbero, on_delete=models.CASCADE, related_name="reservations"
    )
    client_name = models.CharField(max_length=120)
    client_email = models.EmailField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("barber", "date", "time")
        ordering = ["date", "time"]  #  Para listar reservas cronológicamente

    def __str__(self):
        return f"Reserva de {self.client_name} con {self.barber.name} el {self.date} a las {self.time}"
