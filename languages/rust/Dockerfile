FROM zenika/alpine-chrome

USER root

RUN apk add --no-cache \
    pkgconfig \
    openssl-dev \
    cargo

WORKDIR /app
COPY . .

RUN cargo build --release

CMD ["./target/release/rust"]