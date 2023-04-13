import discord
import requests
from config import TOKEN
import logging
import socket
socket.getaddrinfo('localhost', 8080)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    def parse_options(self, data):
        options = []
        # Parse data to get prices and delivery times
        # Add data to array
        return options


    async def on_message(self, message):
        if message.author == client.user:
            return
        if 'delivery' in message.content.lower():
            delivery_options = []
            # Get data from the Russian post, sdek, boxberry, PEC
            russianpost_data = requests.get('https://russianpost.api.com/options')
            sdek_data = requests.get('https://sdek.api.com/options')
            boxberry_data = requests.get('https://boxberry.api.com/options')
            pec_data = requests.get('https://pec.api.com/options')
            # Parse data to get prices and delivery times
            russianpost_delivery_options = self.parse_options(russianpost_data)
            sdek_delivery_options = self.parse_options(sdek_data)
            boxberry_delivery_options = self.parse_options(boxberry_data)
            pec_delivery_options = self.parse_options(pec_data)
            # Append data to array
            delivery_options.extend(russianpost_delivery_options)
            delivery_options.extend(sdek_delivery_options)
            delivery_options.extend(boxberry_delivery_options)
            delivery_options.extend(pec_delivery_options)
            # Sort delivery options
            delivery_options = sorted(delivery_options, key=lambda t: t[1])
            # Build response message
            response = 'I can offer you the following delivery options:n'
            for option in delivery_options:
                response += f'{option[0]}: {option[1]} RUB; Delivery time: {option[2]} daysn'
            await message.channel.send(response)



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(TOKEN)