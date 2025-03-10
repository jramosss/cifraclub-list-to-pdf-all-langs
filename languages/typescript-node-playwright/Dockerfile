FROM mcr.microsoft.com/playwright:v1.51.0-noble

WORKDIR /app

COPY . .

RUN npm ci

CMD ["npm", "run", "build-and-run"]
