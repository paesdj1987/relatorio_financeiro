# callbacks.py
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table, dcc, html, no_update
import io

def register_callbacks(app):
    global df_global
    df_global = None

    @app.callback(
        [
            Output("output-div", "children"),
            Output("export-div", "style")
        ],
        [
            Input("consultar-button", "n_clicks"),
            Input("limpar-button", "n_clicks")
        ],
        [
            State("input-filter-sc", "value"),
            State("input-filter-pc", "value"),
            State("input-filter-nf", "value")
        ],
        prevent_initial_call=True
    )
    def update_output(n_clicks_consultar, n_clicks_limpar, sc_filter, pc_filter, nf_filter):
        global df_global

        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update, no_update

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'consultar-button':
            try:
                # Ler dados do arquivo CSV gerado pelo request.py
                df = pd.read_csv(
                    'vw_financeiro_obra.csv',
                    encoding='utf-8',
                    sep=';',
                    quotechar='"',
                    dtype=str,
                    engine='python'
                )

                # Garantir que as colunas relevantes sejam tratadas como strings
                df = df.fillna('')

                # Aplicar filtros, se houver
                if sc_filter:
                    sc_filter = str(sc_filter).strip()
                    df = df[df["N_da_SC"].str.contains(sc_filter, case=False, na=False)]

                if pc_filter:
                    pc_filter = str(pc_filter).strip()
                    df = df[df["N_do_PC"].str.contains(pc_filter, case=False, na=False)]

                if nf_filter:
                    nf_filter = str(nf_filter).strip()
                    df = df[df["N_da_NF"].str.contains(nf_filter, case=False, na=False)]

                df_global = df

                if df.empty:
                    table = html.Div("Nenhum resultado encontrado.")
                    export_style = {"display": "none"}
                else:
                    table = html.Div([
                        dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'name': col.replace('_', ' '), 'id': col} for col in df.columns],
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'center',
                                'padding': '10px',
                                'whiteSpace': 'normal',
                                'fontSize': '12px',
                            },
                            style_header={
                                'backgroundColor': '#343a40',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'fontSize': '14px',
                            },
                            style_data={
                                'backgroundColor': 'white',
                                'color': '#343a40'
                            },
                            page_size=10,
                        )
                    ])

                    export_style = {
                        "text-align": "right",
                        "margin-bottom": "10px",
                        "display": "block",
                    }

                return table, export_style

            except Exception as e:
                return f"Erro ao ler os dados do CSV: {e}", {"display": "none"}

        elif button_id == 'limpar-button':
            # Retorne valores padrão e deixe o client-side callback cuidar do refresh
            return "", {"display": "none"}

        return no_update, no_update

    @app.callback(
        Output("download-dataframe-xlsx", "data"),
        [Input("download-excel-icon", "n_clicks")],
        prevent_initial_call=True,
    )
    def download_excel(n_clicks):
        global df_global
        if df_global is not None and not df_global.empty:
            # Converte o DataFrame para um arquivo Excel em memória
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_global.to_excel(writer, index=False)
                buffer.seek(0)

            return dcc.send_bytes(
                buffer.getvalue(),
                filename="dados_financeiro_obra.xlsx"
            )
        else:
            return dash.no_update
