# request.py
import pandas as pd
from sqlalchemy import create_engine
import oracledb
import re
import os

def fetch_data_from_oracle():
    try:
        # Inicializar o Oracle Client no modo Thick
        instant_client_path = "/usr/lib/oracle/instantclient"  # Caminho do client 
        if not os.path.exists(instant_client_path):
            raise FileNotFoundError(f"Oracle Instant Client não encontrado no caminho especificado: {instant_client_path}")

        oracledb.init_oracle_client(lib_dir=instant_client_path)
        print("Oracle Client inicializado com sucesso.")

        # Configurar a string de conexão
        connection_string = (
            "oracle+oracledb://OR_CONSULTA:OR_CONSULTA@10.148.64.157:1521/PRODMZ"
        )

        # Criar o engine do SQLAlchemy
        print("Conectando ao banco de dados Oracle...")
        engine = create_engine(connection_string)

        # Executar a consulta na view vw_financeiro_obra
        query = 'SELECT * FROM OR_PGI."vw_financeiro_obra"'
        print(f"Executando consulta SQL: {query}")
        df = pd.read_sql(query, con=engine)
        print(f"Consulta executada com sucesso. {len(df)} registros recuperados.")

        # Função para normalizar os nomes das colunas
        def normalize_column_name(col_name):
            col_name = col_name.strip()
            col_name = re.sub(r'[^\w\s]', '', col_name)  
            col_name = col_name.replace(' ', '_')
            return col_name

        # Aplicar normalização aos nomes das colunas
        df.columns = [normalize_column_name(col) for col in df.columns]

        # Formatar colunas de data, se necessário
        date_columns = [
            "Data_da_SC", "Data_SC_chegada_a_obra", "Data_aprovacao_da_NT",
            "Data_emissao_do_PC", "Previsao_de_entrega", "Data_da_NF",
            "Data_entrada_na_obra", "Data_vencimento"
        ]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')

        # Salvar o DataFrame em um arquivo CSV
        output_csv = '/shared_data/vw_financeiro_obra.csv'
        df.to_csv(output_csv, index=False, encoding='utf-8', sep=';')
        print(f"Arquivo CSV '{output_csv}' gerado com sucesso.")

    except oracledb.DatabaseError as e:
        print(f"Erro ao se conectar ao Oracle: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Erro ao obter dados do Oracle: {e}")

if __name__ == "__main__":
    fetch_data_from_oracle()
