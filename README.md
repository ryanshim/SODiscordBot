# SODiscordBot

Quick and dirty Discord bot that searches for StackOverflow posts given a search string.

![screenshot](https://github.com/ryanshim/SODiscordBot/screenshot.png)

#### Dependencies
* discord.py [Python wrapper for the Discord API]
	* `python3 -m pip install -U discord.py`

#### Register a Discord Bot
* Go to the following URL to register your Discord bot:
	* [https://discordapp.com/developers/applications/](https://discordapp.com/developers/applications/)
* Select the 'Bot' section in the menu on the left and select 'Add Bot'
* Select the 'Send Messages' box under Bot Permissions and save the permissions integer.
* To add the bot to your server, copy and paste the bot's `CLIENT ID` and the `permissions integer` in the URL provided below and open it in your browser:
	* `https://discordapp.com/oauth2/authorize?&client_id=CLIENT_ID_HERE&scope=bot&permissions=PERMISSIONS_INTEGER`

#### StackApps Registration and Authentication
* Register your StackApp and enable client side auth flow
* Obtain your access token using the following steps:
	1. Use the following URL with your `client_id` and the chosen `redirect_uri` in your browser:
		* `https://stackoverflow.com/oauth?client_id=CLIENT_ID&scopeno_expiry&redirect_uri=REDIRECT_URI`
		* Note: If you used the default redirect_uri provided by stackexchange, it will most likely be: `https://stackexchange.com/oauth/login_success`
	2. Accept the application permissions.
	3. Copy and save the code given in the URL and run the authentication script.
	4. Copy and save the access token from the response.

#### Run the Bot
* Start the bot script and input the parameters required.
	* `python3 so_bot.py`

#### Usage
* Searches start with the command prefix `!search [flags] [query string]`
* Example: !search python how to concatenate strings
* Example: !search -o asc -s relevance python how to concatenate strings
