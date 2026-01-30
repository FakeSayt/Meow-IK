# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 17:01:49 2026

@author: theve
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}  # user_id -> list of (message, seconds)
        self.check_reminders.start()

    @tasks.loop(seconds=5)
    async def check_reminders(self):
        to_remove = []
        for user_id, reminder_list in self.reminders.items():
            for i, (msg, timestamp) in enumerate(reminder_list):
                if timestamp <= asyncio.get_event_loop().time():
                    user = self.bot.get_user(user_id)
                    if user:
                        try:
                            await user.send(f"⏰ Reminder: {msg}")
                        except:
                            pass
                    to_remove.append((user_id, i))
        # Remove triggered reminders
        for user_id, i in reversed(to_remove):
            self.reminders[user_id].pop(i)
            if not self.reminders[user_id]:
                del self.reminders[user_id]

    @app_commands.command(
        name="reminder",
        description="Set a reminder in seconds"
    )
    @app_commands.describe(seconds="Time until reminder (in seconds)", message="Reminder message")
    async def reminder(self, interaction: discord.Interaction, seconds: int, message: str):
        user_id = interaction.user.id
        if user_id not in self.reminders:
            self.reminders[user_id] = []
        self.reminders[user_id].append((message, asyncio.get_event_loop().time() + seconds))
        await interaction.response.send_message(f"✅ Reminder set in {seconds} seconds: {message}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Reminder(bot))
