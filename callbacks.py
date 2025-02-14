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
            State("input-filter-nf", "value"),
            State("input-filter-cod-obra", "value"),
            State("input-filter-insumo", "value"),
            State("input-filter-fornecedor", "value"),
            State("input-filter-ua-codigo", "value"),
        ],
        prevent_initial_call=True
    )
    def update_output(n_clicks_consultar, n_clicks_limpar, 
                      sc_filter, pc_filter, nf_filter, 
                      cod_obra_filter, insumo_filter,
                      fornecedor_filter, ua_codigo_filter):
        global df_global

        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update, no_update

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'consultar-button':
            try:
                # Ler dados do arquivo CSV gerado pelo request.py
                df = pd.read_csv(
                    'shared_data/vw_financeiro_obra.csv',  # Caminho para a pasta shared_data
                    encoding='utf-8',
                    sep=';',
                    quotechar='"',
                    dtype=str,
                    engine='python'
                )

                # Garantir que as colunas sejam tratadas como strings
                df = df.fillna('')

                # Aplicar filtros
                if sc_filter:
                    sc_filter = [item.strip() for item in sc_filter.split(';')]
                    df = df[df["N_da_SC"].isin(sc_filter)]

                if pc_filter:
                    pc_filter = [item.strip() for item in pc_filter.split(';')]
                    df = df[df["N_do_PC"].isin(pc_filter)]

                if nf_filter:
                    nf_filter = [item.strip() for item in nf_filter.split(';')]
                    df = df[df["N_da_NF"].isin(nf_filter)]

                if cod_obra_filter:
                    cod_obra_filter = [item.strip() for item in cod_obra_filter.split(';')]
                    df = df[df["Cod_Obra"].isin(cod_obra_filter)]

                if insumo_filter:
                    insumo_filter = [item.strip() for item in insumo_filter.split(';')]
                    df = df[df["Descricao_do_insumo"].apply(
                        lambda x: any(term.lower() in x.lower() for term in insumo_filter)
                    )]
                if fornecedor_filter:
                    fornecedor_filter = [item.strip() for item in fornecedor_filter.split(';')]
                    df = df[df["Fornecedor"].apply(
                    lambda x: any(term.lower() in x.lower() for term in fornecedor_filter)
                    )]

                if ua_codigo_filter:
                    ua_codigo_filter = [item.strip() for item in ua_codigo_filter.split(';')]
                    df = df[df["UA__Código"].isin(ua_codigo_filter)]

                df_global = df

                # Construir a tabela ou mensagem de vazio
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
            # Retorna valores padrão e deixa o client-side callback recarregar a página
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
            # Converter o DataFrame para um arquivo Excel em memória
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
