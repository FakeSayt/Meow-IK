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
        "notes": [
            "Added /addimmortal",
            "Added /createmarch",
            "Added /showmarch",
            "Added /marchhelp",
            "Added persistent storage on Render",
            "Added backup for marches",
            "Initial bot setup by Fakey"
        ]
    }
]

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="changelog", description="Show latest bot updates")
    async def changelog(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📜 Bot Changelog", color=discord.Color.green())
        for update in CHANGELOG:
            notes = "\n".join(f"- {n}" for n in update["notes"])
            embed.add_field(name=f"v{update['version']} ({update['date']})", value=notes, inline=False)
        embed.set_footer(text="Fakey <")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Changelog(bot))

