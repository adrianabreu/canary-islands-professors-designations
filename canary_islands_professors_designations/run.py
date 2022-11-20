import logging
import os
import re
from io import BytesIO
import asyncio

from datetime import datetime 
import requests
import PyPDF2
from telegram import Bot


def get_file(date: str):
    return requests.get(f'https://www.gobiernodecanarias.org/educacion/DGPer/NombraDiarios/Docs/NDS{date}.PDF')

def parse_pdf(stream):
    pdfreader=PyPDF2.PdfFileReader(BytesIO(stream))
    x=pdfreader.numPages
    i = 0
    valid_designations = {}
    while i < x:
        pageobj=pdfreader.getPage(i)
        text=pageobj.extractText()
        designations = text.split('\n \n')

    for call in designations:
        if 'Biología' in call:
            island = re.search("Isla: ([A-Za-z\s]+) Horas", call).group(1)
            if island in valid_designations:
                valid_designations[island] += 1
            else:
                valid_designations[island] = 1
    i+=1
    return valid_designations

def format_message(valid_designations):
    DEFAULT_MESSAGE = 'Hoy no han habido llamamientos para biologia'
    if not bool(valid_designations):
        return DEFAULT_MESSAGE
    
    message = 'Los llamamientos de biologia para hoy son: \n'
    for key in valid_designations:
        message += f'{key}: {valid_designations[key]}\n'
    
    return message
   


async def send(message: str, bot_token: str, group_id: str):
    async with Bot(bot_token) as bot:
        await bot.send_message(group_id, message)

def main():
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    GROUP_ID = os.getenv('GROUP_ID')
    today = datetime.utcnow().strftime("%d-%m-%y")

    response = get_file(today)
    logging.info('Downloading file... ' + str(response.status_code))
    message = 'No hay llamamientos publicados para hoy'

    if response.status_code == 200:
        valid_designations = parse_pdf(response.content)
        message = format_message(valid_designations)
    
    asyncio.run(send(message, BOT_TOKEN, GROUP_ID))