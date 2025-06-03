# Relatórios de Sistema Financeiro

Dashboard profissional desenvolvido em Python com Dash, voltado à gestão e análise de dados financeiros extraídos de um ERP corporativo. A aplicação permite filtragem avançada, visualização tabular e exportação para Excel com base nos dados da view `vw_financeiro_obra`.

---

<img src="assets/images/img_1.png" alt="Tela de Login" style="max-width: 100%; margin-bottom: 15px;"/>

---

## 🔧 Funcionalidades

- 🔐 **Autenticação via LDAP** com controle de sessão e timeout automático  
- 📄 **Consulta por filtros**: SC, PC, NF, UO, Insumo, Fornecedor e UA  
- 📊 **Exibição tabular interativa** com paginação e responsividade  
- 📤 **Exportação para Excel** com formatação automática  
- 💡 **Interface moderna** com responsividade e animações CSS personalizadas  

---

<img src="assets/images/img_2.png" alt="Tela do Mapa de Controle" style="max-width: 100%; margin-bottom: 15px;"/>

---

## 🧠 Módulos Disponíveis

- `Mapa de Controle` — Visualização completa dos lançamentos de todas as faturas de compras de materiais destinadas às obras. Permite consultas por diversos campos como SC, PC, NF, insumo, fornecedor, entre outros.
- `Análise de Contrato` — (em desenvolvimento) Módulo voltado à análise detalhada (analítica) dos contratos e dos lançamentos financeiros associados aos fornecedores.
- `Saldo de Contrato` — (em desenvolvimento) Módulo com foco em fornecer uma visão consolidada e simplificada dos contratos firmados, sem detalhamentos técnicos.

---

## 📌 Explicação dos Filtros do Mapa de Controle

Cada campo de pesquisa na tela do *Mapa de Controle* permite ao usuário refinar os dados com precisão. Abaixo, seguem as siglas utilizadas:

- 🔎 **SC** — *Solicitação de Compra*: permite pesquisar as solicitações de materiais feitas para as obras.
- 🔎 **PC** — *Pedido de Compra*: pesquisa os pedidos formalizados a fornecedores.
- 🔎 **NF** — *Nota Fiscal*: busca por documentos fiscais relacionados às entregas.
- 🏗️ **UO** — *Unidade Organizacional*: cada unidade representa um empreendimento da empresa.
- 🧱 **Insumo** — permite filtrar por tipo de material solicitado ou adquirido.
- 🧾 **Fornecedor** — busca pelos parceiros comerciais que forneceram os produtos ou serviços.
- 💼 **UA** — *Unidade Analítica*: refere-se ao centro de custo ou unidade contábil utilizada internamente.

Esses filtros foram desenvolvidos para proporcionar **flexibilidade e agilidade** na análise dos dados financeiros da operação.

---

## 🗂️ Estrutura do Projeto

├── app.py
├── layout_inicial.py
├── request.py
├── menu_mapa_controle/
│ ├── layout.py
│ └── callbacks.py
├── assets/
│ ├── styles.css
│ └── images/
│ ├── img_1.png
│ └── img_2.png
├── shared_data/
│ └── vw_financeiro_obra.csv

---

## ⚙️ Tecnologias Utilizadas

> Desenvolvido com **Python** e as bibliotecas:

- [Dash](https://dash.plotly.com/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [oracledb](https://oracle.github.io/python-oracledb/)
- [ldap3](https://ldap3.readthedocs.io/en/latest/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🏁 Como Executar Localmente

1. Clone o repositório:

- git clone https://github.com/paesdj1987/vw_financeiro_obra.git
- cd vw_financeiro_obra

2. Instale as dependências:

- pip install -r requirements.txt

3. Configure o arquivo .env com as variáveis de ambiente LDAP.

4. Execute o projeto:

- python app.py

👤 Autor
Desenvolvido por João Paes
🔗 github.com/paesdj1987