# menu_mapa_controle/callbacks.py 
# -----------------------------------------------------------------------------
# • Cache compartilhado em SQLite (load_df / save_df / refresh_async)
# • TTL de 2 h (stale-while-revalidate)
# • DataTable virtualizada
# -----------------------------------------------------------------------------

import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table, dcc, html, no_update
import io
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

from cache_sqlite import load_df, save_df, refresh_async
from request import control_map_query  # consulta Oracle

# TTL do cache
TTL = timedelta(hours=2)

# -----------------------------------------------------------------------------
# Função para registrar todos os callbacks do módulo
# -----------------------------------------------------------------------------
def register_callbacks_mapa(app):

    # -----------------------------------------------------------------------------
    # Callback principal — consulta, filtros e exibição da tabela
    # -----------------------------------------------------------------------------
    @app.callback(
        [
            Output("output-div", "children"),   # DataTable ou alerta
            Output("export-div", "style"),      # exibir/ocultar botão exportar
            Output("df-cache", "data"),         # cache para download
        ],
        [
            Input("consultar-button", "n_clicks"),
            Input("limpar-button",    "n_clicks"),
        ],
        [
            State("input-filter-sc",         "value"),
            State("input-filter-pc",         "value"),
            State("input-filter-nf",         "value"),
            State("input-filter-cod-obra",   "value"),
            State("input-filter-insumo",     "value"),
            State("input-filter-fornecedor", "value"),
            State("input-filter-ua-codigo",  "value"),
            State("data-sc-start",           "date"),
            State("data-sc-end",             "date"),
        ],
        prevent_initial_call=True,
    )
    def update_output(
        n_consultar, n_limpar,
        sc_filter, pc_filter, nf_filter,
        cod_obra_filter, insumo_filter,
        fornecedor_filter, ua_codigo_filter,
        data_sc_start, data_sc_end,
    ):
        """Retorna DataTable filtrada ou alerta."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # ---------- LIMPAR ----------
        if button_id == "limpar-button":
            return "", {"display": "none"}, None

        # ---------- Validação ----------
        if button_id == "consultar-button" and not cod_obra_filter:
            alerta = dbc.Alert(
                "É obrigatório o preenchimento do campo 'Pesquisar por UO...'.",
                color="warning", duration=8000, is_open=True,
                style={
                    "textAlign": "center", "width": "40%",
                    "margin": "0 auto", "marginBottom": "30px",
                },
            )
            return alerta, {"display": "none"}, None

        # ---------- Lista de UOs ----------
        uo_terms = [t.strip() for t in cod_obra_filter.split(";") if t.strip()]

        # ---------- Cache em SQLite ----------
        now      = datetime.now()
        df_cache = load_df(uo_terms, data_sc_start, data_sc_end)

        if df_cache.empty:
            # 1ª vez ou filtros diferentes → consulta Oracle bloqueante
            df_cache = control_map_query(
                uo_list=uo_terms, dt_ini=data_sc_start, dt_fim=data_sc_end
            )
            df_cache["fetched_at"] = now.isoformat()
            save_df(df_cache)
            last_fetch = now
        else:
            last_fetch = pd.to_datetime(df_cache["fetched_at"].iloc[0])
            if now - last_fetch > TTL:
                # serve cache antigo e atualiza em segundo plano
                refresh_async(uo_terms, data_sc_start, data_sc_end, control_map_query)

        # Remove timestamp antes de qualquer filtro / exibição
        df = df_cache.drop(columns=["fetched_at"]).copy()

        # ---------- Formatação de datas ----------
        date_cols = [
            "Data_da_SC", "Data_da_SC_Chegada_a_Obra", "Data_Aprovacao_da_NT",
            "Data_Emissao_do_PC", "Previsao_de_Entrega", "Data_da_NF",
            "Data_Entrada_na_Obra", "Data_Vencimento",
        ]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")\
                              .dt.strftime("%d/%m/%Y")

        # Mantém tudo como string para facilitar filtros de substring
        df = df.fillna("").astype(str)

        # ---------- Filtros digitados ----------
        def apply_filter(df_, col, terms):
            if not terms:
                return df_
            terms = [t.strip().lower() for t in terms.split(";")]
            return df_[df_[col].apply(lambda x: any(t in x.lower() for t in terms))]

        df = apply_filter(df, "Num_da_SC",               sc_filter)
        df = apply_filter(df, "Num_do_PC",               pc_filter)
        df = apply_filter(df, "Num_da_NF",               nf_filter)
        df = apply_filter(df, "Cod_Obra",                cod_obra_filter)
        df = apply_filter(df, "Descricao_do_Insumo",     insumo_filter)
        df = apply_filter(df, "Fornecedor",              fornecedor_filter)
        df = apply_filter(df, "UA_Codigo",               ua_codigo_filter)

        # ---------- Sem resultados ----------
        if df.empty:
            alerta = dbc.Alert(
                "Nenhum resultado encontrado para os filtros informados.",
                color="warning", duration=8000, is_open=True,
                style={
                    "textAlign": "center", "width": "50%",
                    "margin": "0 auto", "marginBottom": "30px",
                },
            )
            return alerta, {"display": "none"}, None

        # ---------- DataTable ----------
        table = html.Div(
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": c.replace("_", " "), "id": c} for c in df.columns],
                page_size=10,
                virtualization=True,
                style_table={"overflowX": "auto", "margin": "16px"},
                style_cell={
                    "textAlign": "center", "padding": "12px",
                    "fontSize": "11px", "fontFamily": "Poppins, sans-serif",
                    "border": "1px solid #ddd",
                },
                style_header={
                    "backgroundColor": "#2C3E50", "color": "#ecf0f1",
                    "fontWeight": "bold", "fontSize": "12px",
                },
                style_cell_conditional=[
                    {"if": {"column_id": "Descricao_do_Insumo"}, "textAlign": "left"},
                    {"if": {"column_id": "Fornecedor"}         , "textAlign": "left"},
                ],
                style_data_conditional=[
                    {
                        "if": {"column_id": "Descricao_do_Insumo"},
                        "whiteSpace": "normal", "overflow": "hidden",
                        "textOverflow": "ellipsis",
                    }
                ],
            ),
            style={"marginLeft": "-20px", "marginRight": "30px"},
        )
        export_style = {
            "display": "block", "textAlign": "left",
            "marginBottom": "10px", "marginLeft": "30px",
        }
        return table, export_style, df.to_dict("records")

# -------------------------------------------------------------------------
# Callback de exportação para Excel
# -------------------------------------------------------------------------
    @app.callback(
        Output("download-dataframe-xlsx", "data"),
        Input("download-excel-icon", "n_clicks"),
        State("df-cache", "data"),
        prevent_initial_call=True,
    )
    def download_excel(n_clicks, rows):
        if not rows:
            return no_update

        # 1) Reconstrói o DataFrame
        df = pd.DataFrame(rows)

        # 2) Calcula Tempo_Atendimento em dias
        if "Data_da_SC" in df.columns and "Data_Emissao_do_PC" in df.columns:
            df["Tempo_Atendimento (em dias)"] = (
                pd.to_datetime(df["Data_Emissao_do_PC"], format="%d/%m/%Y", errors="coerce")
                - pd.to_datetime(df["Data_da_SC"],      format="%d/%m/%Y", errors="coerce")
            ).dt.days

        # 3) Ajusta colunas de data e numéricas
        date_cols = [
            "Data_da_SC", "Data_da_SC_Chegada_a_Obra", "Data_Aprovacao_da_NT",
            "Data_Emissao_do_PC", "Previsao_de_Entrega", "Data_da_NF",
            "Data_Entrada_na_Obra", "Data_Vencimento",
        ]
        # inclui Tempo_Atendimento na formatação numérica
        numeric_cols = [
            "Valor_Unitario", "Qtd_Solicitada", "Valor_Total", "Qtd_Entregue", "Saldo",
            "Qtd_Solicitada_Anterior", "Valor_Unitario_Anterior", "Valor_Total_Anterior",
            "Tempo_Atendimento (em dias)",
        ]
        currency_cols = [
            "Valor_Unitario", "Valor_Total",
            "Valor_Unitario_Anterior", "Valor_Total_Anterior",
        ]

        # Converte de volta para tipo adequado
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")\
                            .dt.strftime("%d/%m/%Y")
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 4) Gera o XLSX
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter", datetime_format="dd/mm/yyyy") as writer:
            df.to_excel(writer, sheet_name="Dados", index=False, na_rep="")
            workbook  = writer.book
            worksheet = writer.sheets["Dados"]

            # formata colunas
            currency_fmt = workbook.add_format({"num_format": '"R$ "#,##0.00'})
            plain_fmt    = workbook.add_format({"num_format": "#,##0.00"})
            date_fmt     = workbook.add_format({"num_format": "dd/mm/yyyy"})

            for idx, col in enumerate(df.columns):
                if col in currency_cols:
                    worksheet.set_column(idx, idx, 15, currency_fmt)
                elif col in numeric_cols:
                    worksheet.set_column(idx, idx, 12, plain_fmt)
                elif col in date_cols:
                    worksheet.set_column(idx, idx, 15, date_fmt)

        buffer.seek(0)
        return dcc.send_bytes(buffer.getvalue(), filename="dados_financeiro_obra.xlsx")
        