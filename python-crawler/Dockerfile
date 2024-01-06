FROM python:3.11-slim
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN ["python3", "-m", "unittest", "otomoto_crawler/tests/unittests.py"]
CMD ["scrapy", "crawl", "car-spider"]
