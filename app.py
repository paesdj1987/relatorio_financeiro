# app.py
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layout import create_layout
from callbacks import register_callbacks
import os

# Estilos externos
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
    "/assets/style.css",
]

# Inicialização do Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True, title="Financeiro Obra - PGI")

# Layout principal
app.layout = create_layout()

# Registro dos callbacks
register_callbacks(app)

# Client-side callback para recarregar a página
app.clientside_callback(
    """
    function(n_clicks_limpar) {
        if (n_clicks_limpar) {
            window.location.reload();
        }
    }
    """,
    Output('dummy-output', 'children'),
    Input('limpar-button', 'n_clicks'),
    prevent_initial_call=True
)

if __name__ == '__main__':
    # Verificar se o CSV existe antes de iniciar o servidor
    if not os.path.exists('vw_financeiro_obra.csv'):
        print("AVISO: O arquivo vw_financeiro_obra.csv não foi encontrado.")

    print("Aplicação iniciada com sucesso...")
    app.run_server(debug=True, port=8052)
