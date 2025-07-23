# ─────────── Imagem base + libs necessárias ───────────
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
      libaio1 unzip gcc build-essential \
      libldap2-dev libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*

# ─── Instala Instant Client (ZIP presente no contexto) ───
WORKDIR /tmp
COPY instantclient-basiclite.zip .
RUN unzip instantclient-basiclite.zip -d /usr/lib/oracle \
 && ln -s /usr/lib/oracle/instantclient_* /usr/lib/oracle/instantclient \
 && echo "/usr/lib/oracle/instantclient" \
      > /etc/ld.so.conf.d/oracle-instantclient.conf \
 && ldconfig \
 && rm instantclient-basiclite.zip

ENV ORACLE_INSTANT_CLIENT_PATH=/usr/lib/oracle/instantclient \
    LD_LIBRARY_PATH=/usr/lib/oracle/instantclient

# ─── Código da aplicação ───────────────────────────────
WORKDIR /relatorio_financeiro
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ─── Porta e comando de entrada ─────────────────────────
EXPOSE 8052
CMD ["gunicorn","app:server","--workers","4","--threads","2","--worker-class","gthread","--bind","0.0.0.0:8052","--timeout","120","--log-level","info"]
