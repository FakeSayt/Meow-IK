# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 19:00:31 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands

CHANGELOG = [
    {
        "version": "0.1",
        "date": "30.01.2026",
        "changes": [
            "Added /addimmortal, /createmarch, /showmarch",
            "Added /bestartifact",
            "Added /changelog"
        ],
        "author": "Fakey <"
    },
    {
        "version": "0.2",
        "date": "30.01.2026",
        "changes": [
            "Persistent storage for /addimmortal and /createmarch using JSON",
            "Added /marchhelp to see all marches from all users",
            "Added creator information to marches"
        ],
        "author": "Fakey <"
    }
]

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="changelog", description="Show the bot's changelog")
    async def changelog(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📜 Bot Changelog", color=discord.Color.blue())
        for entry in CHANGELOG:
            embed.add_field(
                name=f"Version {entry['version']} – {entry['date']}",
                value="\n".join(entry["changes"]) + f"\n**Author:** {entry['author']}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Changelog(bot))

