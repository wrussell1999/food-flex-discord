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

When a user uploads a picture of their food to the submissions chat, they are automatically entered into the vote. Users can only vote once. The bot will won't count additional submission pictures, therefore users who may feel that multiple pictures helps show off their 'flexing', are able to post multiple pictures without error.

### Voting (00:00 - 11:59)

Submissions are closed and a voting poll is displayed. Users can vote for their favourite by sending the letter that corresponds to the user. Users can only vote once, and not for themselves. The bot will won't count additional votes. Also, anyone who submitted, and hasn't voted by 11:00, will received a private message to remind them to vote.

### Results (12:00)

Voting is closed and a results message will be sent. 

**NOTE:** If you submit a picture and don't vote, you are disqualified.

## Docs

See the wiki for documentation on commands, json data and more.

## Tools

- This was built using the discord API wrapper discord.py in Python.
- The bot on my server is hosted on a remote Raspberry Pi.
- The bot can be accessed via SSH.
- Screen was used to create sessions over SSH, that would remain active when the SSH session disconnects. This means the bot will always be online.

## Development

Clone this repo:
```bash
$ git clone https://github.com/wrussell1999/food-flex-discord
$ cd food-flex-discord
$ python3 -m venv .venv
$ source .venv/bin/activate
```

To install discord.py:
```bash
$ sudo apt install python3-pip
$ python3 -m pip install -U discord.py
```

`config.json` inside the config directory:
```json
{
    "token_id": "Token as string",
    "server_id": int,
    "food_chat_id": int,
    "submission_channel_id": int,
    "voting_channel_id": int,
    "results_channel_id": int,
    "dev_channel_id": int,
    "admin_id": int
}
```

To run the bot: 

    $ python3 -m foodflex

<a href="https://discordbots.org/bot/502391189270560773" >
  <img src="https://discordbots.org/api/widget/502391189270560773.svg" alt="Food Flex Judge" />
</a>

## License
MIT License for all the code written by me.
