from rest_framework import serializers
from .models import Rutina, Sesion, EjercicioPersonalizado, SeriePersonalizada
from ejercicios.models import Ejercicio
from ejercicios.serializers import BaseEjercicioSerializer
from vagfit.utils import ImagenURLMixin

class SesionInRutinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = ['id', 'titulo']

class RutinaSerializer(serializers.ModelSerializer):
    sesion = SesionInRutinaSerializer(many=True, read_only=True)
    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Rutina
        fields = ['id', 'usuario', 'titulo', 'descripcion', 'imagen', 'fecha_creacion', 'sesion']

class SeriePersonalizadaSerializer(serializers.ModelSerializer):
    ejercicio_personalizado = serializers.PrimaryKeyRelatedField(queryset=EjercicioPersonalizado.objects.all())

    class Meta:
        model = SeriePersonalizada
        fields = ['id', 'ejercicio_personalizado', 'repeticiones', 'peso', 'velocidad_repeticion', 'descanso', 'rer']

class EjercicioPersonalizadoSerializer(serializers.ModelSerializer):
    series = SeriePersonalizadaSerializer(many=True, required=False)
    ejercicio = BaseEjercicioSerializer(read_only=True)
    ejercicio_id = serializers.PrimaryKeyRelatedField(
        queryset=Ejercicio.objects.all(),
        write_only=True,
        source='ejercicio'
    )
    sesion = serializers.PrimaryKeyRelatedField(queryset=Sesion.objects.all())

    class Meta:
        model = EjercicioPersonalizado
        fields = ['id', 'peso_orden', 'ejercicio', 'ejercicio_id', 'sesion', 'series']

    def create(self, validated_data):
        series_data = validated_data.pop('series', [])
        ejercicio_personalizado = EjercicioPersonalizado.objects.create(**validated_data)

        if not series_data:
            series_data = [{
                'repeticiones': 10,
                'peso': 5,
                'velocidad_repeticion': 2,
                'descanso': 60,
                'rer': 2
            }]

        for serie_data in series_data:
            SeriePersonalizada.objects.create(
                ejercicio_personalizado=ejercicio_personalizado,
                **serie_data
            )
        return ejercicio_personalizado

    def validate(self, data):
        sesion = data.get('sesion')
        if sesion and sesion.rutina.usuario != self.context['request'].user:
            raise serializers.ValidationError("No tiene permiso para agregar ejercicios a esta sesión.")
        return data

class SesionSerializer(serializers.ModelSerializer):
    ejercicios = serializers.SerializerMethodField()
    entrenando_ahora = serializers.SerializerMethodField()
    rutina = serializers.PrimaryKeyRelatedField(queryset=Rutina.objects.all())

    class Meta:
        model = Sesion
        fields = ['id', 'titulo', 'entrenando_ahora', 'rutina', 'ejercicios']

    def get_ejercicios(self, obj):
        ejercicios_personalizados = obj.ejerciciopersonalizado_set.all().order_by('peso_orden')
        return EjercicioPersonalizadoSerializer(ejercicios_personalizados, many=True, context=self.context).data

    def get_entrenando_ahora(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            usuario = request.user
            entrenamiento_activo = obj.entrenamiento_set.filter(usuario=usuario, fin__isnull=True).first()
            return entrenamiento_activo.id if entrenamiento_activo else False
        return False

    def validate_rutina(self, value):
        if value.usuario != self.context['request'].user:
            raise serializers.ValidationError("No tiene permiso para modificar esta rutina.")
        return value
