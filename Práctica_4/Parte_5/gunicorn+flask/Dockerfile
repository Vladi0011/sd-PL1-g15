# Imagen base
FROM python:3.9

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios a la imagen
COPY ejercicio1_finalToDo.py ./
COPY contrasenyas.txt ./
COPY static /app/static

# Instalar las dependencias
RUN pip install flask
RUN pip install gunicorn
RUN pip install httpie
RUN pip install Flask-SQLAlchemy
RUN pip install flask-httpauth
RUN pip install Werkzeug
RUN pip install pymysql

# Variable de entorno SQLALCHEMY_DATABASE_URI para la BBDD
ENV SQLALCHEMY_DATABASE_URI 'mysql+pymysql://tarea_user:tarea_pass@mariadb_tarea_db/tarea_db'

# Exponer el puerto 5000 para Gunicorn
EXPOSE 5000

# Ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "ejercicio1_finalToDo:app"]
