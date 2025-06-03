# menu_mapa_controle/callbacks.py
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table, dcc, html, no_update
import io

def register_callbacks_mapa(app):
    global df_global
    df_global = None

    @app.callback(
        [
            Output("output-div", "children"),
            Output("export-div", "style"),
            Output("df-cache", "data"),  
        ],
        [
            Input("consultar-button", "n_clicks"),
            Input("limpar-button", "n_clicks")
        ],
        [
            State("input-filter-sc", "value"),
            State("input-filter-pc", "value"),
            State("input-filter-nf", "value"),
            State("input-filter-cod-obra", "value"),        
            State("input-filter-insumo", "value"),          
            State("input-filter-fornecedor", "value"),
            State("input-filter-ua-codigo", "value"),       
        ],
        prevent_initial_call=True
    )
    def update_output(n_consultar, n_limpar,
                      sc_filter, pc_filter, nf_filter,
                      cod_obra_filter, insumo_filter,
                      fornecedor_filter, ua_codigo_filter):

        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # ---------- LIMPAR ----------
        if button_id == "limpar-button":
            return "", {"display": "none"}, None

        # ---------- CONSULTAR ----------
        try:
            df = pd.read_csv(
                "shared_data/vw_financeiro_obra.csv",
                sep=";", encoding="utf-8", dtype=str, engine="python"
            ).fillna("").astype(str)

            # filtros ────────────────────────
            def apply_filter(df, col, terms):
                if not terms:
                    return df
                terms = [t.strip().lower() for t in terms.split(";")]
                return df[df[col].apply(lambda x: any(t in x.lower() for t in terms))]

            df = apply_filter(df, "Num_da_SC",        sc_filter)
            df = apply_filter(df, "Num_do_PC",        pc_filter)
            df = apply_filter(df, "Num_da_NF",        nf_filter)
            df = apply_filter(df, "Cod_Obra",         cod_obra_filter)
            df = apply_filter(df, "Descricao_do_insumo", insumo_filter)
            df = apply_filter(df, "Fornecedor",       fornecedor_filter)
            df = apply_filter(df, "UA_Codigo",        ua_codigo_filter)

            # monta componente ou msg “vazio”
            if df.empty:
                return html.Div("Nenhum resultado encontrado."), {"display": "none"}, None

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
                ),
                style={"marginLeft": "-20px", "marginRight": "30px"},
            )
            export_style = {
                "display": "block",
                "textAlign": "left",
                "marginBottom": "10px",
                "marginLeft": "30px",
            }

            # serializa df para o Store (list-of-dicts)
            return table, export_style, df.to_dict("records")

        except Exception as e:
            return f"Erro ao ler CSV: {e}", {"display": "none"}, None

    # ───────────────────────────────────────────────────────────────
    # 2) Callback download Excel — lê dados do Store
    # ───────────────────────────────────────────────────────────────
    @app.callback(
        Output("download-dataframe-xlsx", "data"),
        Input("download-excel-icon", "n_clicks"),
        State("df-cache", "data"),
        prevent_initial_call=True,
    )
    def download_excel(n_clicks, data):
        if not data:
            return dash.no_update

        df = pd.DataFrame(data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
            buffer.seek(0)

        return dcc.send_bytes(buffer.getvalue(), filename="dados_financeiro_obra.xlsx")