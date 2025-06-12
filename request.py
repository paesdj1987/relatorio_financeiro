#request.py
import os
import re
import pandas as pd
from sqlalchemy import create_engine
import oracledb
from dotenv import load_dotenv
load_dotenv()  


def fetch_data_from_oracle():
    try:
        # Caminho do Oracle Instant Client
        instant_client_path = os.getenv('ORACLE_INSTANT_CLIENT_PATH')
        if not os.path.exists(instant_client_path):
            raise FileNotFoundError(
                f"Oracle Instant Client não encontrado: {instant_client_path}"
            )

        # Inicializar o Oracle Client no modo Thick
        oracledb.init_oracle_client(lib_dir=instant_client_path)
        print("Oracle Client inicializado com sucesso.")

        # Configurar a string de conexão
        connection_string = f"oracle+oracledb://{os.getenv('ORACLE_USER')}:{os.getenv('ORACLE_PASSWORD')}@{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"

        # Criar o engine do SQLAlchemy
        print("Conectando ao banco de dados Oracle...")
        engine = create_engine(connection_string)

        # Executar a consulta na view
        query = 'SELECT * FROM OR_PGI."vw_financeiro_obra"'
        print(f"Executando consulta SQL: {query}")
        df = pd.read_sql(query, con=engine)
        print(f"Consulta executada com sucesso. {len(df)} registros recuperados.")

        # Normalizar nomes das colunas 
        def normalize_column_name(col_name):
            col_name = col_name.strip()
            col_name = re.sub(r"[^\w\s]", "", col_name)
            col_name = col_name.replace(" ", "_")
            return col_name

        df.columns = [normalize_column_name(col) for col in df.columns]

        # 1) Ajuste manual dos nomes para manter consistência com callbacks
        df.rename(columns={
            "Num_da_SC": "Num_da_SC",
            "Cod_Obra": "Cod_Obra",
            "Cod_Insumo": "Cod_Insumo",
            "Descricao_do_Insumo": "Descricao_do_Insumo",
            "Data_da_SC": "Data_da_SC",
            "Data_da_SC_Chegada_a_Obra": "Data_da_SC_Chegada_a_Obra",
            "Num_do_PC": "Num_do_PC",
            "Data_Aprovacao_da_NT": "Data_Aprovacao_da_NT",
            "Data_Emissao_do_PC": "Data_Emissao_do_PC",
            "Previsao_de_Entrega": "Previsao_de_Entrega",
            "Data_da_NF": "Data_da_NF",
            "Num_da_NF": "Num_da_NF",
            "Data_Entrada_na_Obra": "Data_Entrada_na_Obra",
            "Data_Vencimento": "Data_Vencimento",
            "Status_da_NF": "Status_da_NF",
            "Fornecedor_CNPJ": "Fornecedor_CNPJ",
            "Fornecedor": "Fornecedor",
            "UA_Codigo": "UA_Codigo",
            "UA_Descricao": "UA_Descricao",
            "Valor_Unitario": "Valor_Unitario",
            "Qtd_Solicitada": "Qtd_Solicitada",
            "Valor_Total": "Valor_Total",
            "Qtd_Entregue": "Qtd_Entregue",
            "Saldo": "Saldo",
            "Qtd_Solicitada_Anterior": "Qtd_Solicitada_Anterior",
            "Valor_Unitario_Anterior": "Valor_Unitario_Anterior",
            "Valor_Total_Anterior": "Valor_Total_Anterior"
        }, inplace=True)

        # 2) Formatar colunas de data após renomear
        date_columns = [
            "Data_da_SC", 
            "Data_da_SC_Chegada_a_Obra", 
            "Data_Aprovacao_da_NT",
            "Data_Emissao_do_PC", 
            "Previsão_de_entrega", 
            "Data_da_NF",
            "Data_Entrada_na_Obra", 
            "Data_Vencimento"
        ]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d/%m/%Y")

        # 3) Salvar em CSV
        output_csv = "/shared_data/vw_financeiro_obra.csv"
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)

        df.to_csv(output_csv, index=False, encoding="utf-8", sep=";")
        print(f"Arquivo CSV '{output_csv}' gerado com sucesso.")

    except oracledb.DatabaseError as e:
        print(f"Erro ao se conectar ao Oracle: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Erro ao obter dados do Oracle: {e}")

if __name__ == "__main__":
    fetch_data_from_oracle()
