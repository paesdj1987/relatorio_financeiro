# cache_sqlite.py
import sqlite3
import pathlib
import threading
import datetime as dt
import pandas as pd

DB_PATH = pathlib.Path("cache.db")
TABLE   = "mapa_controle"

def init():
    """Configura o banco em modo WAL para leituras concorrentes."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.commit()
    conn.close()

def load_df(uo_list, dt_ini, dt_fim):
    """Tenta carregar do SQLite; se tabela não existir, retorna df vazio."""
    conn = sqlite3.connect(DB_PATH)
    placeholders = ", ".join("?"*len(uo_list)) or "NULL"
    sql = f"""
        SELECT * FROM {TABLE}
        WHERE Cod_Obra IN ({placeholders})
          AND (? IS NULL OR Data_da_SC >= ?)
          AND (? IS NULL OR Data_da_SC <= ?)
    """
    params = [*uo_list, dt_ini, dt_ini, dt_fim, dt_fim]
    try:
        df = pd.read_sql(sql, conn, params=params)
    except Exception as e:
        # Se a tabela ainda não existe, retorna DataFrame vazio com colunas mínimas
        df = pd.DataFrame()
    finally:
        conn.close()
    return df


def save_df(df):
    conn = sqlite3.connect(DB_PATH)
    df_ts = df.copy()
    df_ts["fetched_at"] = dt.datetime.now().isoformat()
    df_ts.to_sql(TABLE, conn, if_exists="replace", index=False)
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_obra_data ON {TABLE}(Cod_Obra, Data_da_SC)")
    conn.commit()
    conn.close()

def refresh_async(uo_list, dt_ini, dt_fim, sql_func):
    def _job():
        df_new = sql_func(uo_list, dt_ini, dt_fim)
        save_df(df_new)
    threading.Thread(target=_job, daemon=True).start()

# roda init() ao importar o módulo
init()
