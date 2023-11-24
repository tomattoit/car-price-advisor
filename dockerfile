FROM python:3
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir psycopg2-binary
CMD ["python", "postgres.py"]
