# app.py

import os
from dotenv import load_dotenv

load_dotenv()

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc, clientside_callback
from flask import session
from datetime import datetime
import pytz

# ─────────────────────────────────────────────────────────────
# Configurações gerais

FLASK_SECRET = os.getenv("FLASK_SECRET")
SESSION_TIMEOUT = 3600  # 1 h

# ─────────────────────────────────────────────────────────────
# Importa layouts / callbacks dos módulos

from menu_mapa_controle.layout    import create_layout as layout_mapa_controle
from menu_mapa_controle.callbacks import register_callbacks_mapa
from menu_analise_contrato.layout import create_layout as layout_analise_contrato
from menu_analise_contrato.callbacks import register_callbacks_analise
from menu_saldo_contrato.layout    import create_layout as layout_saldo_contrato
from menu_saldo_contrato.callbacks import register_callbacks_saldo
from callbacks_inicial             import register_callbacks_inicial
from layout_inicial                import create_home_layout

# ─────────────────────────────────────────────────────────────
# Instancia o Dash

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
        "/assets/style.css",
    ],
    suppress_callback_exceptions=True,
    title="Relatórios PGI",
    update_title=None,
)
app.server.secret_key = FLASK_SECRET      # segredo Flask
server = app.server                       # exportado para Gunicorn

# ─────────────────────────────────────────────────────────────
# Layout raiz

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="layout-wrapper"),
        html.Div(id="dummy-output", style={"display": "none"}),
    ]
)

# ─────────────────────────────────────────────────────────────
# Roteamento + proteção de sessão

@app.callback(Output("layout-wrapper", "children"), Input("url", "pathname"))
def display_page(pathname):
    usuario  = session.get("usuario")
    login_ts = session.get("login_time")
    agora    = datetime.now(pytz.timezone("America/Bahia")).timestamp()
    autorizado = False

    # ─── 1. Se for logout, limpa a sessão e volta à Home ───
    if pathname == "/logout":
        session.clear()
        return create_home_layout(False)

    # ─── 2. Verifica e rearma timeout
    if usuario and login_ts and (agora - login_ts) <= SESSION_TIMEOUT:
        autorizado = True
        session["login_time"] = agora
    else:
        if login_ts and (agora - login_ts) > SESSION_TIMEOUT:
            session.clear()

    # Home (login)
    if pathname in ["/", "/home", "/home/"]:
        return create_home_layout(autorizado)

    # Demais rotas exigem login
    if not autorizado:
        return create_home_layout(False)

    # Rotas protegidas
    if pathname.startswith("/mapa-controle"):
        return layout_mapa_controle()
    if pathname.startswith("/analise-contrato"):
        return layout_analise_contrato()
    if pathname.startswith("/saldo-contrato"):
        return layout_saldo_contrato()


    # Fallback
    return create_home_layout(autorizado)

# ─────────────────────────────────────────────────────────────
# Registra callbacks dos módulos

register_callbacks_mapa(app)
register_callbacks_analise(app)
register_callbacks_saldo(app)
register_callbacks_inicial(app)

# ─────────────────────────────────────────────────────────────
# Client-side: botão “Limpar” 

clientside_callback(
    """
    function(n){
        if (n) {
            window.location.reload();
        }
        return '';
    }
    """,
    Output("dummy-output", "children"),
    Input("limpar-button", "n_clicks"),
    prevent_initial_call=True,
)

# ─────────────────────────────────────────────────────────────
# Execução local (desenvolvimento)

if __name__ == "__main__":
    print("Aplicação iniciada em modo DEV…")
    app.run_server(debug=True, host="0.0.0.0", port=8052)