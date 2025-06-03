# Relatórios PGI

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

- `Mapa de Controle` — Filtros avançados e visualização dos dados
- `Análise de Contrato` — (em desenvolvimento)
- `Saldo de Contrato` — (em desenvolvimento)

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
```bash
git clone https://github.com/paesdj1987/vw_financeiro_obra.git
cd vw_financeiro_obra

2. Instale as dependências:
pip install -r requirements.txt

3. Configure o arquivo .env com as variáveis de ambiente LDAP.

4. Execute o projeto:
python app.py

👤 Autor
Desenvolvido por João Paes
🔗 github.com/paesdj1987