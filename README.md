# Food Flex Discord Bot

<p align="center">
  <img src="https://cdn.discordapp.com/attachments/501947007653511172/572491463112523780/unknown.png">
</p>

## What does the bot do?
Food Flex is bot that manages:
- Submissions
- Voting
- Results
- Leaderboard

### Submissions (13:00 - 23:59)
When a user uploads a picture of their food to the chat, they are automatically entered into the vote. Users can only submit once. The bot will won't count additional submission pictures, therefore users who may feel that multiple pictures helps show off their 'flexing', are able to post multiple pictures without error.

### Voting (00:00 - 11:59)
Submissions are closed and a voting poll is displayed. Users can vote for their favourite by sending the letter that corresponds to the user. Users can only vote once, and not for themselves. The bot will won't count additional votes. Also, anyone who submitted, and hasn't voted by 11:00, will received a private message to remind them to vote. You will receive a private message to confirm your vote.

**NOTE:** If you submit a picture and don't vote, you are disqualified.

### Results (12:00)
Voting is closed and a results message will be sent to the chat.

### Leaderboard
This is a read-only channel that updates every day once there are new results. This shows the overall scores over a period of time. This can be a month, university term, or a year.

## Docs
See the wiki for documentation on commands, json data and more.

## Installation
##### Clone latest release
```bash
$ git clone https://github.com/wrussell1999/food-flex-discord
$ cd food-flex-discord
```

#### Setup venv & Install dependencies
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

### Configuration
You need to create the file `config/config.json` give it the following structure:
```python
{
  "token": str,
  "server_id": int,
  "command_prefix":str,
  "admin_ids": [ints],
  "main_channel_id": int,
  "leaderboard_channel_id": int
}
```

###### Meaning of each key
- **token** - your bot's secret token
- **server_id** - the ID of your server
- **command_prefix** - a prefix that marks the message as a command for the bot (you may need a space at the end)
- **admin_ids** - a list of user IDs that will be allowed to use bot commands
- **main_channel_id** - the ID of the channel to use for submissions, voting and results
- **leaderboard_channel_id** - the ID of the channel to use for the leaderboard

###### Getting a token
[This guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) will show you how to create a Discord Bot for your Discord server.

###### Getting IDs
Go to Discord and turn on Developer Mode. With this, you can now right-click on guilds, channels, catergories, users, messages, etc. and get their ID (an integer).

### Run the bot
```bash
$ python3 -m foodflex
```

## Contributors
- [Will Russell](https://www.github.com/wrussell1999): Submissions, voting, results, leaderboard, working with the discord.py API wrapper and Discord servers.
- [Daniel Spencer](https://www.github.com/danielfspencer): Voting validation, improved reliability, general refactoring, and performance improvements with dictionaries.

## License
MIT License for all the code written by Will and Dan.
