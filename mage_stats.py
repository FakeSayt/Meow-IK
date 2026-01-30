# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 16:59:38 2026

@author: Fakey
"""
import discord
from discord.ext import commands
from discord import app_commands

MAGE_STATS = {
    "merlin": {"element": "Water","single_target": 780,"four_target": 3120,"energy_regen": 0.66,"skill_per_sec": 0.72,"dps": 205.92,"special": "Incl. 50% Chill damage buff"},
    "baldwin iv": {"element": "Wind","single_target": 600,"four_target": 2400,"energy_regen": 0.66,"skill_per_sec": 0.71,"dps": 158.40,"special": "Incl. Split 1 75% chance, Split 2 50% chance"},
    "himiko": {"element": "Shadow","single_target": 563,"four_target": 2250,"energy_regen": 0.66,"skill_per_sec": 0.71,"dps": 148.50,"special": "Incl. Shadow affinity amp"},
    "hammurabi": {"element": "Lightning","single_target": 560,"four_target": 2240,"energy_regen": 0.66,"skill_per_sec": 0.71,"dps": 147.84,"special": "Incl. 4 active debuffs (*1.15 per debuff)"},
    "loki": {"element": "Chaos","single_target": 450,"four_target": 1800,"energy_regen": 0.8,"skill_per_sec": 0.81,"dps": 144.00,"special": "Control"},
    "wu": {"element": "Fire","single_target": 600,"four_target": 1306,"energy_regen": 1.0,"skill_per_sec": 1.01,"dps": 130.56,"special": "Incl. 60% chance to hit second up to 3 times"},
    "cleopatra": {"element": "Earth","single_target": 300,"four_target": 1200,"energy_regen": 0.8,"skill_per_sec": 0.89,"dps": 96.00,"special": "Magical damage dealt debuff"},
}

class MageStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats_mage", description="Shows the stats of a mage")
    @app_commands.describe(name="Mage name (e.g., merlin, himiko)")
    async def stats_mage(self, interaction: discord.Interaction, name: str):
        name = name.lower()
        if name not in MAGE_STATS:
            await interaction.response.send_message(f"Mage not found: `{name}` ❌", ephemeral=True)
            return

        mage = MAGE_STATS[name]
        embed = discord.Embed(title=f"Mage Stats: {name.title()}", color=discord.Color.blue())
        embed.add_field(name="Element", value=mage["element"], inline=True)
        embed.add_field(name="DPS", value=mage["dps"], inline=True)
        embed.add_field(name="Single Target", value=mage["single_target"], inline=True)
        embed.add_field(name="Four Target", value=mage["four_target"], inline=True)
        embed.add_field(name="Energy Regen", value=mage["energy_regen"], inline=True)
        embed.add_field(name="Skill per Second", value=mage["skill_per_sec"], inline=True)
        embed.add_field(name="Special", value=mage["special"], inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MageStats(bot))
