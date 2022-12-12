import discord
from main import *


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        embeds = message.embeds # return list of embeds
        for embed in embeds:
            if embed.to_dict()['author']['name'] == 'NOVA RODADA!':
                await message.channel.send(main(embed.to_dict()['description'].replace('`', '')))
            
client = MyClient()
client.run('Your token')