# sidebar.py
from dash import html
import dash_bootstrap_components as dbc

def create_sidebar():
    sidebar = html.Div(
        [
            # Cabeçalho
            html.Div(
                [
                    html.Img(src="/assets/logo.png", className="sidebar-logo"),
                    html.H2("Relatório - PGI", className="sidebar-title")
                ],
                className="sidebar-header"
            ),

            html.Hr(className="sidebar-divider"),

            # Seção de Navegação
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

            # Navegação
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.I(className="fas fa-table me-2"),
                            html.Span("Mapa de Controle")
                        ],
                        href="#",
                        active="exact",
                        className="sidebar-link"
                    ),
                ],
                vertical=True,
                pills=True,
                className="sidebar-nav"
            ),

            # Rodapé
            html.Div(
                "© 2024 - OR Empreendimentos LTDA.",
                className="sidebar-footer"
            )
        ],
        className="sidebar"  # Classe que aplica os estilos
    )

    return sidebar
