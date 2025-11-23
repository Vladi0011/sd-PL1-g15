#!/bin/bash

# --- 1. DETENER CONTENEDORES ---
echo "Deteniendo nginx_tarea..."
docker stop nginx_tarea

echo "Deteniendo tarea_app_flask..."
docker stop tarea_app_flask

echo "Deteniendo mariadb_tarea_db..."
docker stop mariadb_tarea_db

# --- 2. ESPERAR Y LIMPIAR ---
# Esperar unos segundos para asegurarnos de que los contenedores se detengan correctamente
echo "Esperando 10 segundos..."
sleep 10

# Eliminar los contenedores detenidos
echo "Eliminando contenedores detenidos..."
docker container prune -f

# Esperar 5 segundos para asegurarnos de que los contenedores eliminados se liberen correctamente
echo "Esperando 5 segundos..."
sleep 5

# --- 3. LANZAR MARIADB (BASE DE DATOS) ---
# Se usa el comando visto en la Parte 2
echo "Lanzando contenedor con la BBDD..."
docker run -d --name mariadb_tarea_db --rm -v $HOME/basedatos:/var/lib/mysql \
  --network pruebas -e MYSQL_ROOT_PASSWORD=root_pass -e MYSQL_DATABASE=tarea_db \
  -e MYSQL_USER=tarea_user -e MYSQL_PASSWORD=tarea_pass mariadb:latest

# Esperar 5 segundos para asegurarnos de que la base de datos esté en funcionamiento antes de lanzar la aplicación Flask
echo "Esperando 5 segundos..."
sleep 5

# --- 4. LANZAR FLASK (APLICACIÓN) ---
# Se usa el comando de la Parte 3, pero SIN mapear el puerto (-p) como indicaba la Parte 4
echo "Lanzando contenedor con la aplicación FLASK..."
docker run -d --name tarea_app_flask --rm --network pruebas tarea_app

# Esperar 2 segundos para lanzar el último contenedor (nginx)
echo "Esperando 2 segundos..."
sleep 2

# --- 5. LANZAR NGINX (SERVIDOR WEB / PROXY) ---
# Se usa el comando visto en la Parte 4
echo "Lanzando contenedor con el proxy NGINX..."
docker run --name nginx_tarea -d --rm --network pruebas -p 80:80 \
  -v $(pwd)/nginx/default.conf:/etc/nginx/conf.d/default.conf nginx

# --- 6. VERIFICACIÓN ---
echo "Ejecutando docker ps..."
docker ps