from rest_framework import serializers
from .models import Ejercicio, Categoria, Equipamiento, Musculo
from vagfit.utils import ImagenURLMixin

class BaseImagenSerializer(ImagenURLMixin, serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_imagen(self, obj):
        return self.get_imagen_url(obj, 'imagen')

class CategoriaSerializer(BaseImagenSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'titulo', 'imagen']

class EquipamientoSerializer(BaseImagenSerializer):
    class Meta:
        model = Equipamiento
        fields = ['id', 'titulo', 'imagen']

class MusculoSerializer(BaseImagenSerializer):
    class Meta:
        model = Musculo
        fields = ['id', 'titulo', 'imagen']

class BaseEjercicioSerializer(ImagenURLMixin, serializers.ModelSerializer):
    imagen_uno = serializers.SerializerMethodField()
    imagen_dos = serializers.SerializerMethodField()
    categoria = CategoriaSerializer(read_only=True)
    equipamiento = EquipamientoSerializer(read_only=True)
    musculo_primario = MusculoSerializer(read_only=True)
    musculo_secundario = MusculoSerializer(read_only=True)

    class Meta:
        model = Ejercicio
        fields = ['id', 'nombre', 'categoria', 'imagen_uno', 'imagen_dos', 'instrucciones', 'equipamiento', 'musculo_primario', 'musculo_secundario', 'realizar_por_extremidad']

    def get_imagen_uno(self, obj):
        return self.get_imagen_url(obj, 'imagen_uno')

    def get_imagen_dos(self, obj):
        return self.get_imagen_url(obj, 'imagen_dos')

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre es obligatorio.")
        return value

    def validate(self, data):
        if not data.get('nombre'):
            raise serializers.ValidationError({'nombre': 'El nombre es obligatorio.'})
        return data