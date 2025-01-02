from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ejercicio, Musculo, Equipamiento, Categoria
from .serializers import BaseEjercicioSerializer, MusculoSerializer, EquipamientoSerializer, CategoriaSerializer
from django.db.models import Q
import unicodedata

class EjercicioFilter(filters.FilterSet):
    nombre = filters.CharFilter(method='filter_by_nombre')

    class Meta:
        model = Ejercicio
        fields = {
            'id': ['exact'],
            'nombre': ['icontains'],
            'categoria': ['exact'],
            'equipamiento': ['exact'],
            'musculo_primario': ['exact'],
            'musculo_secundario': ['exact'],
        }

    def filter_by_nombre(self, queryset, name, value):
        def normalize(s):
            return ''.join(
                c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn'
            ).lower()

        for word in value.split():
            normalized_word = normalize(word)
            queryset = queryset.filter(
                Q(nombre__icontains=word) | Q(nombre__icontains=normalized_word)
            )
        return queryset

class EjercicioList(generics.ListAPIView):
    queryset = Ejercicio.objects.all()
    serializer_class = BaseEjercicioSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EjercicioFilter

class EjercicioDetail(generics.RetrieveAPIView):
    queryset = Ejercicio.objects.all()
    serializer_class = BaseEjercicioSerializer

class DatosEjercicios(APIView):
    def get(self, request):
        musculos = Musculo.objects.all().order_by('titulo')
        equipamientos = Equipamiento.objects.all().order_by('titulo')
        categorias = Categoria.objects.all().order_by('titulo')

        musculos_data = MusculoSerializer(musculos, many=True).data
        equipamientos_data = EquipamientoSerializer(equipamientos, many=True).data
        categorias_data = CategoriaSerializer(categorias, many=True).data

        data = {
            "musculos": musculos_data,
            "equipamientos": equipamientos_data,
            "categorias": categorias_data
        }

        return Response(data)