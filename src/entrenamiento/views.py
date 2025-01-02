from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import EntrenamientoSerializer, EjercicioRealizadoSerializer, SerieRealizadaSerializer
from .models import Entrenamiento, EjercicioRealizado, SerieRealizada
from rutinas.models import Sesion, EjercicioPersonalizado, SeriePersonalizada

class EntrenamientoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EntrenamientoSerializer

    def get_queryset(self):
        return Entrenamiento.objects.filter(usuario=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        sesion_id = request.data.get('sesion')
        usuario = request.user

        entrenamiento_activo = Entrenamiento.objects.filter(
            sesion_id=sesion_id, usuario=usuario, fin__isnull=True
        ).exists()

        if entrenamiento_activo:
            return Response(
                {'error': 'Ya existe un entrenamiento activo para esta sesión.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sesion = Sesion.objects.get(id=sesion_id)
            entrenamiento = serializer.save(usuario=usuario, sesion=sesion)

            ejercicios_personalizados = EjercicioPersonalizado.objects.filter(sesion=sesion)

            if not ejercicios_personalizados.exists():
                return Response({'error': f'La sesión {sesion_id} no tiene ejercicios vinculados.'}, status=status.HTTP_400_BAD_REQUEST)

            for ejercicio_personalizado in ejercicios_personalizados:
                if not ejercicio_personalizado.ejercicio:
                    return Response({'error': f'El ejercicio personalizado {ejercicio_personalizado.id} no tiene un ejercicio asociado.'}, status=status.HTTP_400_BAD_REQUEST)

                ejercicio_realizado = EjercicioRealizado.objects.create(
                    ejercicio=ejercicio_personalizado.ejercicio,
                    entrenamiento=entrenamiento
                )

                series_personalizadas = SeriePersonalizada.objects.filter(ejercicio_personalizado=ejercicio_personalizado)

                if not series_personalizadas.exists():
                    return Response({'error': f'El ejercicio {ejercicio_personalizado.ejercicio.nombre} no tiene series asociadas.'}, status=status.HTTP_400_BAD_REQUEST)

                for serie_personalizada in series_personalizadas:
                    SerieRealizada.objects.create(
                        ejercicio_realizado=ejercicio_realizado,
                        repeticiones=serie_personalizada.repeticiones,
                        peso=serie_personalizada.peso,
                        velocidad_repeticion=serie_personalizada.velocidad_repeticion,
                        descanso=serie_personalizada.descanso,
                        rer=serie_personalizada.rer,
                        realizada=False,
                        extra=False
                    )

            entrenamiento_serializer = EntrenamientoSerializer(entrenamiento, context={'request': request})
            return Response(entrenamiento_serializer.data, status=status.HTTP_201_CREATED)

        except Sesion.DoesNotExist:
            return Response({'error': f'Sesión con ID {sesion_id} no encontrada.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='finalizar')
    def finalizar_entrenamiento(self, request, pk=None):
        entrenamiento = get_object_or_404(Entrenamiento, pk=pk)

        if entrenamiento.fin is not None:
            return Response(
                {'error': 'El entrenamiento ya ha sido finalizado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        entrenamiento.fin = timezone.now()
        entrenamiento.save()

        serializer = self.get_serializer(entrenamiento, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='resumen-entrenamientos')
    def resumen_entrenamientos(self, request):
        ejercicios_realizados = EjercicioRealizado.objects.filter(
            entrenamiento__usuario=request.user
        ).select_related('ejercicio').order_by('-id')[:15]

        summary = []
        for er in ejercicios_realizados:
            summary.append({
                'ejercicioId': er.ejercicio.id if er.ejercicio else None,
                'ejercicioNombre': er.ejercicio.nombre if er.ejercicio else 'Sin nombre',
                'fecha': er.entrenamiento.inicio,
            })

        return Response({'summary': summary}, status=status.HTTP_200_OK)

class EjercicioRealizadoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EjercicioRealizadoSerializer

    def get_queryset(self):
        return EjercicioRealizado.objects.filter(entrenamiento__usuario=self.request.user).prefetch_related(
            models.Prefetch('series', queryset=SerieRealizada.objects.order_by('id'))
        )


class SerieRealizadaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SerieRealizadaSerializer

    def get_queryset(self):
        return SerieRealizada.objects.filter(ejercicio_realizado__entrenamiento__usuario=self.request.user)

    @action(detail=True, methods=['patch'], url_path='delete')
    def actualizar_deleted(self, request, pk=None):
        serie = get_object_or_404(SerieRealizada, pk=pk)
        deleted = request.data.get('deleted')
        if deleted is None:
            return Response(
                {'error': 'El campo "deleted" es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serie.deleted = bool(deleted)
        serie.save()

        serializer = self.get_serializer(serie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='actualizar')
    def actualizar_datos(self, request, pk=None):
        # Obtener el objeto SerieRealizada usando el ID
        serie = get_object_or_404(SerieRealizada, pk=pk)

        # Validar y obtener los datos de la solicitud
        data = request.data

        # Actualizar solo los campos que están presentes en la solicitud
        for field in ['realizada', 'peso', 'repeticiones', 'velocidad_repeticion', 'descanso', 'rer', 'extra', 'deleted']:
            if field in data:
                setattr(serie, field, data[field])

        # Guardar la instancia actualizada
        serie.save()

        # Serializar y devolver la respuesta actualizada
        serializer = self.get_serializer(serie)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SerieRealizadaCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SerieRealizadaSerializer

    def perform_create(self, serializer):
        ejercicio_realizado_id = self.request.data.get('ejercicio_realizado')
        ejercicio_realizado = get_object_or_404(
            EjercicioRealizado,
            id=ejercicio_realizado_id,
            entrenamiento__usuario=self.request.user
        )
        serializer.save(ejercicio_realizado=ejercicio_realizado)