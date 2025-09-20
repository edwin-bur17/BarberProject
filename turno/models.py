from django.db import models

class Barbero(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=200)

    class Meta:
        db_table = 'barbero'

    def __str__(self):
        return self.nombre



class Reservation(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendiente'),
        ('C', 'Confirmado'),
        ('X', 'Cancelado'),
        ('F', 'Finalizado'),
    ]

    barber = models.ForeignKey(
        Barbero,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    client_name = models.CharField(max_length=120)
    client_email = models.EmailField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('barber', 'date', 'time')
        ordering = ['date', 'time']  #  Para listar reservas cronológicamente

    def __str__(self):
        return f"Reserva de {self.client_name} con {self.barber.name} el {self.date} a las {self.time}"
