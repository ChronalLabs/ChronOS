# --- Stage 1: Build the application ---
# We use a Maven image to build the app from source code
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app

# Copy project definition and source code
COPY pom.xml .
COPY src ./src

# Run the build command (creates the 'target' folder)
RUN mvn clean package -DskipTests

# --- Stage 2: Run the application ---
# We use a lightweight Java image to run the app
FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp

# COPY the JAR file created in Stage 1 (from /app/target)
COPY --from=build /app/target/*.jar app.jar

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
