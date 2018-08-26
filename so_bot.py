import discord
from discord.ext import commands
import asyncio
import json
import requests

consumer_key = input('StackApps consumer key: ')
stackapps_token = input('StackApps access token: ')
discordbot_token = input('Discord Bot Token: ')

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
        context_sortby = ['-s activity', '-s votes', '-s creation', '-s relevance']
        context_orderby = ['-o asc', '-o desc']
        flags = []

        # search for flags in message
        for flag in context_sortby:
            if flag in message.content:
                flags.append(flag[3:])

        for flag in context_orderby:
            if flag in message.content:
                flags.append(flag[3:])

        # process the query from message
        query = message.content[8:]
        for flag in flags:
            query = query.replace('-o ' + flag, "")
            query = query.replace('-s ' + flag, "")
        query = query.strip()   # remove leading/trailing spaces

        link = link_gen(query, flags)   # generate link

        await client.send_message(channel, '**StackOverflow Query:** \'' + query + "\'\n")

        # grab data from stackexchange api
        r = requests.get(link, params={'key': consumer_key, 'access_token': stackapps_token})
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
    
    elif message.content.startswith('!help'):
        help_message = "**USAGE:**\t'!search [flags] [search string]'\n"
        help_message += "**FLAGS:**\t-o  -s\n"
        help_message += "**FLAG OPTIONS:**\n\t\t-o [asc, desc]\n"
        help_message += "\t\t-s [activity, votes, creation, relevance]\n"

        await client.send_message(channel, help_message)


# Generate a link to request from StackExchange API
def link_gen(query, flags):
    sort_by = 'relevance'   # Default values if no flags are given
    order_by = 'desc'
    link = ""

    if len(flags) > 1:
        sort_by = flags[0]
        order_by = flags[1]
        link = "https://api.stackexchange.com/2.2/search/advanced?order=" + \
                order_by + "&sort=" + sort_by + "&q=" + query + \
                "&site=stackoverflow"
    elif len(flags) == 1:
        sort_by = flags[0]
        link = "https://api.stackexchange.com/2.2/search/advanced?order=desc&" + \
                "sort=" + sort_by + "&q=" + query + "&site=stackoverflow"
    else:
        link = "https://api.stackexchange.com/2.2/search/advanced?order=" + \
                order_by + "&sort=" + sort_by + "&q=" + query + \
                "&site=stackoverflow"

    return link

client.run(discordbot_token)
