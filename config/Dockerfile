# Use the base image
FROM bitnami/spark:latest

# Switch to root user for installation
USER root

# Expose ports
EXPOSE 8888 8080

# Install dependencies
RUN pip install jupyter

# Install system dependencies (libaio1, curl, and unzip)
RUN apt-get update && \
    apt-get install -y libaio1 curl unzip gcc && \
    apt-get clean

# Copy the pre-downloaded Oracle Instant Client ZIP file
COPY oracle/instantclient-basic-linux.x64-23.7.0.25.01.zip /oracle/instantclient-basic-linux.x64-23.7.0.25.01.zip
#env files 
ENV LD_LIBRARY_PATH=/oracle/instantclient_23_7:$LD_LIBRARY_PATH
ENV ORACLE_HOME=/oracle/instantclient_23_7


# Install Oracle Instant Client
RUN mkdir -p /oracle && \
    cd /oracle && \
    unzip instantclient-basic-linux.x64-23.7.0.25.01.zip && \
    rm -f instantclient-basic-linux.x64-23.7.0.25.01.zip

# Install cx_Oracle
RUN pip install cx_Oracle tenacity

# Switch back to the default user
USER 1001