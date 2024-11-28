# request.py
import pandas as pd
from sqlalchemy import create_engine
import re

def fetch_data_from_oracle():
    # Configure a conexão com o banco de dados Oracle usando SQLAlchemy
    engine = create_engine('oracle+cx_oracle://OR_CONSULTA:OR_CONSULTA@10.148.64.157:1521/PRODMZ')

    try:
        # Execute a consulta na view vw_financeiro_obra
        query = 'SELECT * FROM OR_PGI."vw_financeiro_obra"'
        df = pd.read_sql(query, con=engine)

        # Função para normalizar os nomes das colunas
        def normalize_column_name(col_name):
            col_name = col_name.strip()
            col_name = re.sub(r'[^\w\s]', '', col_name)  # Remove caracteres não alfanuméricos
            col_name = col_name.replace(' ', '_')
            return col_name

        # Aplicar normalização aos nomes das colunas
        df.columns = [normalize_column_name(col) for col in df.columns]

        # Converter colunas LOB para strings, se necessário
        for col in df.columns:
            if df[col].dtype == object and len(df[col]) > 0 and isinstance(df[col].iloc[0], bytes):
                df[col] = df[col].astype(str)

        # Formatar colunas de data, se necessário
        date_columns = [
            "Data_da_SC", "Data_SC_chegada_a_obra", "Data_aprovacao_da_NT",
            "Data_emissao_do_PC", "Previsao_de_entrega", "Data_da_NF",
            "Data_entrada_na_obra", "Data_vencimento"
        ]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]).dt.strftime('%d/%m/%Y')

        # Salvar o DataFrame em um arquivo CSV, sobrescrevendo o existente, com ";" como delimitador
        df.to_csv('vw_financeiro_obra.csv', index=False, encoding='utf-8', sep=';')

    except Exception as e:
        print(f"Erro ao obter dados do Oracle: {e}")

    finally:
        # Certifique-se de fechar o engine
        engine.dispose()

if __name__ == "__main__":
    fetch_data_from_oracle()
