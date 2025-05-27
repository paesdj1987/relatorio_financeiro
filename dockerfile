# --------------------------------------
#  Dockerfile – produção (Gunicorn)
# --------------------------------------
FROM python:3.12-slim

# 1. diretório de trabalho
WORKDIR /VW_FINANCEIRO_OBRA

# 2. cópia do projeto
COPY . .

# 3. dependências de SO (Oracle) + pip
RUN apt-get update && apt-get install -y \
        libaio1 unzip \
    && unzip instantclient-basiclite.zip -d /usr/lib/oracle/ \
    && ln -s /usr/lib/oracle/instantclient_* /usr/lib/oracle/instantclient \
    && echo "/usr/lib/oracle/instantclient" > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH="/usr/lib/oracle/instantclient:$LD_LIBRARY_PATH"

# 4. comando de execução (Gunicorn)
CMD ["gunicorn", "app:server",           \
     "--workers", "4",                   \
     "--threads", "2",                   \
     "--worker-class", "gthread",        \
     "--bind", "0.0.0.0:8052",           \
     "--timeout", "120",                 \
     "--log-level", "info"]

