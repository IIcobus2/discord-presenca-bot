import os

import discord
from discord import app_commands
from dotenv import load_dotenv

import sheets
import formatting

load_dotenv()

PRESENCA_CHANNEL_ID = int(os.environ['PRESENCA_CHANNEL_ID'])
CHANNEL_IDS = {
    'agenda_semanal': os.environ['AGENDA_SEMANAL_ID'],
    'agenda_mensal': os.environ['AGENDA_MENSAL_ID'],
    'pendencias': os.environ['PENDENCIAS_ID'],
}

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name='presenca', description='Registrar sua presença')
async def presenca(interaction: discord.Interaction):
    if interaction.channel_id != PRESENCA_CHANNEL_ID:
        await interaction.response.send_message(
            formatting.format_wrong_channel(), ephemeral=True
        )
        return

    await interaction.response.defer()

    try:
        sheet = sheets.get_sheet()
    except Exception:
        await interaction.followup.send(
            '❌ Não foi possível conectar ao Google Sheets. Tente novamente mais tarde.'
        )
        return

    user_id = str(interaction.user.id)
    username = str(interaction.user)

    registered, horario = sheets.already_registered_today(sheet, user_id)
    if registered:
        from datetime import datetime
        import pytz
        tz = pytz.timezone(os.environ.get('TIMEZONE', 'America/Sao_Paulo'))
        today = datetime.now(tz).strftime('%d/%m/%Y')
        await interaction.followup.send(
            formatting.format_already_registered(horario, today), ephemeral=True
        )
        return

    now = sheets.register_presence(sheet, user_id, username)
    history = sheets.get_monthly_history(sheet, user_id)

    data = now.strftime('%d/%m/%Y')
    horario = now.strftime('%H:%M')
    mes_ano = now.strftime('%m/%Y')
    mes_label = formatting.month_label(mes_ano)

    await interaction.followup.send(
        formatting.format_success(horario, data, mes_label, history, CHANNEL_IDS)
    )


@client.event
async def on_ready():
    await tree.sync()
    print(f'Bot online como {client.user}')


client.run(os.environ['DISCORD_TOKEN'])
