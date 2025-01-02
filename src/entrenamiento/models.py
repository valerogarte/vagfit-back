from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from ejercicios.models import Ejercicio
from rutinas.models import Sesion

User = get_user_model()

class Entrenamiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, null=True, blank=True)
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Entrenamiento de {self.usuario.username} iniciado el {self.inicio}'

class EjercicioRealizado(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, null=True, blank=True)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.ejercicio.nombre if self.ejercicio else "Sin ejercicio"}'

class SerieRealizada(models.Model):
    ejercicio_realizado = models.ForeignKey(
        EjercicioRealizado,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='series'
    )
    repeticiones = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    peso = models.FloatField(default=0, validators=[MinValueValidator(0)])
    velocidad_repeticion = models.FloatField(default=0, validators=[MinValueValidator(0)])
    descanso = models.IntegerField(default=60, validators=[MinValueValidator(0)])
    rer = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(null=True, blank=True)
    realizada = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    extra = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.ejercicio_realizado.ejercicio.nombre if self.ejercicio_realizado and self.ejercicio_realizado.ejercicio else "Sin ejercicio"}'
