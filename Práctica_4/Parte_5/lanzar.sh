#!/bin/bash
# Script para lanzar la infraestructura Docker de la aplicación To-Do

# 1. Parar y eliminar contenedores preexistentes con el mismo nombre
echo "Deteniendo y eliminando contenedores antiguos..."
docker stop mariadb_tarea_db tarea_app_flask nginx_tarea &> /dev/null
docker rm mariadb_tarea_db tarea_app_flask nginx_tarea &> /dev/null

# 2. Reconstruir la imagen de la aplicación (solo si hay cambios)
echo "Reconstruyendo imagen de la aplicación..."
docker build -t tarea_app .

# 3. Lanzar MariaDB (Base de Datos)
echo "Lanzando MariaDB (DB)..."
docker run -d --name mariadb_tarea_db --rm \
  -v $HOME/basedatos:/var/lib/mysql \
  --network pruebas \
  -e MYSQL_ROOT_PASSWORD=root_pass \
  -e MYSQL_DATABASE=tarea_db \
  -e MYSQL_USER=tarea_user \
  -e MYSQL_PASSWORD=tarea_pass \
  mariadb:latest

# Esperar un tiempo para que la base de datos se inicie
echo "Esperando 10 segundos a que la DB se inicie..."
sleep 10

# 4. Lanzar la Aplicación Flask/Gunicorn (SIN mapeo de puerto)
echo "Lanzando contenedor de la aplicación Flask/Gunicorn..."
docker run -d --name tarea_app_flask --rm --network pruebas tarea_app

# 5. Lanzar el Proxy Inverso Nginx
echo "Lanzando contenedor con el proxy NGINX..."
docker run -d --name nginx_tarea --rm --network pruebas -p 80:80 \
  -v $(pwd)/nginx/default.conf:/etc/nginx/conf.d/default.conf \
  nginx

# 6. Mostrar el estado final
echo "Infraestructura iniciada. Contenedores activos:"
docker ps
echo "Puedes acceder a la aplicación en http://<TU_IP>/"
