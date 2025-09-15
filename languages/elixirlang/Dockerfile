FROM zenika/alpine-chrome

USER root

ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/bin/chromium-browser
ENV CHROME_ARGS="--no-sandbox --disable-dev-shm-usage --headless --disable-gpu"

RUN apk add --no-cache elixir erlang
RUN mix local.hex --force && mix local.rebar --force

WORKDIR /app
COPY mix.exs mix.lock ./
RUN mix deps.get
COPY . .
RUN mix compile

CMD ["mix", "benchmark"]
