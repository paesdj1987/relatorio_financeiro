# 1) Imagem-base leve com Python 3.12
FROM python:3.12-slim

# 2) Define o diretório de trabalho dentro do container
WORKDIR /relatorio_financeiro

# 3) Instala e configura o Oracle Instant Client
COPY instantclient-basiclite.zip /usr/lib/oracle/
RUN apt-get update \
 && apt-get install -y libaio1 unzip \
 && unzip /usr/lib/oracle/instantclient-basiclite.zip -d /usr/lib/oracle/ \
 && ln -s /usr/lib/oracle/instantclient_* /usr/lib/oracle/instantclient \
 && echo "/usr/lib/oracle/instantclient" > /etc/ld.so.conf.d/oracle-instantclient.conf \
 && ldconfig \
 && rm /usr/lib/oracle/instantclient-basiclite.zip

# 4) Instala dependências Python
COPY requirements.txt /relatorio_financeiro/
RUN pip install --no-cache-dir -r /relatorio_financeiro/requirements.txt

# 5) Copia o código da aplicação
COPY . /relatorio_financeiro

# 6) Garante que o loader do sistema encontre o Instant Client
ENV LD_LIBRARY_PATH="/usr/lib/oracle/instantclient:$LD_LIBRARY_PATH"

# 7) Comando de entrada: Gunicorn em modo production
CMD ["gunicorn", "app:server", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "gthread", \
     "--bind", "0.0.0.0:8052", \
     "--timeout", "120", \
     "--log-level", "info"]
