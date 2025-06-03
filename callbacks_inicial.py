# callbacks_inicial.py

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import session
from ldap_auth import authenticate_and_authorize
from pathlib import Path
from datetime import datetime
import csv, pytz, dash

LOG_FILE = Path("shared_data/log_historico_acesso.csv")

def registrar_acesso(usuario: str):
    ts = datetime.now(pytz.timezone("America/Bahia")).strftime("%d/%m/%Y %H:%M:%S")
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerow([usuario, ts])

def register_callbacks_inicial(app):
    @app.callback(
        Output("login-message", "children"),
        Output("login-message", "is_open"),
        Output("login-message", "color"),
        Output("url", "pathname"),
        Input("login-button", "n_clicks"),
        State("input-user", "value"),
        State("input-senha", "value"),
        prevent_initial_call=True,
    )
    def on_login(n_clicks, usuario, senha):
        if not n_clicks:
            raise PreventUpdate

        # 1) Campos vazios
        if not usuario or not senha:
            return (
                "Preencha usuário e senha",
                True,
                "warning",    
                dash.no_update
            )

        # 2) Tenta autenticar
        try:
            validado = authenticate_and_authorize(usuario, senha)
        except RuntimeError:
            return (
                "Servidor indisponível. Tente mais tarde.",
                True,
                "danger",      
                dash.no_update
            )

        # 3) Sucesso
        if validado:
            session["usuario"]    = usuario
            session["login_time"] = datetime.now(
                pytz.timezone("America/Bahia")
            ).timestamp()
            registrar_acesso(usuario)
            return (
                "Acesso autorizado",
                True,
                "success",    
                "/home"
            )

        # 4) Credenciais inválidas
        return (
            "Usuário e/ou senha inválido",
            True,
            "danger",
            dash.no_update
        )
