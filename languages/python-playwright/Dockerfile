FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

WORKDIR /app

COPY . .
# install uv
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install

CMD ["pytest", "-s", "-q", "--no-header", "--no-summary", "--disable-warnings", "."]