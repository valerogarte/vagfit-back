
# Proyecto Django con Docker

Este proyecto es una aplicación Django desplegada con Docker. A continuación, se detalla el proceso de instalación, configuración y comandos útiles para gestionar el proyecto.

## Requisitos previos

- Docker y Docker Compose instalados en tu sistema.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
2. Construye los contenedores de Docker:
   ```bash
   docker-compose build
   ```

## Montar el proyecto

Ejecuta los siguientes comandos para configurar la base de datos y crear un usuario administrador:

```bash
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```
## Configurar certificado

1. Introduce los certificados en esta carpeta: /nginx/certs
2. Si es de un NAS ve a Seguridad > Certificado >  tu-dominio.synology.me
- `chain.pem` -> Se usa para generar el fullchain.pem
- `cert.pem` -> Se usa para generar el fullchain.pem
- `privkey.pem` -> Clave privada
- `fullchain.pem` -> Deberás crearlo desde este comando `cat cert.pem <(echo "") chain.pem > fullchain.pem`


## Importar ejercicios

Para importar un conjunto de ejercicios en español al proyecto:

1. Clona el repositorio de ejercicios:
   ```bash
   git clone https://github.com/yuhonas/free-exercise-db
   ```
2. Configura el volumen en `docker-compose.yml` para añadir la carpeta del proyecto de ejercicios:
   ```yaml
   volumes:
      # Solo para importar
      - ../free-exercise-db:/free-exercise-db
   ```
3. Genera el JSON traducido al español:
   ```bash
   docker-compose run web python manage.py traducir-json
   ```
4.1. Importa el JSON generado:
   ```bash
   docker-compose run web python manage.py import-json
   ```
4.2. OLD - Importa el JSON desde el repositorio
   ```bash
   docker-compose run web python manage.py import-json ./exercises_translated.json
   ```
## Comandos interesantes

Comandos adicionales para gestionar la aplicación y la base de datos:

- Revertir migraciones en la app `ejercicios`:
  ```bash
  docker-compose run web python manage.py migrate ejercicios zero
  ```
- Crear migraciones para las apps `ejercicios`, `rutinas` y `entrenamiento`:
  ```bash
  docker-compose run web python manage.py makemigrations ejercicios
  docker-compose run web python manage.py makemigrations rutinas
  docker-compose run web python manage.py makemigrations entrenamiento
  ```
- Aplicar todas las migraciones pendientes:
  ```bash
  docker-compose run web python manage.py migrate
  ```
- Limpiar caché:
  ```bash
  docker-compose run web python manage.py clearcache
  ```
- Limpiar toda la base de datos (cuidado, elimina todos los datos):
  ```bash
  docker-compose run web python manage.py flush
  ```

## Arrancar el proyecto

Para iniciar el servidor Django en el entorno de Docker, ejecuta:

```bash
python manage.py runserver 0.0.0.0:8000
```

Accede a la aplicación en [http://localhost:8000](http://localhost:8000).

## Contribución

Si deseas contribuir al proyecto, realiza un fork, crea una rama con tus cambios y abre un pull request.

---0xFFE0E0E0

¡Gracias por utilizar este proyecto!
