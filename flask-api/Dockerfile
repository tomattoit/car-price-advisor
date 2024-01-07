FROM python:3.11-slim
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# CMD ["gunicorn", "--preload", "-b", "0.0.0.0:5000", "-w", "4", "backend:app"]
CMD ["python", "backend.py"]
