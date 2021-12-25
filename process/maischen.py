import asyncio
import json
from json.decoder import JSONDecoder
import logging


async def send_status(users):
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = "json.dumps(recipe)"
        await asyncio.wait([user.send(message) for user in USERS])
