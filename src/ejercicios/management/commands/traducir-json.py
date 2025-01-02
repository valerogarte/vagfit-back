import os
import json
from django.core.management.base import BaseCommand
from deep_translator import GoogleTranslator
import sys

def split_text(text, max_length=5000):
    """
    Divide un texto en fragmentos que no excedan max_length palabras.
    """
    words = text.split()
    fragments = []
    current_fragment = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            fragments.append(' '.join(current_fragment))
            current_fragment = [word]
            current_length = len(word)
        else:
            current_fragment.append(word)
            current_length += len(word) + 1

    if current_fragment:
        fragments.append(' '.join(current_fragment))

    return fragments

def translate_large_text(translator, text):
    """
    Traduce un texto que puede ser mayor a 5000 caracteres.
    """
    try:
        fragments = split_text(text)
        translated_fragments = [translator.translate(fragment) for fragment in fragments]
        return ''.join(translated_fragments)
    except Exception as e:
        print(f"Error al traducir el texto: {e}")
        return text

class Command(BaseCommand):
    help = 'Importa ejercicios desde /free-exercise-db/dist/exercises.json, los traduce, y genera un nuevo archivo traducido.'

    def handle(self, *args, **kwargs):
        input_file_path = '/free-exercise-db/dist/exercises.json'  # Archivo original
        output_file_path = '/free-exercise-db/dist/exercises_translated.json'  # Nuevo archivo traducido
        translator = GoogleTranslator(source='en', target='es')

        # Verificar si el archivo original existe
        if not os.path.exists(input_file_path):
            self.stdout.write(self.style.ERROR(f'Error: El archivo {input_file_path} no existe.'))
            return

        # Cargar el archivo JSON original
        try:
            with open(input_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                self.stdout.write(self.style.SUCCESS(f'Archivo JSON cargado correctamente.'))

                # Obtener el total de ejercicios
                total_exercises = len(data)

                # Traducir los datos
                translated_data = []
                for idx, exercise in enumerate(data, start=1):
                    name = exercise.get('name')
                    description = exercise.get('description', '')
                    instructions = exercise.get('instructions', [])

                    # Traducir el nombre, descripción y las instrucciones al español
                    try:
                        name_translated = translator.translate(name)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir el nombre: {e}"))
                        name_translated = name
                    
                    description_translated = translate_large_text(translator, description)
                    instructions_translated = []
                    for inst in instructions:
                        try:
                            translated_instruction = translate_large_text(translator, inst)
                            instructions_translated.append(translated_instruction)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error al traducir la instrucción: {e}"))
                            instructions_translated.append(inst)
                    
                    # Manejar posibles errores con valores que no sean texto (listas, etc.)
                    try:
                        force_translated = translator.translate(exercise.get('force', '') or 'N/A')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'force': {e}"))
                        force_translated = exercise.get('force', 'N/A')
                    
                    try:
                        level_translated = translator.translate(exercise.get('level', '') or 'N/A')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'level': {e}"))
                        level_translated = exercise.get('level', 'N/A')
                    
                    try:
                        mechanic_translated = translator.translate(exercise.get('mechanic', '') or 'N/A')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'mechanic': {e}"))
                        mechanic_translated = exercise.get('mechanic', 'N/A')
                    
                    try:
                        equipment_translated = translator.translate(exercise.get('equipment', '') or 'N/A')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'equipment': {e}"))
                        equipment_translated = exercise.get('equipment', 'N/A')
                    
                    try:
                        primaryMuscles = exercise.get('primaryMuscles', [])
                        primaryMuscles_translated = translator.translate(', '.join(primaryMuscles)) if primaryMuscles else 'N/A'
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'primaryMuscles': {e}"))
                        primaryMuscles_translated = primaryMuscles
                    
                    try:
                        secondaryMuscles = exercise.get('secondaryMuscles', [])
                        secondaryMuscles_translated = translator.translate(', '.join(secondaryMuscles)) if secondaryMuscles else 'N/A'
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'secondaryMuscles': {e}"))
                        secondaryMuscles_translated = secondaryMuscles
                    
                    try:
                        category_translated = translator.translate(exercise.get('category', '') or 'N/A')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al traducir 'category': {e}"))
                        category_translated = exercise.get('category', 'N/A')

                    # Crear un nuevo diccionario con los valores traducidos
                    translated_exercise = {
                        'name': name_translated,
                        'description': description_translated,
                        'force': force_translated,
                        'level': level_translated,
                        'mechanic': mechanic_translated,
                        'equipment': equipment_translated,
                        'primaryMuscles': primaryMuscles_translated,
                        'secondaryMuscles': secondaryMuscles_translated,
                        'instructions': instructions_translated,
                        'category': category_translated,
                        'images': exercise.get('images'),
                        'id': exercise.get('id')
                    }

                    # Añadir el ejercicio traducido a la nueva lista
                    translated_data.append(translated_exercise)

                    # Imprimir el porcentaje de avance
                    progress_percentage = (idx / total_exercises) * 100
                    sys.stdout.write(f"\rProgreso: {progress_percentage:.2f}%")
                    sys.stdout.flush()

                # Guardar los datos traducidos en un nuevo archivo JSON
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    json.dump(translated_data, outfile, ensure_ascii=False, indent=4)
                
                self.stdout.write(self.style.SUCCESS(f'\nArchivo traducido generado en: {output_file_path}'))

        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error al cargar el archivo JSON: {e}'))
