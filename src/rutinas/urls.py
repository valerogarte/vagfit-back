from django.urls import path
from .views import RutinaList, RutinaDetailAPIView, SesionListCreateAPIView, SeriePersonalizadaDetailAPIView, EjercicioPersonalizadoCreateAPIView, UpdateOrderEjercicioPersonalizadoAPIView, SeriePersonalizadaCreateAPIView
from . import views

urlpatterns = [
    path('rutina/', RutinaList.as_view(), name='rutina-list'),
    path('rutina/<int:pk>/', RutinaDetailAPIView.as_view(), name='rutina-detail'),
    path('sesion/', SesionListCreateAPIView.as_view(), name='sesion-list-create'),
    path('sesion/<int:pk>/', views.SesionDetailAPIView.as_view(), name='sesiones-detail'),
    path('ejercicios-sesion/', EjercicioPersonalizadoCreateAPIView.as_view(), name='ejercicio-personalizado-create'),
    path('ejercicios-sesion/<int:pk>/', views.EjercicioPersonalizadoDetailAPIView.as_view(), name='ejercicios-sesion-detail'),
    path('ejercicios-sesion/update-order/', UpdateOrderEjercicioPersonalizadoAPIView.as_view(), name='update_ejercicio_personalizado_order'),
    path('series/', SeriePersonalizadaCreateAPIView.as_view(), name='serie-personalizada-create'),
    path('series/<int:pk>/', views.SeriePersonalizadaDetailAPIView.as_view(), name='series-detail'),
]
