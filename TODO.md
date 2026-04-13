# TODO

A lista abaixo cobre apenas correções, refactors, testes, documentação, segurança e performance do estado atual do repositório.

## P1 — Alta prioridade

### S
- [ ] Corrigir a inconsistência entre `Procfile` e o código atual: o arquivo referencia `bot.py`, mas `bot.py` não existe.
- [ ] Adicionar testes para falhas de configuração em `sheets.py`, incluindo ausência de `GOOGLE_CREDENTIALS` e `SPREADSHEET_ID`.
- [ ] Adicionar testes para limites de data/fuso horário em `already_registered_today` e `get_monthly_history`.

### M
- [ ] Revisar o custo de `sheet.get_all_records()` em cada operação e documentar o limite operacional esperado da aba `Presenças`.

## P2 — Média prioridade

### S
- [ ] Documentar explicitamente no fluxo de desenvolvimento que a spec do produto está à frente da implementação atual.
- [ ] Cobrir com testes o comportamento quando a aba `Presenças` não existe ou retorna colunas inesperadas.

### M
- [ ] Verificar se o escopo `https://www.googleapis.com/auth/drive` é realmente necessário; remover se o acesso à planilha funcionar apenas com privilégio mínimo.
- [ ] Revisar se o formato de `GOOGLE_CREDENTIALS` em variável única precisa de orientação adicional de escaping no README.

## P3 — Baixa prioridade

### S
- [ ] Padronizar critérios de evidência de QA para cada nova funcionalidade adicionada ao repositório.

### M
- [ ] Avaliar uma estratégia de testes de integração controlados para a camada Google Sheets sem depender de credenciais reais em CI.
