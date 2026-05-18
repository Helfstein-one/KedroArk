FROM mcr.microsoft.com/devcontainers/python:3.10

# Install OpenJDK 11 for PySpark
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Upgrade pip
RUN pip install --upgrade pip
