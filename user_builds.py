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

DATA_FILE = "user_marches.json"

# Helper: wczytaj dane z pliku
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Helper: zapisz dane do pliku
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class UserBuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()  # wczytaj przy starcie

    # ================= ADD IMMORTAL =================
    @app_commands.command(name="addimmortal", description="Add an immortal to your collection")
    @app_commands.describe(name="Immortal name", skills="Skills separated by commas", artifact="Artifact name", attributes="Attributes separated by commas")
    async def addimmortal(self, interaction: discord.Interaction, name: str, skills: str, artifact: str, attributes: str):
        user_id = str(interaction.user.id)
        user_name = str(interaction.user)
        immortal = {
            "name": name,
            "skills": [s.strip() for s in skills.split(",")],
            "artifact": artifact,
            "attributes": [a.strip() for a in attributes.split(",")]
        }
        self.data.setdefault(user_id, {"username": user_name, "immortals": [], "marches": []})
        self.data[user_id]["immortals"].append(immortal)
        save_data(self.data)
        await interaction.response.send_message(f"✅ Immortal **{name}** added to your collection.", ephemeral=True)

    # ================= CREATE MARCH =================
    @app_commands.command(name="createmarch", description="Create a march with up to 4 immortals")
    @app_commands.describe(name="Name of your march", immortal1="First immortal", immortal2="Second immortal (optional)", immortal3="Third immortal (optional)", immortal4="Fourth immortal (optional)")
    async def createmarch(self, interaction: discord.Interaction, name: str, immortal1: str, immortal2: str = None, immortal3: str = None, immortal4: str = None):
        user_id = str(interaction.user.id)
        user_name = str(interaction.user)
        user_data = self.data.get(user_id)
        if not user_data or not user_data["immortals"]:
            await interaction.response.send_message("❌ You have no immortals yet. Use /addimmortal first.", ephemeral=True)
            return

        immortals_names = [immortal1, immortal2, immortal3, immortal4]
        immortals_list = []
        for name_ in immortals_names:
            if name_:
                match = next((i for i in user_data["immortals"] if i["name"].lower() == name_.lower()), None)
                if not match:
                    await interaction.response.send_message(f"❌ Immortal **{name_}** not found in your collection.", ephemeral=True)
                    return
                immortals_list.append(match)

        march = {"name": name, "immortals": immortals_list, "creator": user_name}
        user_data["marches"].append(march)
        save_data(self.data)
        await interaction.response.send_message(f"✅ March **{name}** created with {len(immortals_list)} immortals.", ephemeral=True)

    # ================= SHOW MARCH (twoje) =================
    @app_commands.command(name="showmarch", description="Show your marches")
    async def showmarch(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        user_data = self.data.get(user_id)
        if not user_data or not user_data["marches"]:
            await interaction.response.send_message("❌ You have no marches yet.", ephemeral=True)
            return

        embed = discord.Embed(title=f"{interaction.user}'s Marches", color=discord.Color.blurple())
        for march in user_data["marches"]:
            march_text = ""
            for imm in march["immortals"]:
                march_text += f"• {imm['name']} | Artifact: {imm['artifact']} | Skills: {', '.join(imm['skills'])} | Attributes: {', '.join(imm['attributes'])}\n"
            embed.add_field(name=march["name"], value=march_text, inline=False)
        await interaction.response.send_message(embed=embed)

    # ================= MARCH HELP =================
    @app_commands.command(name="marchhelp", description="See all marches from all users")
    async def marchhelp(self, interaction: discord.Interaction):
        all_marches = []
        for user_id, user_data in self.data.items():
            for march in user_data.get("marches", []):
                all_marches.append((march["name"], march["creator"], march["immortals"]))

        if not all_marches:
            await interaction.response.send_message("❌ No marches found yet.", ephemeral=True)
            return

        embed = discord.Embed(title="📜 All User Marches", color=discord.Color.green())
        for march_name, creator, immortals in all_marches:
            march_text = "\n".join([f"• {imm['name']} | Artifact: {imm['artifact']}" for imm in immortals])
            embed.add_field(name=f"{march_name} (by {creator})", value=march_text, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserBuilds(bot))

