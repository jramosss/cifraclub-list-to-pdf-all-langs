FROM mcr.microsoft.com/playwright/java:v1.50.0-noble AS build

WORKDIR /app

COPY pom.xml ./
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests

# Imagen final
FROM mcr.microsoft.com/playwright/java:v1.50.0-noble

WORKDIR /app

COPY --from=build /app/target/java-1.0-SNAPSHOT.jar app.jar

CMD ["java", "-jar", "app.jar"]