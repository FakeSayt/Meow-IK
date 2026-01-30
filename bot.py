# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 16:59:38 2026

@author: Fakey
"""
# bot.py
import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands
from config import DISCORD_TOKEN, PORT
import asyncio

# Flask
app = Flask(__name__)
@app.route("/")
def home(): return "Discord bot is running!"
Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, use_reloader=False)).start()

# Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
async def load_extensions():
    for extension in [
        "mage_stats", "bestartifact", "strategy", "reminder",
        "mage_info", "fun_features", "admin"
    ]:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Error loading {extension}: {e}")

@bot.event
async def setup_hook():
    GUILD_ID = 123456789012345678  # Twój serwer testowy
    guild = discord.Object(id=GUILD_ID)
    await load_extensions()
    await bot.tree.sync(guild=guild)
    print(f"{bot.user} online, commands synced to guild {GUILD_ID}!")

if not DISCORD_TOKEN: raise ValueError("DISCORD_TOKEN missing!")
bot.run(DISCORD_TOKEN)

