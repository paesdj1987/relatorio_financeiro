# sidebar.py
from dash import html
import dash_bootstrap_components as dbc

def create_sidebar():
    # Cabeçalho do sidebar
    sidebar_header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src="/assets/logo.png", 
                        height="50px", 
                        style={"margin-bottom": "10px"}
                    ),
                    html.H3(
                        "Relatório - PGI",
                        className="display-7",
                        style={
                            "color": "white",
                            "font-size": "20px",
                            "font-weight": "bold",
                            "margin": "0",
                        }
                    ),
                ],
                style={
                    "text-align": "center",
                    "background-color": "#344955",
                    "padding": "15px 10px",
                    "border-radius": "12px",
                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",
                },
            )
        ],
        style={
            "margin-bottom": "20px",
        },
    )

    # Itens do menu
    menu_items = [
        html.Div(
            [
                html.Div(
                    "Navegação",
                    style={
                        "color": "#A9BCC1",
                        "font-size": "14px",
                        "font-weight": "bold",
                        "margin-top": "20px",
                        "margin-bottom": "8px",
                    },
                ),
                dbc.NavLink(
                [
                    html.I(className="fas fa-table me-3", style={"margin-right": "20px"}),  # Ajuste do ícone
                    html.Span("Mapa de Controle"),
                ],
                href="#",
                active="exact",
                className="nav-link",
                style={
                    "color": "white",
                    "font-size": "14px",
                    "padding": "12px 8px",  # Reduzido o padding horizontal
                    "border-radius": "8px",
                    "transition": "all 0.3s ease-in-out",
                    "justify-content": "flex-start",  # Força os itens a alinharem à esquerda
                    "display": "flex",  # Garante que flexbox é aplicado
                    "align-items": "center",  # Centraliza verticalmente os itens
                },
            ),
           

            ],
            style={
                "margin-bottom": "20px",
            },
        ),
    ]

    # Rodapé do sidebar
    sidebar_footer = html.Div(
        [
            html.Div(
                "© 2024 - OR Empreendimentos LTDA.",
                style={
                    "color": "#A9BCC1",
                    "font-size": "12px",
                    "text-align": "center",  # Centraliza o texto no próprio elemento
                },
            ),
        ],
        style={
            "position": "absolute",
            "bottom": "10px",
            "left": "50%",  # Centraliza horizontalmente usando o ponto médio
            "transform": "translateX(-50%)",  # Ajusta para que o rodapé fique centralizado
            "width": "fit-content",  # Evita que o rodapé ocupe largura desnecessária
        },
    )


    # Sidebar completo
    sidebar = html.Div(
        [
            sidebar_header,
            dbc.Nav(menu_items, vertical=True, pills=True),
            sidebar_footer,
        ],
        id="sidebar",
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "200px",
            "padding": "20px",
            "background-color": "#455F6B",
            "color": "white",
            "transition": "all 0.5s ease-in-out",
            "box-shadow": "2px 0px 5px rgba(0, 0, 0, 0.2)",
        },
    )

    return sidebar
