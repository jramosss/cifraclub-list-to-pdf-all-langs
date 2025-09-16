# Use the official Playwright image with Go support
FROM mcr.microsoft.com/playwright:v1.47.0-focal

# Install Go
RUN apt-get update && apt-get install -y wget && \
    wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz && \
    rm go1.22.2.linux-amd64.tar.gz

# Set Go environment variables
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/go"
ENV GOBIN="/go/bin"

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Install playwright for Go
RUN go install github.com/playwright-community/playwright-go/cmd/playwright@latest
RUN playwright install --with-deps

# Build the application
RUN go build -o cifraclub-list-to-pdf

# Run the application
CMD ["./cifraclub-list-to-pdf"]
