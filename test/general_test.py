import pytest
import pytest_asyncio
import discord.ext.test as dpytest

@pytest.mark.asyncio
async def test_ping(bot):
    await bot.load_extension("cogs.general")    
    dpytest.configure(bot)
    await dpytest.message("av!ping")
    assert dpytest.verify().message().contains().content("Pong!")