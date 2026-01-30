# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 17:01:36 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands

# Przykładowe strategie bazujące na roli i magach
STRATEGIES = {
    "mage": "Use high DPS mages first, focus on crowd control and energy regeneration.",
    "attack": "Prioritize your strongest physical attackers, apply debuffs early, and chain ultimates efficiently."
}

class Strategy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def role_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=r, value=r) for r in STRATEGIES.keys() if current.lower() in r.lower()]

    @app_commands.command(
        name="strategy",
        description="Provides strategy suggestions based on role"
    )
    @app_commands.describe(role="Select your role (mage or attack)")
    @app_commands.autocomplete(role=role_autocomplete)
    async def strategy(self, interaction: discord.Interaction, role: str):
        role = role.lower()
        if role not in STRATEGIES:
            await interaction.response.send_message(f"❌ Invalid role. Available: {', '.join(STRATEGIES.keys())}", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Strategy Suggestions - {role.title()}",
            description=STRATEGIES[role],
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Strategy(bot))
