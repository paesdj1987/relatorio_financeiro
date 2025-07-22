# menu_mapa_controle/callbacks.py 

import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table, dcc, html, no_update
import io
import dash_bootstrap_components as dbc 
import datetime
import threading

from request import control_map_query  

# ————— Configuração de cache global —————
df_global     = None
df_last_fetch = None
df_last_filters  = (None, None, None)
FETCH_TTL     = datetime.timedelta(hours=2)
fetch_lock    = threading.Lock()   

def register_callbacks_mapa(app):
    
    @app.callback(
        [
            Output("output-div", "children"),
            Output("export-div", "style"),
            Output("df-cache", "data"),
        ],
        [
            Input("consultar-button", "n_clicks"),
            Input("limpar-button", "n_clicks"),
        ],
        [
            State("input-filter-sc", "value"),
            State("input-filter-pc", "value"),
            State("input-filter-nf", "value"),
            State("input-filter-cod-obra", "value"),
            State("input-filter-insumo", "value"),
            State("input-filter-fornecedor", "value"),
            State("input-filter-ua-codigo", "value"),
            State("data-sc-start", "date"),
            State("data-sc-end",   "date"),
        ],
        prevent_initial_call=True,
    )
    def update_output(
        n_consultar, n_limpar,
        sc_filter, pc_filter, nf_filter,
        cod_obra_filter, insumo_filter,
        fornecedor_filter, ua_codigo_filter,
        data_sc_start, data_sc_end
    ):
        
        global df_global, df_last_fetch, df_last_filters
        
        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # ---------- LIMPAR ----------
        if button_id == "limpar-button":
            return "", {"display": "none"}, None

        if button_id == "consultar-button" and not cod_obra_filter:
            alerta = dbc.Alert(
                "É obrigatório o preenchimento do campo 'Pesquisar por UO...'",
                color="warning",
                duration=8000,     
                is_open=True,
                style={
                    "textAlign": "center",
                    "width": "40%",         
                    "margin": "0 auto",     
                    "marginBottom": "30px",
                    "marginTop": "0px"  
                }
            )
            return alerta, {"display": "none"}, None
        
        # ---------- PREPARA LISTA DE UOs ----------
        uo_terms = [t.strip() for t in cod_obra_filter.split(";") if t.strip()]
            
        # ---------- CONSULTAR ----------
        try:

            # — CACHE + TTL + LOCK + DETECÇÃO DE MUDANÇA DE FILTRO —
            now = datetime.datetime.now()
            with fetch_lock:
                if (
                    df_global is None
                    or df_last_fetch is None
                    or (now - df_last_fetch) > FETCH_TTL
                    or (tuple(uo_terms), data_sc_start, data_sc_end) != df_last_filters   
                ):
                    # chama o SQL passando UO + intervalo de datas
                    df_global = control_map_query(
                        uo_list = uo_terms,  
                        dt_ini=data_sc_start,
                        dt_fim=data_sc_end
                    )
                    df_last_fetch = now
                    df_last_filters = (tuple(uo_terms), data_sc_start, data_sc_end) 

            # Usa cache sem nova consulta 
            df = df_global.copy()

            # ——— Remover hora das colunas de data ———
            date_cols = [
                "Data_da_SC",
                "Data_da_SC_Chegada_a_Obra",
                "Data_Aprovacao_da_NT",
                "Data_Emissao_do_PC",
                "Previsao_de_Entrega",
                "Data_da_NF",
                "Data_Entrada_na_Obra",
                "Data_Vencimento",
            ]
            for col in date_cols:
                if col in df.columns:
                    # converte pra datetime e formata só a parte de data
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d/%m/%Y")

            # opcional: para manter filtros baseados em texto    "Data_da_SC",
            df = df.fillna("").astype(str)

            def apply_filter(df, col, terms):
                if not terms:
                    return df
                terms = [t.strip().lower() for t in terms.split(";")]
                return df[df[col].apply(lambda x: any(t in x.lower() for t in terms))]
     
            df = apply_filter(df, "Num_da_SC", sc_filter)
            df = apply_filter(df, "Num_do_PC", pc_filter)
            df = apply_filter(df, "Num_da_NF", nf_filter)
            df = apply_filter(df, "Cod_Obra", cod_obra_filter)
            df = apply_filter(df, "Descricao_do_Insumo", insumo_filter)
            df = apply_filter(df, "Fornecedor", fornecedor_filter)
            df = apply_filter(df, "UA_Codigo", ua_codigo_filter)
 
            table = html.Div(
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    columns=[{"name": c.replace("_", " "), "id": c} for c in df.columns],
                    page_size=10,
                    style_table={"overflowX": "auto", "margin": "16px"},
                    style_cell={
                        "textAlign": "center",
                        "padding": "12px",
                        "fontSize": "11px",
                        "fontFamily": "Poppins, sans-serif",
                        "border": "1px solid #ddd",
                    },
                    style_header={
                        "backgroundColor": "#2C3E50",
                        "color": "#ecf0f1",
                        "fontWeight": "bold",
                        "fontSize": "12px",
                    },
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "Descricao_do_Insumo"},
                            "textAlign": "left",
                        },
                        {
                            "if": {"column_id": "Fornecedor"},
                            "textAlign": "left",
                        }
                    ],
                    style_data_conditional=[
                        {
                            "if": {"column_id": "Descricao_do_Insumo"},
                            "whiteSpace": "normal",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        }
                    ],
                ),
                style={"marginLeft": "-20px", "marginRight": "30px"},
            )

            export_style = {
                "display": "block",
                "textAlign": "left",
                "marginBottom": "10px",
                "marginLeft": "30px",
            }

            return table, export_style, df.to_dict("records")

        except Exception as e:
            return f"Erro ao consultar Oracle: {e}", {"display": "none"}, None

    # -------------------------------------------------
    #  Exportar para Excel 
    # -------------------------------------------------
    @app.callback(
        Output("download-dataframe-xlsx", "data"),
        Input("download-excel-icon", "n_clicks"),
        State("df-cache", "data"),
        prevent_initial_call=True,
    )
    def download_excel(n_clicks, data):
        if not data:
            return no_update

        df = pd.DataFrame(data)

        # 1) Converter colunas de data para “date” (sem hora)
        date_cols = [
            "Data_da_SC",
            "Data_da_SC_Chegada_a_Obra",
            "Data_Aprovacao_da_NT",
            "Data_Emissao_do_PC",
            "Previsao_de_Entrega",
            "Data_da_NF",
            "Data_Entrada_na_Obra",
            "Data_Vencimento"
        ]
        for col in date_cols:
            if col in df.columns:
                # converte para datetime e em seguida extrai só a parte de data
                df[col] = pd.to_datetime(
                    df[col],
                    format="%d/%m/%Y",
                    errors="coerce"
                ).dt.strftime("%d/%m/%Y")

        # 2) Calcula Tempo_Atendimento em dias (pc.data_aceite − sc.data_registro)
        if "Data_da_SC" in df.columns and "Data_Emissao_do_PC" in df.columns:
            df["Tempo_Atendimento (em dias)"] = (
                pd.to_datetime(df["Data_Emissao_do_PC"], format="%d/%m/%Y", errors="coerce")
                - pd.to_datetime(df["Data_da_SC"],      format="%d/%m/%Y", errors="coerce")
            ).dt.days

        # 3) Colunas numéricas em geral
        numeric_cols = [
            "Valor_Unitario", "Qtd_Solicitada", "Valor_Total",
            "Qtd_Entregue", "Saldo",
            "Qtd_Solicitada_Anterior", "Valor_Unitario_Anterior", "Valor_Total_Anterior"
        ]
        currency_cols = [
            "Valor_Unitario", "Valor_Total",
            "Valor_Unitario_Anterior", "Valor_Total_Anterior"
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Dados", index=False, na_rep="")
            workbook  = writer.book
            worksheet = writer.sheets["Dados"]

            # formatos
            plain_fmt    = workbook.add_format({'num_format': '#,##0.00'})
            currency_fmt = workbook.add_format({'num_format': '"R$ "#,##0.00'})
            date_fmt     = workbook.add_format({'num_format': 'dd/mm/yyyy'})

            # aplica formatação coluna a coluna
            for idx, col in enumerate(df.columns):
                if col in currency_cols:
                    worksheet.set_column(idx, idx, 15, currency_fmt)
                elif col in numeric_cols:
                    worksheet.set_column(idx, idx, 12, plain_fmt)
                elif col in date_cols:
                    worksheet.set_column(idx, idx, 15, date_fmt)

        buffer.seek(0)
        return dcc.send_bytes(buffer.getvalue(), filename="dados_financeiro_obra.xlsx")


