# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:48:26 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands
import random

MAG_NAMES = ["Merlin", "Baldwin IV", "Himiko", "Hammurabi", "Loki", "Wu", "Cleopatra"]

class FunFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll a random mage or artifact")
    async def roll(self, interaction: discord.Interaction):
        choice = random.choice(MAG_NAMES)
        await interaction.response.send_message(f"🎲 You rolled: **{choice}**!")

    @app_commands.command(name="quiz", description="Simple IK quiz")
    async def quiz(self, interaction: discord.Interaction):
        q = "Which element does Merlin use?"
        options = ["Fire", "Water", "Earth", "Wind"]
        correct = "Water"
        embed = discord.Embed(title="Infinity Kingdom Quiz", description=q, color=discord.Color.orange())
        embed.add_field(name="Options", value=" | ".join(options))
        embed.set_footer(text=f"Correct answer: {correct}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(FunFeatures(bot))
