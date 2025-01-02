# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza pip a la última versión
RUN pip install --upgrade pip

# Copia el archivo requirements.txt en el contenedor
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente en el contenedor
COPY ./src /app/

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
