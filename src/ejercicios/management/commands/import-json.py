import json
from django.core.management.base import BaseCommand
from django.core.files import File
from pathlib import Path
from django.utils._os import safe_join
from ejercicios.models import Ejercicio, Equipamiento, Musculo, Categoria

class Command(BaseCommand):
    help = 'Importa ejercicios desde un archivo JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, nargs='?', default='/app/exercises_translated.json', help='Ruta del archivo JSON a importar')

    def handle(self, *args, **kwargs):
        json_path = kwargs['json_path']
        try:
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
                for item in data:
                    # Función para manejar "N/A" o "N / A" y reemplazar por "Otros"
                    def procesar_otros(valor):
                        if valor.strip().lower() in ['n/a', 'n / a', 'otro', 'otros']:
                            return 'Otros'
                        return valor.strip().capitalize()

                    # Procesar o crear la categoría
                    categoria_nombre = procesar_otros(item.get('category', 'Sin categoría'))
                    categoria, created = Categoria.objects.get_or_create(titulo=categoria_nombre)

                    # Procesar o crear el equipamiento
                    equipamiento_nombre = procesar_otros(item.get('equipment', 'Sin equipamiento'))
                    equipamiento, created = Equipamiento.objects.get_or_create(titulo=equipamiento_nombre)

                    # Procesar o crear los músculos primarios
                    primary_muscle = None
                    primary_muscles = item.get('primaryMuscles', '')
                    if primary_muscles:
                        musculo_primario_nombre = procesar_otros(primary_muscles.split(',')[0])
                        primary_muscle, created = Musculo.objects.get_or_create(titulo=musculo_primario_nombre)

                    # Procesar o crear los músculos secundarios
                    secondary_muscle = None
                    secondary_muscles = item.get('secondaryMuscles', '')
                    if secondary_muscles:
                        musculo_secundario_nombre = procesar_otros(secondary_muscles.split(',')[0])
                        secondary_muscle, created = Musculo.objects.get_or_create(titulo=musculo_secundario_nombre)

                    # Crear o actualizar el ejercicio
                    ejercicio, created = Ejercicio.objects.get_or_create(
                        nombre=item.get('name'),
                        defaults={
                            'instrucciones': "\n".join(item.get('instructions', [])),
                            'categoria': categoria,
                            'equipamiento': equipamiento,
                            'musculo_primario': primary_muscle,
                            'musculo_secundario': secondary_muscle
                        }
                    )

                    # Guardar las imágenes
                    images = item.get('images', [])
                    if len(images) > 0:
                        image_path = safe_join('/free-exercise-db', images[0])
                        ejercicio.imagen_uno.save(images[0], File(open(Path(image_path), 'rb')))
                    if len(images) > 1:
                        image_path = safe_join('/free-exercise-db', images[1])
                        ejercicio.imagen_dos.save(images[1], File(open(Path(image_path), 'rb')))

                    ejercicio.save()
                    self.stdout.write(self.style.SUCCESS(f"Ejercicio '{ejercicio.nombre}' importado correctamente."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante la importación: {e}"))
