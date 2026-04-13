MONTH_NAMES = {
    '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
    '04': 'Abril', '05': 'Maio', '06': 'Junho',
    '07': 'Julho', '08': 'Agosto', '09': 'Setembro',
    '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro',
}


def format_wrong_channel() -> str:
    return "⚠️ Este comando só funciona no canal **#presenca**."


def format_already_registered(horario: str, data: str) -> str:
    return f"⚠️ Você já registrou presença hoje! ({data} às {horario})"


def format_success(
    horario: str,
    data: str,
    mes_label: str,
    history: list,
    channel_ids: dict,
) -> str:
    lines = [
        "✅ Presença registrada!",
        f"📅 {data} às {horario}",
        "",
        f"📊 Seu histórico em {mes_label}:",
    ]
    for entry in history:
        lines.append(f"  • {entry['data']} — {entry['horario']}")
    total = len(history)
    word = "presença" if total == 1 else "presenças"
    lines.append(f"Total: {total} {word} este mês")
    lines.append("")
    lines.append("📌 Antes de sair, verifique os canais:")
    semanal = channel_ids['agenda_semanal']
    mensal = channel_ids['agenda_mensal']
    pendencias = channel_ids['pendencias']
    lines.append(f"<#{semanal}> • <#{mensal}> • <#{pendencias}>")
    lines.append("para se manter atualizado(a) sobre a empresa!")
    return "\n".join(lines)


def month_label(mes_ano: str) -> str:
    """Converte '04/2026' em 'Abril/2026'."""
    month, year = mes_ano.split('/')
    return f"{MONTH_NAMES[month]}/{year}"
