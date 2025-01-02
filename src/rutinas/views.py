from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Rutina, Sesion, EjercicioPersonalizado, SeriePersonalizada
from .serializers import RutinaSerializer, SesionSerializer, EjercicioPersonalizadoSerializer, SeriePersonalizadaSerializer

class RutinaFilter(filters.FilterSet):
    class Meta:
        model = Rutina
        fields = {
            'titulo': ['icontains'],
            'descripcion': ['exact'],
            'fecha_creacion': ['exact'],
        }

class RutinaList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RutinaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RutinaFilter

    def get_queryset(self):
        return Rutina.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class RutinaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RutinaSerializer

    def get_queryset(self):
        return Rutina.objects.filter(usuario=self.request.user)

class SesionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SesionSerializer

    def get_queryset(self):
        return Sesion.objects.filter(rutina__usuario=self.request.user)

    def perform_create(self, serializer):
        rutina = get_object_or_404(Rutina, id=self.request.data.get('rutina'), usuario=self.request.user)
        serializer.save(rutina=rutina)

class SesionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SesionSerializer

    def get_queryset(self):
        return Sesion.objects.filter(rutina__usuario=self.request.user)

    def perform_update(self, serializer):
        sesion = self.get_object()
        if (sesion.rutina.usuario != self.request.user):
            raise PermissionDenied("No tienes permiso para actualizar esta sesión.")
        serializer.save()

    def perform_destroy(self, instance):
        if (instance.rutina.usuario != self.request.user):
            raise PermissionDenied("No tienes permiso para eliminar esta sesión.")
        instance.delete()

class EjercicioPersonalizadoCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EjercicioPersonalizadoSerializer

    def get_queryset(self):
        return EjercicioPersonalizado.objects.filter(sesion__rutina__usuario=self.request.user)

    def perform_create(self, serializer):
        sesion = serializer.validated_data['sesion']
        if (sesion.rutina.usuario != self.request.user):
            raise PermissionDenied("No tiene permiso para agregar ejercicios a esta sesión.")
        serializer.save()

class EjercicioPersonalizadoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EjercicioPersonalizadoSerializer

    def get_queryset(self):
        return EjercicioPersonalizado.objects.filter(sesion__rutina__usuario=self.request.user).prefetch_related(
            Prefetch('series', queryset=SeriePersonalizada.objects.order_by('id'))
        )

    def perform_destroy(self, instance):
        # Opcionalmente, puedes agregar lógica adicional antes de eliminar
        # Por ejemplo, verificar si el usuario tiene permiso
        if (instance.sesion.rutina.usuario != self.request.user):
            raise PermissionDenied("No tienes permiso para eliminar este ejercicio.")
        instance.delete()

class UpdateOrderEjercicioPersonalizadoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Se espera que el cuerpo de la solicitud sea una lista de diccionarios con 'id' y 'peso_orden'
        data = request.data
        if not isinstance(data, list):
            return Response({'error': 'Formato de datos inválido. Se espera una lista.'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = request.user
        for item in data:
            ejercicio_id = item.get('id')
            peso_orden = item.get('peso_orden')
            if ejercicio_id is None or peso_orden is None:
                return Response({'error': 'Cada objeto debe contener "id" y "peso_orden".'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                ejercicio_personalizado = EjercicioPersonalizado.objects.get(
                    id=ejercicio_id,
                    sesion__rutina__usuario=usuario
                )
                ejercicio_personalizado.peso_orden = peso_orden
                ejercicio_personalizado.save()
            except EjercicioPersonalizado.DoesNotExist:
                return Response({'error': f'El ejercicio con ID {ejercicio_id} no existe o no tienes permiso.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'Orden actualizado correctamente.'}, status=status.HTTP_200_OK)

class SeriePersonalizadaCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SeriePersonalizadaSerializer

    def get_queryset(self):
        return SeriePersonalizada.objects.filter(
            ejercicio_personalizado__sesion__rutina__usuario=self.request.user
        )

    def perform_create(self, serializer):
        ejercicio_personalizado = serializer.validated_data['ejercicio_personalizado']
        if (ejercicio_personalizado.sesion.rutina.usuario != self.request.user):
            raise PermissionDenied("No tiene permiso para agregar series a este ejercicio.")
        serializer.save()

class SeriePersonalizadaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SeriePersonalizadaSerializer

    def get_queryset(self):
        return SeriePersonalizada.objects.filter(
            ejercicio_personalizado__sesion__rutina__usuario=self.request.user
        )

    def perform_create(self, serializer):
        ejercicio_personalizado_id = self.request.data.get('ejercicio_personalizado')
        ejercicio_personalizado = get_object_or_404(EjercicioPersonalizado, id=ejercicio_personalizado_id)
        serializer.save(ejercicio_personalizado=ejercicio_personalizado)

    def perform_update(self, serializer):
        # Verificar permisos antes de actualizar
        instance = serializer.instance
        if (instance.ejercicio_personalizado.sesion.rutina.usuario != self.request.user):
            raise PermissionDenied("No tienes permiso para modificar esta serie.")
        serializer.save()
