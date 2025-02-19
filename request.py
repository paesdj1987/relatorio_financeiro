import os
import re
import pandas as pd
from sqlalchemy import create_engine
import oracledb

def fetch_data_from_oracle():
    try:
        # Caminho do Oracle Instant Client
        instant_client_path = r"C:\app\client\joaodanilo\product\12.2.0\client_1"
        if not os.path.exists(instant_client_path):
            raise FileNotFoundError(
                f"Oracle Instant Client não encontrado: {instant_client_path}"
            )

        # Inicializar o Oracle Client no modo Thick
        oracledb.init_oracle_client(lib_dir=instant_client_path)
        print("Oracle Client inicializado com sucesso.")

        # Configurar a string de conexão
        connection_string = "oracle+oracledb://OR_CONSULTA:OR_CONSULTA@10.148.64.157:1521/PRODMZ"

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
            # SC
            "N_da_SC": "N_da_SC",

            # UO: Cd_Obra => agora "Cód_Obra"
            "Cd_Obra": "Cód_Obra",

            # Insumo
            "Cd_insumo": "Cód_insumo",
            "Descrio_do_insumo": "Descrição_do_insumo",

            # Quantidade
            "Qt_solicitada": "Qt_solicitada",
            "Quant_entregue": "Quant_entregue",
            "Saldo": "Saldo",

            # Datas
            "Data_da_SC": "Data_da_SC",
            "Data_SC_chegada_obra": "Data_SC_chegada_a_obra",
            "Data_aprovao_da_NT": "Data_aprovação_da_NT",
            "Data_emisso_do_PC": "Data_emissão_do_PC",
            "Previso_de_entrega": "Previsão_de_entrega",
            "Data_da_NF": "Data_da_NF",
            "Data_entrada_na_obra": "Data_entrada_na_obra",
            "Data_vencimento": "Data_vencimento",

            # PC e NF
            "N_do_PC": "N_do_PC",
            "N_da_NF": "N_da_NF",
            "Status_da_NF": "Status_da_NF",

            # Valor
            "Valor_Unitrio": "Valor_Unitário",

            # Fornecedor
            "Fornecedor__CNPJ": "Fornecedor__CNPJ",
            "Fornecedor": "Fornecedor",

            # UA => UA__Cdigo => agora "UA_Código"
            "UA__Cdigo": "UA_Código",
            "UA__Descrio": "UA_Descrição",
        }, inplace=True)

        # 2) Formatar colunas de data após renomear
        date_columns = [
            "Data_da_SC", 
            "Data_SC_chegada_a_obra", 
            "Data_aprovação_da_NT",
            "Data_emissão_do_PC", 
            "Previsão_de_entrega", 
            "Data_da_NF",
            "Data_entrada_na_obra", 
            "Data_vencimento"
        ]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d/%m/%Y")

        # 3) Salvar em CSV
        output_csv = "shared_data/vw_financeiro_obra.csv"
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
