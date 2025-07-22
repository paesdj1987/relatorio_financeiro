# menu_analise_contrato/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout():
    """
    Retorna o layout principal do módulo Análise de Contrato,
    contendo inicialmente apenas o cabeçalho moderno com largura ajustada.
    """

    # 1. Cabeçalho

    header = dbc.Container(
        fluid=True,
        style={
            "background": "linear-gradient(135deg, #283E51 0%, #4B79A1 100%)",
            "padding": "18px",
            "borderBottom": "3px solid #FFA80B",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "borderBottomLeftRadius": "12px",
            "borderBottomRightRadius": "12px"
        },
        children=[
            dbc.Row(
                align="center",
                justify="between",
                children=[
                    # Coluna da ESQUERDA: Logo + Título
                    dbc.Col(
                        html.Div(
                            [
                                html.Img(
                                    src="/assets/logoOR2.png",
                                    height="60px",
                                    style={"marginRight": "15px"}
                                ),
                                html.H1(
                                    "Análise de Contrato",
                                    className="h2 text-white mb-0",
                                    style={
                                        "fontWeight": "700",
                                        "fontSize": "35px",
                                        "margin": "0"
                                    }
                                ),
                            ],
                            className="d-flex align-items-center"
                        ),
                        width="auto"
                    ),

                    # Coluna da DIREITA  ─ Logout (em cima) + Navegação (embaixo)
                    dbc.Col(
                        html.Div(
                            [
                                # ─── 1. Botão / imagem de Logout ───
                                dcc.Link(
                                    html.Img(
                                        src="/assets/logout.png",    
                                        height="26px",
                                        title="Sair da Aplicação",
                                        style={
                                            "cursor": "pointer",
                                            "position": "relative",
                                            "top": "-10px",           
                                            "left": "-8px",
                                            "marginBottom": "12px"   
                                        }
                                    ),
                                    href="/logout",     
                                    refresh=True
                                ),

                                # ─── 2. Bloco de links de navegação ───
                                html.Div(
                                    [
                                        dcc.Link(
                                            dbc.Button("Home", color="light", outline=True,
                                                       className="me-2 nav-button", style={"fontSize": "14px"}),
                                            href="/", refresh=False
                                        ),
                                        dcc.Link(
                                            dbc.Button("Mapa de Controle", color="light", outline=True,
                                                       className="me-2 nav-button", style={"fontSize": "14px"}),
                                            href="/mapa-controle", refresh=False
                                        ),
                                        dcc.Link(
                                            dbc.Button("Análise de Contrato", color="light", outline=True,
                                                       className="me-2 nav-button", style={"fontSize": "14px"}),
                                            href="/analise-contrato", refresh=False
                                        ),
                                        dcc.Link(
                                            dbc.Button("Saldo Contrato", color="light", outline=True,
                                                       className="me-2 nav-button", style={"fontSize": "14px"}),
                                            href="/saldo-contrato", refresh=False
                                        ),
                                    ],
                                    className="d-flex justify-content-end align-items-center"
                                ),
                            ],
                            # Coluna vira “empilhada”: logout em cima, links embaixo
                            className="d-flex flex-column align-items-end",
                            style={"marginTop": "20px"}
                        ),
                        width="auto"
                    )

                ]
            )
        ]
    )

    # 2. Aviso "Em construção"
    aviso = dbc.Container(
        dbc.Alert(
            "🚧 Página em construção 🚧",
            color="warning",
            style={
                "textAlign": "center",
                "maxWidth": "600px",
                "margin": "0 auto",
                "fontSize": "24px",
                "fontWeight": "600"
            }
        ),
        fluid=True,
        style={
            "marginTop": "200px"   
        }
    )

    # Retorna o cabeçalho dentro de um container 
    return html.Div(
        [header, aviso],
        id="page-content",
        style={
            "maxWidth": "2400px",   
            "margin": "0 auto",     
            "padding": "0 20px"     
        }
    )


