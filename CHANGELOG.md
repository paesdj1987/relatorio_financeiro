# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

## [v1.2.5] - 2025-07-23
### Adicionado
- Inserção de alerta quando nenhuma informação for encontrada na consulta no callbacks.py.

## [v1.2.4] - 2025-07-22
### Adicionado
- Suporte a múltiplas UOs no campo "Pesquisar por UO": agora aceita códigos separados por ponto-e-vírgula e gera cláusula IN dinamicamente no SQL.
- Alterado
- control_map_query (request.py): utiliza TRUNC("sc"."data_registro") para remover o horário e filtra opcionalmente por :dt_ini e :dt_fim na própria query.
- update_output (menu_mapa_controle/callbacks.py): reativado o filtro de intervalo de datas, passando data_sc_start e data_sc_end para o SQL, e ajustada a lógica de cache para considerar mudanças em UO e datas.
- Removida filtragem de Data_da_SC em Python, delegando todo o intervalo de datas à query SQL para otimizar desempenho.

## [v1.2.3] - 2025-06-18
### Adicionado
- Validação em update_output para exibir alerta “Necessário preencher, pelo menos, um (1) campo de pesquisa!” quando nenhum filtro for preenchido.

### Alterado
- Função update_output (menu_mapa_controle/callbacks.py):
- Remoção do horário (hh:mm:ss) das colunas de data na tabela de consulta, formatando-as como dd/mm/yyyy no Excel com XlsxWriter.
- Implementação de cache em memória com TTL de 2 h e uso de threading.Lock para evitar requisições concorrentes ao banco.
- Remoção de chamada direta extra a control_map_query() após o cache.
- Estilização do alerta: centralização, largura definida e marginBottom para espaçar os botões.
- Conversão das mesmas colunas de data para pd.to_datetime(...).dt.date e aplicação de formato dd/mm/yyyy no Excel com XlsxWriter.

## [v1.2.2] - 2025-06-10

### Alterado
- Atualização visual e técnica do `README.md` para fins de portfólio
- Ajuste no request.py
- Ajuste no arquivo .env

## [v1.2.1] - 2025-06-03

### Alterado
- Atualização visual e técnica do `README.md` para fins de portfólio

## [v1.2.0] - 2025-06-03

### Adicionado
- Prints da aplicação e imagens organizadas na pasta `assets/images`
- Estrutura profissional no `README.md` com imagens, funcionalidades e instruções de execução

### Alterado
- Atualização visual e técnica do `README.md` para fins de portfólio


## [v1.1.0] - 2025-05-27 *****************

### Adicionado
- Botão de logout no cabeçalho dos módulos posicionado acima dos links de navegação
- Rota `/logout` no `app.py` para limpar a sessão e redirecionar para a tela de login
- Imagem `logout.png` no diretório `assets/` usada como ícone do botão de logout
- Criação do arquivo `ldap_auth.py` para configurar a autenticação de login
- Criação do arquivo `.env` com os acessos para configurar o acesso com o AD

### Alterado
- `callbacks_inicial.py`: callback unificado para login e logout, evitando conflito de múltiplos `Output("url", "pathname")`
- `layout.py` do módulo `menu_saldo_contrato`: reposicionamento do ícone de logout para topo-direita (com `top` e `left` via CSS)
- `layout_inicial.py`: ajuste no `login-message` para mostrar mensagem ao voltar do logout e outras alterações
- `app.py`: alterado para rodar com o gunicorn
- `app.py`: tratamento da rota `/logout` diretamente na função `display_page`, com `session.clear()` e redirecionamento
- `callbacks.py`: Ajuste no callbacks do menuna_mapa_controle. Ajustando a variável global para melhor aplicabilidade de Escalabilidade
- `request.py`: Ajuste do request para conexão com a view atualizada

### Corrigido
- Comportamento ao clicar em logout que deixava a página incompleta — agora forçado `refresh=True` no `dcc.Link` para recarregar completamente
- Estilo do botão de logout reposicionado corretamente sem aumentar a altura do cabeçalho
