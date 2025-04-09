from dash import html

def create_layout():
    return html.Div(
        [
            html.H1("Análise de Contrato", style={"text-align": "center"}),
            html.Div("Aqui colocaremos a lógica de Análise de Contrato.")
        ],
        style={"padding": "20px"}
    )
