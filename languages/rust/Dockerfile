FROM rust:latest AS builder

# Instalar dependencias necesarias para construir el proyecto
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Compilar el proyecto en modo release
RUN cargo build --release

# Imagen final
FROM debian:bullseye-slim

# Instalar wkhtmltopdf y dependencias
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Copiar el binario compilado desde la imagen de compilación
COPY --from=builder /app/target/release/build /usr/local/bin/build

# Definir el comando de entrada
CMD ["/usr/local/bin/build"]