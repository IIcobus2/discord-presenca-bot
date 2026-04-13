from formatting import format_success, format_already_registered, format_wrong_channel

CHANNEL_IDS = {
    'agenda_semanal': '1493049627551862784',
    'agenda_mensal': '1493049739170808000',
    'pendencias': '1493053855842435163',
}


def test_format_wrong_channel():
    msg = format_wrong_channel()
    assert 'presenca' in msg.lower() or '#' in msg


def test_format_already_registered():
    msg = format_already_registered('09:30', '13/04/2026')
    assert '09:30' in msg
    assert '13/04/2026' in msg


def test_format_success_contains_registration():
    history = [
        {'data': '01/04/2026', 'horario': '09:00'},
        {'data': '13/04/2026', 'horario': '14:32'},
    ]
    msg = format_success('14:32', '13/04/2026', 'Abril/2026', history, CHANNEL_IDS)
    assert '14:32' in msg
    assert '13/04/2026' in msg


def test_format_success_contains_history():
    history = [
        {'data': '01/04/2026', 'horario': '09:00'},
        {'data': '13/04/2026', 'horario': '14:32'},
    ]
    msg = format_success('14:32', '13/04/2026', 'Abril/2026', history, CHANNEL_IDS)
    assert '01/04/2026' in msg
    assert '09:00' in msg
    assert 'Total: 2' in msg


def test_format_success_contains_channel_links():
    history = [{'data': '13/04/2026', 'horario': '14:32'}]
    msg = format_success('14:32', '13/04/2026', 'Abril/2026', history, CHANNEL_IDS)
    assert '<#1493049627551862784>' in msg
    assert '<#1493049739170808000>' in msg
    assert '<#1493053855842435163>' in msg


def test_format_success_singular_presenca():
    history = [{'data': '13/04/2026', 'horario': '14:32'}]
    msg = format_success('14:32', '13/04/2026', 'Abril/2026', history, CHANNEL_IDS)
    assert 'Total: 1 presença' in msg


def test_format_success_plural_presencas():
    history = [
        {'data': '01/04/2026', 'horario': '09:00'},
        {'data': '13/04/2026', 'horario': '14:32'},
    ]
    msg = format_success('14:32', '13/04/2026', 'Abril/2026', history, CHANNEL_IDS)
    assert 'Total: 2 presenças' in msg
