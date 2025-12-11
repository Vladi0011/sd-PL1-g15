# Imagen base
FROM python:3.12

# Crear carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar la API y archivos necesarios
COPY api_flask.py .
COPY c.txt .
COPY static ./static

# Instalar dependencias
RUN pip install flask
RUN pip install redis
RUN pip install gunicorn
RUN pip install flask-httpauth
RUN pip install Werkzeug

# Exponer el puerto donde escuchará Gunicorn
EXPOSE 5000

# Ejecutar la aplicación usando Gunicorn con 4 workers
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "api_flask:app"]
