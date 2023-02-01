import pytest
import pytest_asyncio
import discord.ext.test as dpytest
import cogs.general

@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("av!ping")
    assert dpytest.verify().message().contains().content("Pong!")