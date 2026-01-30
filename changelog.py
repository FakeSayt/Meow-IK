# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 19:00:31 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 0.1
        self.changelog = [
            {
                "version": "0.1",
                "date": "30.01.2026",
                "changes": [
                    "Initial release",
                    "Added /addimmortal, /editimmortal, /removeimmortal",
                    "Added /createmarch, /editmarch, /removemarch, /showmarch",
                    "Autocomplete for immortals and marches",
                    "Ability to name marches",
                    "Added /bestartifact command",
                    "Dynamic lists for empty or existing collections"
                ]
            }
        ]

    @app_commands.command(name="changelog", description="Show the bot's changelog and latest updates")
    async def changelog(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📜 Bot Changelog", color=discord.Color.blurple())
        for entry in self.changelog:
            changes_text = "\n".join(f"• {c}" for c in entry["changes"])
            embed.add_field(
                name=f"Version {entry['version']} — {entry['date']}",
                value=changes_text,
                inline=False
            )
        embed.set_footer(text="Fakey")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Changelog(bot))
