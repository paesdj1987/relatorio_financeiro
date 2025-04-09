import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc
import os

# Importação do layout e callbacks
from menu_mapa_controle.layout import create_layout as layout_mapa_controle
from menu_mapa_controle.callbacks import register_callbacks
from layout_inicial import create_home_layout
import request  
from request import fetch_data_from_oracle

# Chama o request.py para garantir que os dados estejam disponíveis
if not os.path.exists('shared_data/vw_financeiro_obra.csv'):
    print("Arquivo CSV não encontrado. Atualizando dados do Oracle...")
    fetch_data_from_oracle()
else:
    print("Arquivo CSV encontrado. Dados prontos!")

# Estilos externos
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
    "/assets/style.css",
]

# Inicialização do Dash
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title="Relatório - PGI"
)

# Layout dinâmico baseado em rotas
app.layout = html.Div([
    dcc.Location(id='url'),  # Detecta a URL
    html.Div(id='layout-wrapper')  # Onde o conteúdo será carregado dinamicamente
])

# Callback para alternar entre Home e Páginas com Sidebar
@app.callback(
    Output('layout-wrapper', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """Carrega o layout correto com ou sem sidebar"""
    if pathname in ["/", "/home", "/home/"]:
        return create_home_layout()  
    elif pathname in ["/mapa-controle", "/mapa-controle/"]:
        return layout_mapa_controle()
    else:
        return create_home_layout()  # Qualquer outra rota volta para a Home

# Registrar Callbacks do Mapa de Controle
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
    print("Aplicação iniciada com sucesso...")
    app.run(debug=False, host='0.0.0.0', port=8052)
