# TODO: Create a link generator that provides order and sort-by options
import discord
from discord.ext import commands
import asyncio
import json
import requests

TOKEN = 'ACCESS TOKEN HERE'
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('!search'):
        query = message.content[8:]
        await client.send_message(channel, '**StackOverflow Query:** \'' + query + "\'\n")

        link = "https://api.stackexchange.com/2.2/search/advanced?order=desc&" + \
                "sort=relevance&q=" + query + "&site=stackoverflow"

        r = requests.get(link)
        data = json.loads(r.text)

        bot_response = ""

        if data['items']:
            for i in range(5):
                bot_response += "**" + str(i+1) + ". " + data['items'][i]['title'] + ":**\n"
                bot_response += "**Link:** <" + data['items'][i]['link'] + ">" + "\n\n"

            await client.send_message(channel, bot_response)
        else:
            bot_response += "No topics found."
            await client.send_message(channel, bot_response)

        print("Queries remaining: " + str(data['quota_remaining']))

client.run(TOKEN)
