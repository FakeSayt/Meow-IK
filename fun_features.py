# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:48:26 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

MAG_NAMES = ["Merlin", "Baldwin IV", "Himiko", "Hammurabi", "Loki", "Wu", "Cleopatra"]
QUIZ_FILE = "quiz_scores.json"

def load_scores():
    if not os.path.exists(QUIZ_FILE):
        return {}
    with open(QUIZ_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_scores(scores):
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)

class QuizSelect(discord.ui.Select):
    def __init__(self, correct_answer, user_id):
        self.correct_answer = correct_answer
        self.user_id = str(user_id)
        options = [
            discord.SelectOption(label="Fire"),
            discord.SelectOption(label="Water"),
            discord.SelectOption(label="Earth"),
            discord.SelectOption(label="Wind")
        ]
        super().__init__(placeholder="Choose an answer...", options=options)

    async def callback(self, interaction: discord.Interaction):
        scores = load_scores()
        scores.setdefault(self.user_id, 0)

        if self.values[0] == self.correct_answer:
            scores[self.user_id] += 1
            save_scores(scores)
            await interaction.response.send_message(
                f"✅ Correct! Your score: {scores[self.user_id]}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Wrong! Correct answer was **{self.correct_answer}**. Your score: {scores[self.user_id]}",
                ephemeral=True
            )

class QuizView(discord.ui.View):
    def __init__(self, correct_answer, user_id):
        super().__init__(timeout=60)  # <--- timeout 60s
        self.add_item(QuizSelect(correct_answer, user_id))

class FunFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll a random mage or artifact")
    async def roll(self, interaction: discord.Interaction):
        choice = random.choice(MAG_NAMES)
        await interaction.response.send_message(f"🎲 You rolled: **{choice}**!")

    @app_commands.command(name="quiz", description="Infinity Kingdom interactive quiz")
    async def quiz(self, interaction: discord.Interaction):
        question = "Which element does Merlin use?"
        correct_answer = "Water"
        options = ["Fire", "Water", "Earth", "Wind"]

        embed = discord.Embed(
            title="Infinity Kingdom Quiz",
            description=question,
            color=discord.Color.orange()
        )
        embed.add_field(name="Options", value=" | ".join(options))
        embed.set_footer(text="Click your answer below!")

        view = QuizView(correct_answer, interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="quizscore", description="Check your current quiz score")
    async def quizscore(self, interaction: discord.Interaction):
        scores = load_scores()
        score = scores.get(str(interaction.user.id), 0)
        await interaction.response.send_message(f"📊 {interaction.user.name}, your current quiz score: {score}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunFeatures(bot))
