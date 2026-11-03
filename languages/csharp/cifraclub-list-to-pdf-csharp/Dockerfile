FROM mcr.microsoft.com/playwright/dotnet:v1.50.0-noble

WORKDIR /app

COPY . .

RUN dotnet restore

RUN dotnet build --configuration Release --no-restore

RUN dotnet publish --configuration Release --no-build --output /app/out

CMD ["dotnet", "/app/out/cifraclub-list-to-pdf-csharp.dll"]