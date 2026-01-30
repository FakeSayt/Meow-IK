# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:51:37 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import shutil
from datetime import datetime

# =============================
# PATHS (RENDER PERSISTENT DISK)
# =============================
DATA_DIR = "/data"
DATA_FILE = f"{DATA_DIR}/user_marches.json"
BACKUP_FILE = f"{DATA_DIR}/user_marches_backup.json"

# =============================
# ENSURE DATA DIRECTORY EXISTS
# =============================
os.makedirs(DATA_DIR, exist_ok=True)

# =============================
# SAFE LOAD
# =============================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # jeśli JSON jest uszkodzony → próbujemy backup
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

# =============================
# SAFE SAVE (ANTI-CORRUPTION)
# =============================
def save_data(data):
    # backup przed zapisem
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE)

    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    os.replace(temp_file, DATA_FILE)

# =============================
# COG
# =============================
class UserBuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    def refresh_data(self):
        self.data = load_data()

    # ================= ADD IMMORTAL =================
    @app_commands.command(name="addimmortal", description="Add an immortal to your collection")
    async def addimmortal(
        self,
        interaction: discord.Interaction,
        name: str,
        skills: str,
        artifact: str,
        attributes: str
    ):
        self.refresh_data()
        user_id = str(interaction.user.id)

        self.data.setdefault(user_id, {
            "username": str(interaction.user),
            "immortals": [],
            "marches": []
        })

        # block duplicates
        if any(i["name"].lower() == name.lower() for i in self.data[user_id]["immortals"]):
            await interaction.response.send_message("❌ Immortal already exists.", ephemeral=True)
            return

        immortal = {
            "name": name,
            "skills": [s.strip() for s in skills.split(",")],
            "artifact": artifact,
            "attributes": [a.strip() for a in attributes.split(",")],
            "created": datetime.utcnow().isoformat()
        }

        self.data[user_id]["immortals"].append(immortal)
        save_data(self.data)

        await interaction.response.send_message(f"✅ Immortal **{name}** added.", ephemeral=True)

    # ================= CREATE MARCH =================
    @app_commands.command(name="createmarch", description="Create a march from your immortals")
    async def createmarch(
        self,
        interaction: discord.Interaction,
        name: str,
        immortal1: str,
        immortal2: str = None,
        immortal3: str = None,
        immortal4: str = None
    ):
        self.refresh_data()
        user_id = str(interaction.user.id)

        user = self.data.get(user_id)
        if not user or not user["immortals"]:
            await interaction.response.send_message("❌ No immortals found.", ephemeral=True)
            return

        selected = []
        for imm_name in [immortal1, immortal2, immortal3, immortal4]:
            if imm_name:
                match = next(
                    (i for i in user["immortals"] if i["name"].lower() == imm_name.lower()),
                    None
                )
                if not match:
                    await interaction.response.send_message(
                        f"❌ Immortal **{imm_name}** not found.",
                        ephemeral=True
                    )
                    return
                selected.append(match)

        march = {
            "name": name,
            "creator": str(interaction.user),
            "immortals": selected,
            "created": datetime.utcnow().isoformat()
        }

        user["marches"].append(march)
        save_data(self.data)

        await interaction.response.send_message(
            f"✅ March **{name}** created ({len(selected)} immortals).",
            ephemeral=True
        )

    # ================= SHOW MY MARCHES =================
    @app_commands.command(name="showmarch", description="Show your marches")
    async def showmarch(self, interaction: discord.Interaction):
        self.refresh_data()
        user_id = str(interaction.user.id)

        user = self.data.get(user_id)
        if not user or not user["marches"]:
            await interaction.response.send_message("❌ You have no marches.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{interaction.user.name}'s Marches",
            color=discord.Color.blurple()
        )

        for march in user["marches"]:
            value = ""
            for imm in march["immortals"]:
                value += (
                    f"• **{imm['name']}**\n"
                    f"  Artifact: {imm['artifact']}\n"
                    f"  Skills: {', '.join(imm['skills'])}\n"
                    f"  Attributes: {', '.join(imm['attributes'])}\n\n"
                )
            embed.add_field(name=march["name"], value=value, inline=False)

        await interaction.response.send_message(embed=embed)

    # ================= MARCH HELP (GLOBAL) =================
    @app_commands.command(name="marchhelp", description="See all marches from all users")
    async def marchhelp(self, interaction: discord.Interaction):
        self.refresh_data()

        embed = discord.Embed(
            title="📜 Community Marches",
            color=discord.Color.green()
        )

        found = False
        for user in self.data.values():
            for march in user.get("marches", []):
                found = True
                names = ", ".join(i["name"] for i in march["immortals"])
                embed.add_field(
                    name=f"{march['name']} (by {march['creator']})",
                    value=names,
                    inline=False
                )

        if not found:
            await interaction.response.send_message("❌ No marches available.", ephemeral=True)
            return

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserBuilds(bot))
