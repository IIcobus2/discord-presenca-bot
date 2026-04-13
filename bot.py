import os
import time
from datetime import datetime

import discord
from discord import app_commands
from dotenv import load_dotenv
import pytz

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

    user_id = str(interaction.user.id)
    username = str(interaction.user)

    try:
        sheet = sheets.get_sheet()
        registered, horario, today = sheets.already_registered_today(sheet, user_id)
        if registered:
            await interaction.followup.send(
                formatting.format_already_registered(horario, today), ephemeral=True
            )
            return

        now = sheets.register_presence(sheet, user_id, username)
    except Exception as e:
        print(f'[ERROR] Sheets operation failed for user {user_id}: {e}')
        await interaction.followup.send(
            '❌ Não foi possível conectar ao Google Sheets. Tente novamente mais tarde.'
        )
        return

    data = now.strftime('%d/%m/%Y')
    horario_fmt = now.strftime('%H:%M')
    mes_ano = now.strftime('%m/%Y')
    mes_label = formatting.month_label(mes_ano)

    try:
        history = sheets.get_monthly_history(sheet, user_id)
    except Exception as e:
        print(f'[ERROR] get_monthly_history failed for user {user_id}: {e}')
        history = []

    await interaction.followup.send(
        formatting.format_success(horario_fmt, data, mes_label, history, CHANNEL_IDS)
    )


@client.event
async def on_ready():
    if os.environ.get('SYNC_COMMANDS') == '1':
        await tree.sync()
        print('Slash commands sincronizados.')
    print(f'Bot online como {client.user}')


time.sleep(5)  # prevent rapid restart loops from rate-limiting Discord
client.run(os.environ['DISCORD_TOKEN'])
