FROM python:3.12

WORKDIR /app

COPY servidor_proc.py .

RUN pip install redis

CMD ["python", "-u", "servidor_proc.py"]
