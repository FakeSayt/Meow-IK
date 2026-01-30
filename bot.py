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

# Flask server
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, use_reloader=False)).start()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load extensions
async def load_extensions():
    for extension in ["mage_stats", "bestartifact", "strategy", "reminder"]:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Error loading {extension}: {e}")

@bot.event
async def setup_hook():
    await load_extensions()
    await bot.tree.sync()
    print(f"{bot.user} is online and all commands are synced!")

# Run bot
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is missing!")

bot.run(DISCORD_TOKEN)
