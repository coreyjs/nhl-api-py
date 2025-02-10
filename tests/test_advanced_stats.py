"""
test_advanced_stats.py

This module contains unit and integration tests for advanced_stats.py.
It uses pytest-asyncio to test asynchronous code and mocks the websocket connection
to simulate responses from the NHL edge site.
"""

import asyncio
import json
import pytest
from aiohttp import WSMsgType
from unittest.mock import patch
from contextlib import asynccontextmanager

from nhlpy.api.advanced_stats import AdvancedStats, AdvancedStatsConfig


# A fake websocket class that simulates sending and receiving messages.
class FakeWebSocket:
    def __init__(self, messages):
        self.messages = messages
        self.index = 0

    async def send_json(self, message):
        # Log the message being sent in tests if needed.
        print("Fake send_json called with:", message)

    async def receive(self):
        if self.index < len(self.messages):
            msg = self.messages[self.index]
            self.index += 1
            return msg
        # When no more messages, simulate a timeout to exit the loop.
        await asyncio.sleep(0.1)
        raise asyncio.TimeoutError()

    async def close(self):
        pass


# A simple fake WS message to simulate websocket messages.
class FakeWSMessage:
    def __init__(self, msg_type, data):
        self.type = msg_type
        self.data = data


@pytest.fixture
def fake_ws_messages():
    # Prepare a list of fake websocket messages.
    messages = [
        FakeWSMessage(WSMsgType.TEXT, json.dumps({"response": "initial_handshake_ack"})),
        FakeWSMessage(WSMsgType.TEXT, json.dumps({"response": "subsequent_message_ack"}))
    ]
    return messages


# A custom async context manager that wraps a fake websocket.
class FakeWSContextManager:
    def __init__(self, ws):
        self.ws = ws

    async def __aenter__(self):
        return self.ws

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.mark.asyncio
async def test_connect_and_listen(fake_ws_messages):
    """
    Test the connect_and_listen method of AdvancedStats by patching
    aiohttp.ClientSession.ws_connect to return a fake websocket wrapped in our
    FakeWSContextManager.
    """
    # Create a fake websocket instance using the fixture messages.
    fake_ws = FakeWebSocket(fake_ws_messages)

    # Patch ws_connect to return our FakeWSContextManager with the fake websocket.
    with patch('aiohttp.ClientSession.ws_connect', new=lambda *args, **kwargs: FakeWSContextManager(fake_ws)):
        config = AdvancedStatsConfig(player_id="8478439")
        adv_stats = AdvancedStats(config)
        messages = await adv_stats.connect_and_listen()

        # Verify that two messages were received.
        assert len(messages) == 2
        # Verify the content of the first message.
        assert messages[0].get("response") == "initial_handshake_ack"
        # Verify the content of the second message.
        assert messages[1].get("response") == "subsequent_message_ack"