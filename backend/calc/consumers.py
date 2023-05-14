import asyncio
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

REFRESH_RATE = 5  # in seconds
RUNTIME = 1  # in minutes


class CalculationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        if text_data == 'start calculation':
            for i in range(RUNTIME * 60 // REFRESH_RATE):
                result = [round(random.random(), 2) for _ in range(106)]
                await self.send(json.dumps(result))
                await asyncio.sleep(REFRESH_RATE)
