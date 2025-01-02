from django.urls import path
from .views import EjercicioList, EjercicioDetail
from .views import DatosEjercicios

urlpatterns = [
    path('ejercicios/', EjercicioList.as_view(), name='ejercicio-list'),
    path('ejercicios/<int:pk>/', EjercicioDetail.as_view(), name='ejercicio-detail'),
    path('datos-ejercicios/', DatosEjercicios.as_view(), name='datos-ejercicios'),
]
