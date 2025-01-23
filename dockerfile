# Set base image (host OS)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /VW_FINANCEIRO_OBRA

# Copy the project files to the working directory
COPY . /VW_FINANCEIRO_OBRA

# Install dependencies
RUN apt-get update && apt-get install -y \
    libaio1 \
    unzip \
    && unzip /VW_FINANCEIRO_OBRA/instantclient-basiclite.zip -d /usr/lib/oracle/ \
    && ln -s /usr/lib/oracle/instantclient_* /usr/lib/oracle/instantclient \
    && echo "/usr/lib/oracle/instantclient" > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install oracledb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variable for Oracle Instant Client
ENV LD_LIBRARY_PATH="/usr/lib/oracle/instantclient:$LD_LIBRARY_PATH"

# Command to run on container start
CMD ["python", "./app.py"]
