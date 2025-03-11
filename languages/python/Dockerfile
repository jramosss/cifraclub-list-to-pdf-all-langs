FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install

CMD ["python", "benchmark.py"]