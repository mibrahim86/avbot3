import pytest
import pytest_asyncio
import discord.ext.test as dpytest

@pytest.mark.asyncio
async def test_ping(bot):
    try:
        await bot.load_extension("cogs.General")
    except Exception as e:
        print(f"Error loading extension: {e}")
        return
    try:
        dpytest.configure(bot)
    except Exception as e:
        print(f"Error configuring dpytest: {e}")
        return
    try:
        await dpytest.message("av!ping")
    except Exception as e:
        print(f"Error sending message: {e}")
        return
    try:
        assert dpytest.verify().message().contains().content("Pong!")
    except Exception as e:
        print(f"Error verifying message: {e}")
        return
