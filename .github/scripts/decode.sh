#!/bin/bash

echo -n "$GC_SA" | base64 -d > bot/credentials.json

cat << EOF > bot/.env
TOKEN=$TOKEN
SERVER_ID=$SERVER_ID
MAIN_CHANNEL_ID=$MAIN_CHANNEL_ID
LEADERBOARD_CHANNEL_ID=$LEADERBOARD_CHANNEL_ID
EOF