import json
import os
from datetime import datetime

import gspread
import pytz
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]


def get_sheet():
    creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(os.environ['SPREADSHEET_ID'])
    return spreadsheet.worksheet('Presenças')


def _now():
    tz = pytz.timezone(os.environ.get('TIMEZONE', 'America/Sao_Paulo'))
    return datetime.now(tz)


def already_registered_today(sheet, user_id: str):
    """Retorna (True, 'HH:MM') se já registrou hoje, senão (False, None)."""
    today = _now().strftime('%d/%m/%Y')
    for row in sheet.get_all_records():
        if str(row['user_id']) == str(user_id) and row['data'] == today:
            return True, row['horario']
    return False, None


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
    return [
        {'data': r['data'], 'horario': r['horario']}
        for r in sheet.get_all_records()
        if str(r['user_id']) == str(user_id) and r['mes_ano'] == mes_ano
    ]
