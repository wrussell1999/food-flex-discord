# Food Flex Discord Bot
Discord Bot for Food Flex created by Will Russell

## What does the bot do?

Food Flex is bot that manages:
- Submissions
- Voting 
- Results

These events happen between certain times.

### Submissions

This happens between 13:00 GMT and 23:59 GMT.

When a user uploads a picture of their food to the submissions chat, they are automatically entered into the vote. 

Users can only vote once. The bot will won't count additional submission pictures, therefore users who may feel that multiple pictures helps show off their 'flexing', are able to post multiple pictures without error.

### Voting

This happens between 00:00 GMT and 11:59 GMT.

Submissions are closed and a voting poll is displayed. Users can vote for their favourite by sending the letter that corresponds to the user. 

Users can only vote once. The bot will won't count additional votes.

### Results

This happens at 12:00 GMT.

Voting is closed and a results message will be sent. 

### Other things to note

- You can't vote for yourself
- If you submit a picture and don't vote, you are disqualified

## Tools

- This was built using the discord API wrapper discord.py in Python.
- The bot on my server is hosted on a remote Raspberry Pi.
- The bot can be accessed via SSH.
- Screen was used to create sessions over SSH, that would remain active when the SSH session disconnects. This means the bot will always be online.

## Development

Clone this repo:

    $ git clone https://github.com/wrussell1999/food-flex-discord
    $ cd food-flex-discord

To install discord.py:

    $ sudo apt install python3-pip
    $ python3 -m pip install -U discord.py

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

    $ python3 main.py


## License
MIT License for all the code written by me