from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Barbero(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
 # 👈 Relación con el usuario
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

    def __str__(self):
        return f"Reserva de {self.cliente} con {self.barbero} el {self.fecha} a las {self.hora_inicio}"


class ListaEspera(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creado_en"]

    def __str__(self):
        return f"Espera de {self.cliente} con {self.barbero} el {self.fecha} a las {self.hora_inicio}"
