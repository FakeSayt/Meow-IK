# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:47:46 2026

@author: theve
"""

# mage_info.py
import discord
from discord.ext import commands
from discord import app_commands

# Import statystyk z mage_stats.py
from mage_stats import MAGE_STATS

class MageInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mage_info", description="Shows detailed info about a mage")
    @app_commands.describe(name="Mage name (e.g., merlin, himiko)")
    async def mage_info(self, interaction: discord.Interaction, name: str):
        name = name.lower()
        if name not in MAGE_STATS:
            await interaction.response.send_message(f"Mage not found: `{name}` ❌", ephemeral=True)
            return

        mage = MAGE_STATS[name]
        embed = discord.Embed(title=f"Mage Info: {name.title()}", color=discord.Color.teal())
        embed.add_field(name="Element", value=mage["element"], inline=True)
        embed.add_field(name="DPS", value=mage["dps"], inline=True)
        embed.add_field(name="Single Target", value=mage["single_target"], inline=True)
        embed.add_field(name="Four Target", value=mage["four_target"], inline=True)
        embed.add_field(name="Energy Regen", value=mage["energy_regen"], inline=True)
        embed.add_field(name="Skill per Second", value=mage["skill_per_sec"], inline=True)
        embed.add_field(name="Special", value=mage["special"], inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MageInfo(bot))
