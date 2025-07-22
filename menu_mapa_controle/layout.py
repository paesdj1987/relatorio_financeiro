# menu_mapa_controle/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout():
    """
    Retorna o layout principal do Mapa de Controle
    contendo:
      1. Cabeçalho moderno (header)
      2. Seção de conteúdo (pesquisa, botões, tabela etc.)
    """
    cache = dcc.Store(id="df-cache", storage_type="memory")
    
    # ----------------------------------------------------------------
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
                                "Mapa de Controle",
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
                            className="d-flex flex-column align-items-end",
                            style={"marginTop": "20px"}
                        ),
                        width="auto"
                    )

            ]
        )
    ]
)

    # ----------------------------------------------------------------
    # 2. Conteúdo Específico do Mapa de Controle

    content = html.Div(
    [
        # Primeira linha de filtros (SC, PC, NF, UO)
        dbc.Row(
            style={"marginTop": "60px", "marginBottom": "30px"},
            justify="center",
            children=[
                dbc.Col(
                    html.Div(                             
                        [
                            dcc.Input(
                                id="input-filter-cod-obra",
                                type="text",
                                placeholder="Pesquisar por UO...",
                                style={
                                    "width": "100%",
                                    "height": "42px",
                                    "font-size": "12px",
                                    "border-radius": "12px",
                                    "border": "1px solid #d1d1d1",
                                    "background-color": "#ffffff",
                                    "padding-left": "10px",
                                    "box-shadow": "0 3px 6px rgba(0,0,0,0.1)",
                                    "transition": "all 0.3s ease-in-out",
                                },
                            ),
                            html.Span(
                                "*",
                                style={
                                    "color": "red",
                                    "font-size": "22px",
                                    "position": "absolute",
                                    "right": "8px",        # distância da borda direita
                                    "top": "8px",          # distância da borda superior
                                },
                            ),
                        ],
                        style={"position": "relative"},     # base para o absolute
                    ),
                    xs=12, sm=6, md=3, lg=2,
                ),
                dbc.Col(
                    html.Div(
                        [
                            dcc.Input(
                                id='input-filter-sc',
                                type='text',
                                placeholder='Pesquisar por SC...',
                                style={
                                    'flex': '1',
                                    'height': '42px',
                                    'font-size': '12px',
                                    'border-radius': '12px',
                                    'border': '1px solid #d1d1d1',
                                    'background-color': '#ffffff',
                                    'padding-left': '10px',
                                    'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                                    'transition': 'all 0.3s ease-in-out',
                                }
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    ),
                    xs=12, sm=6, md=3, lg=2  
                ),

                dbc.Col(
                    dcc.Input(
                        id='input-filter-pc',
                        type='text',
                        placeholder='Pesquisar por PC...',
                        style={
                            'width': '100%',
                            'height': '42px',
                            'font-size': '12px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '10px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    xs=12, sm=6, md=3, lg=2
                ),
                dbc.Col(
                    dcc.Input(
                        id='input-filter-nf',
                        type='text',
                        placeholder='Pesquisar por NF...',
                        style={
                            'width': '100%',
                            'height': '42px',
                            'font-size': '12px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '10px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    xs=12, sm=6, md=3, lg=2
                ),
                

            ],
        ),

        # Segunda linha de filtros (Insumo, Fornecedor, UA, ...)
        dbc.Row(
            style={"marginTop": "50px", "marginBottom": "30px"},
            justify="center",
            children=[
                dbc.Col(
                    dcc.Input(
                        id='input-filter-insumo',
                        type='text',
                        placeholder='Pesquisar por Insumo...',
                        style={
                            'width': '100%',
                            'height': '42px',
                            'font-size': '12px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '10px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    xs=12, sm=6, md=3, lg=2
                ),
                dbc.Col(
                    dcc.Input(
                        id='input-filter-fornecedor',
                        type='text',
                        placeholder='Pesquisar por Fornecedor...',
                        style={
                            'width': '100%',
                            'height': '42px',
                            'font-size': '12px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '10px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    xs=12, sm=6, md=3, lg=2
                ),
                dbc.Col(
                    dcc.Input(
                        id='input-filter-ua-codigo',
                        type='text',
                        placeholder='Pesquisar por UA...',
                        style={
                            'width': '100%',
                            'height': '42px',
                            'font-size': '12px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '10px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    xs=12, sm=6, md=3, lg=2
                ),
            ]
        ),

        # ----------------------------------------------------------------
        #  Linha: intervalo de datas (Data_da_SC)
       
        dbc.Row(
            style={"marginTop": "50px", "marginBottom": "30px"},
            justify="center",
            children=[
                dbc.Col(                      
                    html.Div(
                        [
                            #html.Span("*", className="required-asterisk"),
                            dcc.DatePickerSingle(
                                id="data-sc-start",
                                display_format="DD/MM/YYYY",
                                placeholder="Início Data SC",
                                className="date-pick date-pick-left",
                            ),
                            html.Span("→", className="date-arrow"),
                            dcc.DatePickerSingle(
                                id="data-sc-end",
                                display_format="DD/MM/YYYY",
                                placeholder="Fim Data SC",
                                className="date-pick date-pick-right",
                            ),
                        ],
                        className="d-flex justify-content-center align-items-center",
                    ),
                    width="auto",              
                    className="mx-auto",     
                ),
            ],
        ),


        # Div para os botões
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    dbc.Button(
                        "Consultar Visualização",
                        id="consultar-button",
                        color="warning",
                        className="me-3",
                        style={
                            "border-radius": "25px",
                            "background-color": "#FAA61A",
                            "color": "white",
                            "border": "none",
                            "font-size": "14px",
                            "font-weight": "bold",
                            "padding": "10px 26px",
                            "boxShadow": "0 4px 10px rgba(0,0,0,0.25)",
                            "transition": "all 0.3s ease-in-out",
                            "marginTop": "25px",
                            "cursor": "pointer",
                        },
                    ),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button(
                        "Limpar Pesquisa",
                        id="limpar-button",
                        color="secondary",
                        style={
                            "border-radius": "25px",
                            "border": "none",
                            "color": "white",
                            "font-size": "14px",
                            "font-weight": "bold",
                            "padding": "10px 26px",
                            "boxShadow": "0 4px 10px rgba(0,0,0,0.25)",
                            "transition": "all 0.3s ease-in-out",
                            "marginTop": "25px",
                            "cursor": "pointer",
                        },
                    ),
                    width="auto"
                )
            ]
        ),

        html.Div(style={"height": "40px"}),  

            # Ícone de exportação
            html.Div(
                id="export-div",
                children=[
                    html.A(
                        html.Img(
                            src="/assets/excel.png",
                            id="download-excel-icon",
                            n_clicks=0,
                            style={
                                "height": "50px",
                                "width": "60px",
                                "cursor": "pointer",
                            }
                        ),
                        id="download-excel-link",
                    ),
                ],
                style={
                    "text-align": "left",       
                    "margin-bottom": "20px",
                    "margin-left": "20px",       
                    "display": "none",
                }
            ),

            # Tabela (carregada dinamicamente)
            dcc.Loading(
                id="loading-output",
                type="circle",
                children=[html.Div(id="output-div", className="mt-3", style={"margin-left": "20px"})]
            ),


            # Componente para download
            dcc.Download(id="download-dataframe-xlsx"),

            html.Div(id='dummy-output', style={'display': 'none'})
        ],
        id="page-content",
    )

    # ----------------------------------------------------------------
    # Header + Conteúdo

    return html.Div(
        [
        header,
        cache,
        content,
        ],
        style={
            "maxWidth": "2400px",   
            "margin": "0 auto",      
            "padding": "0 20px"      
        }
    )
