# PLANNING

Este planejamento cobre apenas melhorias de documentação, correção, testes, segurança e performance do estado atual do repositório.

## Milestone 1 — Tornar o estado atual explícito e executável

**Objective**
Eliminar inconsistências entre documentação, estrutura e ponto de entrada atual do projeto.

**Tasks**
- Resolver o item `TODO:P1:S` sobre a inconsistência entre `Procfile` e `bot.py`.
- Resolver o item `TODO:P2:S` sobre a diferença entre spec e implementação atual.
- Manter `README.md`, `TODO.md` e `PLANNING.md` alinhados ao código real.

**Acceptance criteria**
- A documentação descreve corretamente o que já existe e o que ainda não existe.
- Não há instrução de execução principal que aponte para arquivo ausente sem aviso explícito.
- Um novo colaborador consegue entender o estado real do repositório sem inferências.

**Risks / rollback**
- Risco: mascarar lacunas reais da implementação com documentação otimista.
- Rollback: restaurar o documento anterior caso alguma descrição passe a divergir do código.

## Milestone 2 — Endurecer a camada `sheets.py`

**Objective**
Aumentar a confiança na camada de planilha cobrindo cenários de falha e fronteiras temporais.

**Tasks**
- Resolver os itens `TODO:P1:S` sobre variáveis de ambiente ausentes.
- Resolver os itens `TODO:P1:S` sobre bordas de data/fuso horário.
- Resolver o item `TODO:P2:S` sobre aba ausente ou colunas inesperadas.

**Acceptance criteria**
- Existem testes automatizados cobrindo cenários felizes e cenários de falha relevantes.
- O comportamento esperado para timezone e duplicidade diária está explícito e validado.
- Erros de configuração deixam de ser pontos cegos na validação.

**Risks / rollback**
- Risco: testes frágeis por depender do horário atual.
- Rollback: reverter apenas o bloco de testes ou a alteração pontual que introduzir instabilidade.

## Milestone 3 — Reduzir risco operacional e de permissão

**Objective**
Revisar custo operacional e escopos de acesso da integração com Google Sheets.

**Tasks**
- Resolver o item `TODO:P1:M` sobre leitura completa da planilha em cada operação.
- Resolver o item `TODO:P2:M` sobre escopo de Drive.
- Resolver o item `TODO:P2:M` sobre orientação de configuração de credenciais.
- Resolver o item `TODO:P3:S` sobre critério de evidência de QA contínuo.

**Acceptance criteria**
- O projeto documenta o impacto esperado de leitura da planilha.
- Os escopos de permissão são os mínimos necessários ou estão justificados.
- O fluxo de QA contínuo possui saída objetiva e repetível.

**Risks / rollback**
- Risco: reduzir permissões e quebrar acesso real à planilha.
- Rollback: restaurar o conjunto anterior de scopes caso a integração deixe de funcionar.
