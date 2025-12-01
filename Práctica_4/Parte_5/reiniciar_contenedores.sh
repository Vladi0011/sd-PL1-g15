#!/bin/bash

# --- 1. DETENER CONTENEDORES ---
echo "Deteniendo nginx_tarea..."
docker stop nginx_tarea
echo "Deteniendo tarea_app_flask..."
docker stop tarea_app_flask
echo "Deteniendo mariadb_tarea_db..."
docker stop mariadb_tarea_db

# --- 2. ESPERAR Y LIMPIAR ---
echo "Esperando 10 segundos..."
sleep 10
echo "Eliminando contenedores detenidos..."
docker container prune -f
echo "Esperando 5 segundos..."
sleep 5

# --- 3. LANZAR MARIADB ---
echo "Lanzando contenedor con la BBDD..."
docker run -d --name mariadb_tarea_db --rm -v $HOME/basedatos:/var/lib/mysql   --network pruebas -e MYSQL_ROOT_PASSWORD=root_pass -e MYSQL_DATABASE=tarea_db   -e MYSQL_USER=tarea_user -e MYSQL_PASSWORD=tarea_pass mariadb:latest

echo "Esperando 5 segundos..."
sleep 5

# --- 4. LANZAR FLASK ---
echo "Lanzando contenedor con la aplicación FLASK..."
docker run -d --name tarea_app_flask --rm --network pruebas tarea_app

echo "Esperando 2 segundos..."
sleep 2

# --- 5. LANZAR NGINX ---
echo "Lanzando contenedor con el proxy NGINX..."
docker run --name nginx_tarea -d --rm --network pruebas -p 80:80   -v $(pwd)/nginx/default.conf:/etc/nginx/conf.d/default.conf nginx

# --- 6. VERIFICACIÓN ---
echo "Ejecutando docker ps..."
docker ps
