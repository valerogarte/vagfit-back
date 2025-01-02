from rest_framework import serializers
from .models import Entrenamiento, EjercicioRealizado, SerieRealizada
from ejercicios.models import Ejercicio
from ejercicios.serializers import (CategoriaSerializer, EquipamientoSerializer, MusculoSerializer, BaseEjercicioSerializer)
from vagfit.utils import ImagenURLMixin

class SerieRealizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerieRealizada
        fields = ['id', 'ejercicio_realizado', 'repeticiones', 'peso', 'velocidad_repeticion', 'descanso', 'rer', 'inicio', 'fin', 'realizada', 'extra', 'deleted']

class EjercicioRealizadoSerializer(serializers.ModelSerializer):
    series = SerieRealizadaSerializer(many=True, read_only=True)
    ejercicio = BaseEjercicioSerializer(read_only=True)

    class Meta:
        model = EjercicioRealizado
        fields = ['id', 'ejercicio', 'series']

class EntrenamientoSerializer(serializers.ModelSerializer):
    ejercicios = serializers.SerializerMethodField()
    titulo = serializers.SerializerMethodField()
    rutina = serializers.SerializerMethodField()

    class Meta:
        model = Entrenamiento
        fields = ['id', 'titulo', 'inicio', 'fin', 'rutina', 'ejercicios']

    def get_titulo(self, obj):
        return obj.sesion.titulo if obj.sesion else None

    def get_rutina(self, obj):
        if obj.sesion and obj.sesion.rutina:
            rutina = obj.sesion.rutina
            return {
                'id': rutina.id,
                'titulo': rutina.titulo,
                'imagen': self.context['request'].build_absolute_uri(rutina.imagen.url) if rutina.imagen else None
            }
        return None

    def get_ejercicios(self, obj):
        ejercicios_realizados = obj.ejerciciorealizado_set.all()
        return EjercicioRealizadoSerializer(ejercicios_realizados, many=True, context=self.context).data
