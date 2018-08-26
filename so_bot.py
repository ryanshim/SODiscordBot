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
    print('Logged in as:', client.user.name)
    print('UserID:', client.user.id)
    print('------')

@client.event
async def on_message(message):
    channel = message.channel

    if message.content.startswith('!search'):
        flags = get_flags(message.content)  # extract flags

        query = get_query(message.content, flags) # extract actual search string

        link = link_gen(query, flags)   # generate link

        await client.send_message(channel, '**StackOverflow Query:** \'' + query + "\'\n")

        # grab data from stackexchange api
        r = requests.get(link, params={'key': consumer_key, 'access_token': stackapps_token})
        data = json.loads(r.text)

        bot_response = ""

        if 'items' in data:
            if len(data['items']) > 0:
                for i in range(5):
                    bot_response += "**" + str(i+1) + ". " + data['items'][i]['title'] + ":**\n"
                    bot_response += "**Link:** <" + data['items'][i]['link'] + ">" + "\n\n"
                await client.send_message(channel, bot_response)
            else:
                bot_response += "No topics found."
                await client.send_message(channel, bot_response)

            print("Queries remaining: " + str(data['quota_remaining']))

        elif 'error_message' in data:
            bot_response += "Error retrieving data from StackExchange API.\n"
            bot_response += "Reason: " + data['error_message']
            print(data['error_message'])
            await client.send_message(channel, bot_response)

    elif message.content.startswith('!help'):
        help_message = "**USAGE:**\t'!search [flags] [search string]'\n" + \
                "**FLAGS:**\t-o  -s\n**FLAG OPTIONS:**\n\t\t-o [asc, desc]\n" + \
                "\t\t-s [activity, votes, creation, relevance]\n"

        await client.send_message(channel, help_message)

# Extracts the search string from the message
def get_query(raw_message, flags):
    query = raw_message[8:]

    for flag in flags:
        query = query.replace('-o ' + flag, "")
        query = query.replace('-s ' + flag, "")
    query = query.strip()   # remove leading/trailing spaces

    return query

# Parses message for flags
def get_flags(raw_message):
    context_sortby = ['-s activity', '-s votes', '-s creation', '-s relevance']
    context_orderby = ['-o asc', '-o desc']
    flags = []

    # search for flags in message
    for flag in context_sortby:
        if flag in raw_message:
            flags.append(flag[3:])
    for flag in context_orderby:
        if flag in raw_message:
            flags.append(flag[3:])

    return flags

# Generate a link to request from StackExchange API
def link_gen(query, flags):
    sort_by = 'relevance'   # Default values if no flags are given
    order_by = 'desc'
    link = ""

    if len(flags) > 1:
        sort_by = flags[0]
        order_by = flags[1]
    elif len(flags) == 1:
        sort_by = flags[0]

    link = "https://api.stackexchange.com/2.2/search/advanced?order=" + \
            order_by + "&sort=" + sort_by + "&q=" + query + \
            "&site=stackoverflow"

    return link

client.run(discordbot_token)
