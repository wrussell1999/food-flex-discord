# Food Flex Discord Bot [![Discord Bots](https://discordbots.org/api/widget/status/502391189270560773.svg)](https://discordbots.org/bot/502391189270560773)

[Discord Bot](https://discordbots.org/bot/502391189270560773) created by Will Russell
<p align="center">
  <img src="https://cdn.discordapp.com/attachments/501947007653511172/572491463112523780/unknown.png">
</p>

## What does the bot do?
Food Flex is bot that manages:
- Submissions
- Voting 
- Results

### Submissions (13:00 - 23:59)

When a user uploads a picture of their food to the chat, they are automatically entered into the vote. Users can only submit once. The bot will won't count additional submission pictures, therefore users who may feel that multiple pictures helps show off their 'flexing', are able to post multiple pictures without error.

### Voting (00:00 - 11:59)

Submissions are closed and a voting poll is displayed. Users can vote for their favourite by sending the letter that corresponds to the user. Users can only vote once, and not for themselves. The bot will won't count additional votes. Also, anyone who submitted, and hasn't voted by 11:00, will received a private message to remind them to vote. You will receive a private message to confirm your vote.

### Results (12:00)

Voting is closed and a results message will be sent to the chat. 

**NOTE:** If you submit a picture and don't vote, you are disqualified.

## Docs

See the wiki for documentation on commands, json data and more.

## Tools

You may want to use a similar set up for hosting your own Food Flex:

- This was built using the discord API wrapper discord.py in Python.
- The bot on my server is hosted on a remote Raspberry Pi.
- The bot can be accessed via SSH.
- `screen` was used to create sessions over SSH, that would remain active when the SSH session disconnects. This means the bot will always be online.

## Development

### Setup repository
```bash
$ git clone https://github.com/wrussell1999/food-flex-discord
$ cd food-flex-discord
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### Install dependencies
_With virtual environment_
```bash
$ pip3 install -r requirements.txt
```
_Without virtual environment_
```bash
$ sudo apt install python3-pip
$ python3 -m pip install -U discord.py
```

### Create Discord Bot
[This guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) will show you how to create a Discord Bot for your Discord server.

Doing this will allow us to get a token, which we need to add to the `config.json`...


### Config file
`config.json` can be found inside the config directory.

Go to Discord and turn on Developer Mode. With this, you can now right-click on guilds, channels, catergories, users, messages, etc. and get their ID (a snowflake stored as an int for `discord.py`). Use this to get the following IDs needed for `config.json`.

_Note: Token is stored as a string, and IDs (snowflakes) are stored as integers._
```json
{
    "token": "String",
    "admin_id": int,
    "guild_id": int,
    "food_chat_id": int,
    "food_flex_channel_id": int,
    "leaderboard_channel_id": int,
    "leaderboard_message_id": int
}
```

### Run the bot 

    $ python3 -m foodflex

## License
MIT License for all the code written by me.
