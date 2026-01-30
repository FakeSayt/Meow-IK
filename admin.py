# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:48:12 2026

@author: theve
"""

# admin.py
import discord
from discord.ext import commands
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {}  # Example: {guild_id: {"reminder_channel": 12345}}

    @app_commands.command(name="settings", description="Configure bot settings for this server")
    @app_commands.describe(channel="Channel for reminders / notifications")
    async def settings(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.settings[interaction.guild_id] = {"reminder_channel": channel.id}
        await interaction.response.send_message(f"✅ Settings updated! Reminders will go to {channel.mention}")

    @app_commands.command(name="update_stats", description="Admin: Update mage stats (temporary)")
    @app_commands.describe(name="Mage name", dps="New DPS value")
    async def update_stats(self, interaction: discord.Interaction, name: str, dps: float):
        from mage_stats import MAGE_STATS
        name = name.lower()
        if name not in MAGE_STATS:
            await interaction.response.send_message(f"Mage `{name}` not found ❌", ephemeral=True)
            return
        MAGE_STATS[name]["dps"] = dps
        await interaction.response.send_message(f"✅ {name.title()}'s DPS updated to {dps}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
