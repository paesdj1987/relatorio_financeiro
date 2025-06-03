# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

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
