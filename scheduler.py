# scheduler.py

import time
from datetime import datetime
from request import control_map_query
from cache_sqlite import save_df

INTERVAL = 2 * 3600  # 2 horas em segundos

def refresh_job():
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Iniciando refresh de cache…")
    # Sem filtros: pega tudo
    df = control_map_query()  
    save_df(df)
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Cache atualizado: {len(df)} linhas.")

if __name__ == "__main__":
    # Loop infinito
    while True:
        try:
            refresh_job()
        except Exception as e:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Erro no scheduler:", e)
        time.sleep(INTERVAL)
