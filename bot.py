# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 16:59:38 2026
@author: Fakey
"""
import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands
from config import DISCORD_TOKEN, PORT
import asyncio

# ===================== FLASK (KEEP-ALIVE) =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

# uruchomienie Flask w osobnym wątku
Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, use_reloader=False)).start()

# ===================== DISCORD BOT =====================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===================== LOAD COGS =====================
async def load_extensions():
    # Lista wszystkich COGs
    extensions = [
        "mage_stats",
        "bestartifact",
        "strategy",
        "reminder",
        "mage_info",
        "fun_features",
        "admin",
        "user_builds",   # addimmortal, createmarch, showmarch
        "marchhelp",     # nowe, wybór marchy od innych graczy
        "changelog"      # komenda z historią aktualizacji
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Error loading {ext}: {e}")

# ===================== SETUP HOOK =====================
@bot.event
async def setup_hook():
    # Ładuj wszystkie COGs
    await load_extensions()

    # Globalna synchronizacja wszystkich slash commandów
    # Jeśli chcesz, żeby były tylko w jednym guildzie (szybciej), możesz podać guild=discord.Object(id=GUILD_ID)
    await bot.tree.sync()

    print(f"{bot.user} online, all commands synced globally!")

# ===================== RUN BOT =====================
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN missing!")

bot.run(DISCORD_TOKEN)
