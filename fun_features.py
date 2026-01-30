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

class QuizSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Fire"),
            discord.SelectOption(label="Water"),
            discord.SelectOption(label="Earth"),
            discord.SelectOption(label="Wind"),
        ]
        super().__init__(placeholder="Choose an answer...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Water":
            await interaction.response.send_message("✅ Correct! Merlin uses **Water**.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Wrong answer. Try again next time!", ephemeral=True)

class QuizView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.add_item(QuizSelect())

class FunFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll a random mage or artifact")
    async def roll(self, interaction: discord.Interaction):
        choice = random.choice(MAG_NAMES)
        await interaction.response.send_message(f"🎲 You rolled: **{choice}**!")

    @app_commands.command(name="quiz", description="Infinity Kingdom quiz")
    async def quiz(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Infinity Kingdom Quiz",
            description="Which element does **Merlin** use?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="Options",
            value="Fire | Water | Earth | Wind"
        )

        await interaction.response.send_message(embed=embed, view=QuizView())

async def setup(bot):
    await bot.add_cog(FunFeatures(bot))
