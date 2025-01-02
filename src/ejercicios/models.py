from django.db import models

class Equipamiento(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='equipamiento/')

    def __str__(self):
        return self.titulo

class Musculo(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='musculos/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Categoria(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categoria/')

    def __str__(self):
        return self.titulo

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='ejercicios', null=True, blank=True)
    imagen_uno = models.ImageField(upload_to='ejercicios/', null=True, blank=True)
    imagen_dos = models.ImageField(upload_to='ejercicios/', null=True, blank=True)
    instrucciones = models.TextField(null=True, blank=True)
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE, related_name='ejercicios', null=True, blank=True)
    musculo_primario = models.ForeignKey(Musculo, related_name='ejercicios_principales', on_delete=models.CASCADE, null=True, blank=True)
    musculo_secundario = models.ForeignKey(Musculo, related_name='ejercicios_secundarios', on_delete=models.CASCADE, null=True, blank=True)
    realizar_por_extremidad = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre