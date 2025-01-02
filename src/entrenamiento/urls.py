from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntrenamientoViewSet, EjercicioRealizadoViewSet, SerieRealizadaViewSet
from . import views

router = DefaultRouter()
router.register(r'entrenamientos', EntrenamientoViewSet, basename='entrenamiento')
router.register(r'ejercicios-realizados', EjercicioRealizadoViewSet, basename='ejercicio-realizado')
router.register(r'series-realizadas', SerieRealizadaViewSet, basename='serie-realizada')

urlpatterns = [
    path('', include(router.urls)),
    path('series-realizadas/', views.SerieRealizadaCreateAPIView.as_view(), name='series-realizadas-create'),
    path('entrenamientos/resumen-entrenamientos/', views.EntrenamientoViewSet.as_view({'get': 'resumen_entrenamientos'}), name='resumen-entrenamientos'),
]
