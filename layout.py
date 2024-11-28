# layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from sidebar import create_sidebar

def create_layout():
    content = html.Div(
        [
            # Título
            html.Div(
                [
                    html.H1(
                        "Financeiro Obra - PGI",
                        style={
                            "font-size": "38px",
                            "font-weight": "600",
                            "color": "#343a40",
                            "letter-spacing": "1.5px",
                            "text-align": "center",
                            "margin": "0",
                        }
                    ),
                    # Linha decorativa abaixo do título
                    html.Div(
                        style={
                            "width": "500px",
                            "height": "3px",
                            "background-color": "#343a40",
                            "margin": "10px auto 20px auto"
                        }
                    )
                ],
                style={
                    "text-align": "center",
                    "padding": "20px 0 40px 0",
                }
            ),

            # Linha para campos de pesquisa (SC, PC e NF)
            html.Div(
                [
                    dcc.Input(
                        id='input-filter-sc',
                        type='text',
                        placeholder='Pesquisar por SC...',
                        style={
                            'margin-bottom': '30px',
                            'width': '240px',
                            'height': '42px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '15px',
                            'margin-right': '15px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    dcc.Input(
                        id='input-filter-pc',
                        type='text',
                        placeholder='Pesquisar por PC...',
                        style={
                            'margin-bottom': '30px',
                            'width': '240px',
                            'height': '42px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '15px',
                            'margin-right': '15px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                    dcc.Input(
                        id='input-filter-nf',
                        type='text',
                        placeholder='Pesquisar por NF...',
                        style={
                            'margin-bottom': '30px',
                            'width': '240px',
                            'height': '42px',
                            'border-radius': '12px',
                            'border': '1px solid #d1d1d1',
                            'background-color': '#ffffff',
                            'padding-left': '15px',
                            'box-shadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                            'transition': 'all 0.3s ease-in-out',
                        }
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center"
                }
            ),

            # Div para os botões
            html.Div(
                [
                    dbc.Button(
                        "Consultar Visualização",
                        id="consultar-button",
                        color="success",
                        className="button mt-3",
                        disabled=False,
                        n_clicks=0,
                        style={
                            "background-color": "#FAA61A",  # Cor sólida
                            "border-radius": "25px",  # Bordas arredondadas
                            "border": "none",
                            "color": "white",
                            "font-size": "16px",
                            "font-weight": "bold",
                            "padding": "12px 30px",  # Tamanho aumentado
                            "box-shadow": "0 4px 10px rgba(0,0,0,0.25)",  # Sombra moderna
                            "margin-right": "15px",
                            "transition": "all 0.3s ease-in-out",  # Transição suave
                            "cursor": "pointer",
                        },
                    ),
                    dbc.Button(
                        "Limpar Pesquisa",
                        id="limpar-button",
                        color="secondary",
                        className="button mt-3",
                        disabled=False,
                        n_clicks=0,
                        style={
                            "background-color": "#455F6B",  # Cor sólida
                            "border-radius": "25px",  # Bordas arredondadas
                            "border": "none",
                            "color": "white",
                            "font-size": "16px",
                            "font-weight": "bold",
                            "padding": "12px 30px",  # Tamanho aumentado
                            "box-shadow": "0 4px 10px rgba(0,0,0,0.25)",  # Sombra moderna
                            "transition": "all 0.3s ease-in-out",  # Transição suave
                            "cursor": "pointer",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "margin-bottom": "20px",
                }
            ),

            # Div para o ícone de exportação
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
                                "width": "50px",
                                "cursor": "pointer",
                            }
                        ),
                        id="download-excel-link",
                    ),
                ],
                style={
                    "text-align": "right",
                    "margin-bottom": "15px",
                    "display": "none",
                }
            ),

            # Componente de Loading envolvendo o output-div
            dcc.Loading(
                id="loading-output",
                type="circle",
                children=[html.Div(id="output-div", className="mt-3")]
            ),

            # Componente para download
            dcc.Download(id="download-dataframe-xlsx"),

            # Componente dcc.Location para refresh da página
            dcc.Location(id='url', refresh=True),
            
            # Adicione isso ao final do layout.py
            html.Div(id='dummy-output', style={'display': 'none'})

        ],
        id="page-content",
        style={
            "margin-left": "200px",
            "padding": "20px",
            "transition": "margin-left 0.5s",
            "text-align": "center",
        }
    )

    layout = html.Div(
        [
            dcc.Location(id="url"),
            create_sidebar(),
            content
        ]
    )

    return layout
