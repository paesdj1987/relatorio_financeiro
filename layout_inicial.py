# layout_inicial.py
import dash_bootstrap_components as dbc
from dash import html

def create_home_layout():
    return html.Div(
        [
            # Logo animada ao carregar
            html.Img(
                src="/assets/logoor.png",
                style={
                    "width": "220px",  # Tamanho levemente maior para destaque
                    "height": "auto",
                    "margin-bottom": "80px",
                    "opacity": "0",
                    "animation": "fadeIn 1.2s ease-in-out forwards"
                }
            ),

            # Título estilizado
            html.H1(
                "Relatórios PGI",
                style={
                    "color": "#343a40",
                    "fontSize": "44px",
                    "fontWeight": "bold",
                    "margin-bottom": "80px",
                    "letter-spacing": "1.5px",
                    "text-transform": "uppercase",
                    "opacity": "0",
                    "animation": "fadeIn 1.2s ease-in-out 0.3s forwards"
                }
            ),

            # Container de botões
            html.Div(
                [
                    dbc.Button(
                        "Mapa de Controle",
                        href="/mapa-controle",
                        style={
                            "background-color": "#3d5462",
                            "color": "white",
                            "border": "2px solid #3d5462",
                            "border-radius": "25px",
                            "padding": "14px 32px",
                            "margin": "20px", # Mais espaçamento entre botões
                            "font-size": "18px", # Fonte levemente maior
                            "font-weight": "bold",
                            "transition": "all 0.3s ease-in-out",
                            "cursor": "pointer",
                            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                        },
                        className="btn-home"
                    ),
                    dbc.Button(
                        "Análise de Contrato",
                        href="/analise-contrato",
                        style={
                            "background-color": "#3d5462",
                            "color": "white",
                            "border": "2px solid #3d5462",
                            "border-radius": "25px",
                            "padding": "14px 32px",
                            "margin": "20px", # Mais espaçamento entre botões
                            "font-size": "18px", # Fonte levemente maior
                            "font-weight": "bold",
                            "transition": "all 0.3s ease-in-out",
                            "cursor": "pointer",
                            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                        },
                        className="btn-home"
                    ),
                    dbc.Button(
                        "Saldo de Contrato",
                        href="/saldo-contrato",
                        style={
                            "background-color": "#3d5462",
                            "color": "white",
                            "border": "2px solid #3d5462",
                            "border-radius": "25px",
                            "padding": "14px 32px",
                            "margin": "20px", # Mais espaçamento entre botões
                            "font-size": "18px", # Fonte levemente maior
                            "font-weight": "bold",
                            "transition": "all 0.3s ease-in-out",
                            "cursor": "pointer",
                            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                        },
                        className="btn-home"
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "flex-wrap": "wrap",
                    "opacity": "0",
                    "animation": "fadeIn 1.2s ease-in-out 0.6s forwards"
                }
            )
        ],
        style={
            "background-color": "white",
            "min-height": "100vh",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "text-align": "center"
        },
        className="home-container"  # <--- adicionado aqui
    )
