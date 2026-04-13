# DiscordBot

Bot de presença para Discord em desenvolvimento.

## Status atual

O repositório ainda está em fase inicial. No momento, a implementação existente cobre apenas a camada de persistência em Google Sheets para registros de presença.

Implementado hoje:
- helpers de integração com Google Sheets em `sheets.py`
- testes unitários dessa camada em `tests/test_sheets.py`
- definição funcional do produto em `docs/superpowers/specs/2026-04-13-presenca-bot-design.md`

Ainda não implementado neste repositório:
- `bot.py`
- comando `/presenca`
- validação de canal do Discord
- resposta pública/ephemeral no Discord
- deploy funcional via `Procfile`

## Arquitetura atual

### `sheets.py`
Responsável por:
- abrir a aba `Presenças` da planilha configurada
- verificar se um usuário já registrou presença no dia atual
- registrar uma nova presença
- retornar o histórico mensal do usuário

### `tests/test_sheets.py`
Cobre os principais cenários da camada atual:
- presença já registrada no dia
- ausência de registro
- filtro por usuário
- gravação de nova linha
- retorno de histórico mensal

## Requisitos

- Python 3.11+
- acesso a uma planilha Google Sheets com aba `Presenças`
- credenciais de service account válidas

## Dependências

Listadas em `requirements.txt`:
- `discord.py==2.3.2`
- `gspread==6.1.2`
- `google-auth==2.29.0`
- `python-dotenv==1.0.1`
- `pytz==2024.1`
- `pytest==8.2.0`

## Variáveis de ambiente

Exemplo em `.env.example`:

```env
DISCORD_TOKEN=seu_token_aqui
GOOGLE_CREDENTIALS={"type":"service_account",...}
SPREADSHEET_ID=id_da_planilha_aqui
PRESENCA_CHANNEL_ID=id_do_canal_presenca
AGENDA_SEMANAL_ID=1493049627551862784
AGENDA_MENSAL_ID=1493049739170808000
PENDENCIAS_ID=1493053855842435163
TIMEZONE=America/Sao_Paulo
```

## Estrutura do projeto

```text
DiscordBot/
├── .env.example
├── Procfile
├── README.md
├── PLANNING.md
├── TODO.md
├── sheets.py
├── requirements.txt
├── docs/
│   └── superpowers/
│       └── specs/
└── tests/
    └── test_sheets.py
```

## Configuração local

1. Crie um ambiente virtual Python.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente.
4. Garanta que a planilha tenha uma aba chamada `Presenças` com colunas compatíveis com:
   - `user_id`
   - `username`
   - `data`
   - `horario`
   - `mes_ano`

## Como rodar os testes

```bash
pytest -q
```

## Uso atual

A interface utilizável hoje é programática, via `sheets.py`.

Exemplo:

```python
import sheets

sheet = sheets.get_sheet()
registered, horario = sheets.already_registered_today(sheet, "123")

if not registered:
    sheets.register_presence(sheet, "123", "Ana")

history = sheets.get_monthly_history(sheet, "123")
```

## Deploy

O `Procfile` aponta para `python bot.py`, mas `bot.py` ainda não existe neste repositório.

Na prática, o deploy automático ainda não está pronto para produção até que a camada do bot seja implementada e validada.

## Troubleshooting

### `KeyError` em variáveis de ambiente
Verifique se `GOOGLE_CREDENTIALS`, `SPREADSHEET_ID` e `TIMEZONE` estão definidos conforme necessário.

### Falha ao acessar a planilha
Confirme se:
- o `SPREADSHEET_ID` está correto
- a service account tem acesso à planilha
- a aba `Presenças` existe com o nome exato

### Testes passam, mas o bot não roda
Isso é esperado no estado atual do repositório, porque a camada Discord ainda não foi implementada.
