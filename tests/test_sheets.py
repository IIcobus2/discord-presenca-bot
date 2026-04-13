import os
os.environ['TIMEZONE'] = 'America/Sao_Paulo'
os.environ['GOOGLE_CREDENTIALS'] = '{}'
os.environ['SPREADSHEET_ID'] = 'fake'

from unittest.mock import MagicMock
from datetime import datetime
import pytz
import sheets


def make_sheet(records):
    mock = MagicMock()
    mock.get_all_records.return_value = records
    return mock


def today():
    tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(tz).strftime('%d/%m/%Y')


def mes_ano():
    tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(tz).strftime('%m/%Y')


def test_already_registered_today_true():
    sheet = make_sheet([
        {'user_id': '123', 'username': 'Ana', 'data': today(),
         'horario': '09:00', 'mes_ano': mes_ano()}
    ])
    registered, horario = sheets.already_registered_today(sheet, '123')
    assert registered is True
    assert horario == '09:00'


def test_already_registered_today_false_empty():
    sheet = make_sheet([])
    registered, horario = sheets.already_registered_today(sheet, '123')
    assert registered is False
    assert horario is None


def test_already_registered_today_false_different_user():
    sheet = make_sheet([
        {'user_id': '999', 'username': 'Outro', 'data': today(),
         'horario': '09:00', 'mes_ano': mes_ano()}
    ])
    registered, horario = sheets.already_registered_today(sheet, '123')
    assert registered is False
    assert horario is None


def test_register_presence_appends_row():
    sheet = make_sheet([])
    sheets.register_presence(sheet, '123', 'Ana')
    sheet.append_row.assert_called_once()
    row = sheet.append_row.call_args[0][0]
    assert row[0] == '123'
    assert row[1] == 'Ana'
    assert len(row) == 5  # user_id, username, data, horario, mes_ano


def test_register_presence_returns_datetime():
    sheet = make_sheet([])
    result = sheets.register_presence(sheet, '123', 'Ana')
    assert hasattr(result, 'strftime')


def test_get_monthly_history_filters_by_user_and_month():
    sheet = make_sheet([
        {'user_id': '123', 'username': 'Ana', 'data': '01/04/2026',
         'horario': '09:00', 'mes_ano': mes_ano()},
        {'user_id': '123', 'username': 'Ana', 'data': '07/04/2026',
         'horario': '08:58', 'mes_ano': mes_ano()},
        {'user_id': '999', 'username': 'Outro', 'data': '07/04/2026',
         'horario': '10:00', 'mes_ano': mes_ano()},
    ])
    history = sheets.get_monthly_history(sheet, '123')
    assert len(history) == 2
    assert history[0] == {'data': '01/04/2026', 'horario': '09:00'}
    assert history[1] == {'data': '07/04/2026', 'horario': '08:58'}


def test_get_monthly_history_empty():
    sheet = make_sheet([])
    history = sheets.get_monthly_history(sheet, '123')
    assert history == []
