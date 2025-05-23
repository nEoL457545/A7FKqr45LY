# Step 1: Use an official OpenJDK base image
FROM openjdk:17-jdk-slim AS build

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the Maven build file into the container (pom.xml) and download dependencies
COPY pom.xml /app/
RUN ./mvnw dependency:go-offline

# Step 4: Copy the rest of the application code into the container
COPY src /app/

# Step 5: Build the application using Maven
RUN ./mvnw clean package -DskipTests

# Step 6: Create the runtime image by using a smaller image (only JRE required)
FROM openjdk:17-jre-slim

# Step 7: Set the working directory for the runtime image
WORKDIR /app

# Step 8: Copy the JAR file from the build stage into the runtime image
COPY --from=build /app/target/ecom-microservices-0.0.1-SNAPSHOT.jar /app/ecom-microservices.jar

# Step 9: Expose the port that the application will run on
EXPOSE 8080

# Step 10: Define the entry point to run the Spring Boot application
ENTRYPOINT ["java", "-jar", "ecom-microservices.jar"]

# Step 11: Optionally, set environment variables (e.g., for database connection, etc.)
ENV SPRING_PROFILES_ACTIVE=prod
ENV DB_URL=jdbc:mysql://mysql-service:3306/ecommerce_db
ENV DB_USERNAME=ecommerce_user
ENV DB_PASSWORD=ecommerce_password
# Step 12: Add health check to ensure the application is running correctly
