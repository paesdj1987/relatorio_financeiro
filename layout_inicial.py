# layout_inicial.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from flask import session  # Para obter o usuário logado

def create_home_layout(authorized: bool = False):

    # 1. Cabeçalho (logo + título)
    header_group = html.Div(
        [
            html.Img(
                src="/assets/logoor.png",
                style={
                    "width": "170px",
                    "height": "auto",
                    "opacity": "0",
                    "animation": "fadeIn 1.2s ease-in-out forwards",
                    "marginBottom": "20px",
                },
            ),
            html.H1(
                "Relatórios PGI",
                style={
                    "color": "#3d5462",
                    "fontSize": "30px",
                    "fontWeight": "bold",
                    "letterSpacing": "1.5px",
                    "textTransform": "uppercase",
                    "opacity": "0",
                    "animation": "fadeIn 1.2s ease-in-out 0.3s forwards",
                },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "transform": "translateY(-40px)",
            "marginTop": "10px",
        },
        className="header-group",
    )

    # Inicia lista de componentes
    children = [header_group]

    # 2. Se NÃO autorizado: exibe apenas o card de login
    if not authorized:
        login_body = dbc.CardBody(
            [
                dbc.Label(html_for="input-user", style={"fontWeight": "500", "marginBottom": "1px"}),
                dbc.Input(
                    id="input-user",
                    placeholder="Digite seu usuário",
                    style={"borderColor": "#3d5462", "borderWidth": "1px", "borderRadius": "6px", "marginTop": "1px"},
                ),
                dbc.Label(html_for="input-senha", style={"fontWeight": "500", "marginTop": "10px"}),
                dbc.Input(
                    id="input-senha",
                    type="password",
                    placeholder="Digite sua senha",
                    style={"borderColor": "#3d5462", "borderWidth": "1px", "borderRadius": "6px"},
                ),
                dbc.Button(
                    "Acessar",
                    id="login-button",
                    n_clicks=0,
                    style={
                        "backgroundColor": "#3d5462",
                        "borderColor": "#3d5462",
                        "color": "white",
                        "width": "100%",
                        "marginTop": "20px",
                        "borderRadius": "6px",
                        "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                    },
                ),
                dbc.Alert(
                    "",
                    id="login-message",
                    color="success",
                    is_open=False,
                    duration=15000,
                    style={
                        "marginTop": "12px",
                        "fontSize": "0.875rem",
                        "padding": "6px 12px",
                        "width": "80%",
                        "marginLeft": "auto",
                        "marginRight": "auto",
                    },
                ),
            ],
            style={
                "paddingTop": "4px",
                "paddingBottom": "12px",
                "paddingLeft": "12px",
                "paddingRight": "12px",
            },
        )

        login_card = dbc.Card(
            dcc.Loading(
                id="loading-login",
                type="circle",
                color="#FAA80A",
                children=login_body,
            ),
            style={
                "width": "320px",
                "maxWidth": "90%",
                "border": "1px solid #3d5462",
                "borderRadius": "12px",
                "boxShadow": "0 8px 16px rgba(0,0,0,0.2)",
                "marginTop": "5px",
                "transform": "translateY(-30px)",
                "position": "relative",
            },
            className="login-card",
        )

        children.append(login_card)
    else:
        # 3. Se autorizado: mensagem de boas-vindas + botões de navegação
        usuario = session.get("usuario", "")
        welcome_div = html.Div(
            f"Bem-vind{'o' if usuario.endswith(('a','e','i','o','u')) else 'o'}, {usuario}!",
            style={
                "color": "#3d5462",
                "fontSize": "18px",
                "fontWeight": "500",
                "marginTop": "10px",
                "opacity": "0",
                "animation": "fadeIn 1.2s ease-in-out 0.6s forwards",
                # Espaçamento maior abaixo da mensagem
                "marginBottom": "15px",
            },
            className="welcome-message",
        )
        children.append(welcome_div)

        # Navegação
        def nav_button(label, href):
            base_style = {
                "backgroundColor": "#3d5462",
                "color": "white",
                "border": "2px solid #3d5462",
                "borderRadius": "25px",
                "padding": "10px 26px",
                "marginTop": "20px",
                "marginBottom": "20px",
                "marginLeft": "30px",
                "marginRight": "30px",
                "fontSize": "16px",
                "fontWeight": "bold",
                "transition": "all 0.3s ease-in-out",
                "cursor": "pointer",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.2)",
            }
            return dbc.Button(label, href=href, style=base_style, className="btn-home")

        buttons_container = html.Div(
            [
                nav_button("Mapa de Controle", "/mapa-controle"),
                nav_button("Análise de Contrato", "/analise-contrato"),
                nav_button("Saldo de Contrato", "/saldo-contrato"),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "flexWrap": "wrap",
                "opacity": "0",
                # Aumenta a distância para a mensagem acima
                "marginTop": "20px",
                "animation": "fadeIn 1.2s ease-in-out 0.8s forwards",
            },
            className="buttons-container",
        )

        children.append(buttons_container)

    # 4. Rodapé fixo centralizado
    footer = html.Div(
        "© 2025 OR Empreendimentos LTDA. Todos os direitos reservados.",
        style={
            "position": "absolute",
            "bottom": "10px",
            "width": "100%",
            "textAlign": "center",
            "fontSize": "12px",
            "color": "#414f5a",
        },
        className="footer",
    )
    children.append(footer)

    # 5. Container principal da Home
    return html.Div(
        children,
        style={
            "backgroundColor": "white",
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "textAlign": "center",
        },
        className="home-container",
    )
