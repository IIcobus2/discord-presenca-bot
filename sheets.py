import json
import os
from datetime import datetime

import gspread
import pytz

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]


def get_sheet():
    raw = os.environ.get('GOOGLE_CREDENTIALS', '')
    if not raw or raw.strip() == '{}':
        raise RuntimeError(
            "GOOGLE_CREDENTIALS environment variable is not set or is empty. "
            "Set it to the JSON content of your Google Service Account key file."
        )
    creds_json = json.loads(raw)
    client = gspread.service_account_from_dict(creds_json, scopes=SCOPES)
    spreadsheet = client.open_by_key(os.environ['SPREADSHEET_ID'])
    return spreadsheet.worksheet('Presenças')


def _now():
    tz = pytz.timezone(os.environ.get('TIMEZONE', 'America/Sao_Paulo'))
    return datetime.now(tz)


def already_registered_today(sheet, user_id: str):
    """Retorna (True, 'HH:MM', 'DD/MM/YYYY') se já registrou hoje, senão (False, None, 'DD/MM/YYYY')."""
    today = _now().strftime('%d/%m/%Y')
    records = sheet.get_all_records(value_render_option='FORMATTED_VALUE')
    for row in records:
        if str(row['user_id']) == str(user_id) and row['data'] == today:
            return True, row['horario'], today
    return False, None, today


def register_presence(sheet, user_id: str, username: str):
    """Grava nova linha de presença e retorna o datetime do registro."""
    now = _now()
    sheet.append_row([
        str(user_id),
        username,
        now.strftime('%d/%m/%Y'),
        now.strftime('%H:%M'),
        now.strftime('%m/%Y'),
    ])
    return now


def get_monthly_history(sheet, user_id: str):
    """Retorna lista de {'data', 'horario'} do usuário no mês atual."""
    mes_ano = _now().strftime('%m/%Y')
    records = sheet.get_all_records(value_render_option='FORMATTED_VALUE')
    return [
        {'data': r['data'], 'horario': r['horario']}
        for r in records
        if str(r['user_id']) == str(user_id) and r['mes_ano'] == mes_ano
    ]
