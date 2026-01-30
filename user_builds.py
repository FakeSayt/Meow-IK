# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:51:37 2026

@author: fakey
"""
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "user_marches.json"
BACKUP_FILE = "user_marches_backup.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

def save_data(data):
    if os.path.exists(DATA_FILE):
        os.replace(DATA_FILE, BACKUP_FILE)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class UserBuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addimmortal", description="Add or edit an Immortal for your account")
    @app_commands.describe(
        immortal="Immortal name",
        skills="Skills (comma separated)",
        artifact="Artifact name",
        attributes="Attributes (comma separated)"
    )
    async def addimmortal(self, interaction: discord.Interaction, immortal: str, skills: str, artifact: str, attributes: str):
        data = load_data()
        user_id = str(interaction.user.id)
        data.setdefault(user_id, {"username": interaction.user.name, "immortals": {}, "marches": {}})
        data[user_id]["immortals"][immortal] = {
            "skills": skills,
            "artifact": artifact,
            "attributes": attributes
        }
        save_data(data)
        await interaction.response.send_message(f"✅ Immortal **{immortal}** saved for {interaction.user.name}!")

    @app_commands.command(name="createmarch", description="Create a march from your saved Immortals")
    @app_commands.describe(
        march_name="Name your march",
        immortal1="Immortal 1",
        immortal2="Immortal 2",
        immortal3="Immortal 3",
        immortal4="Immortal 4"
    )
    async def createmarch(self, interaction: discord.Interaction,
                          march_name: str,
                          immortal1: str, immortal2: str, immortal3: str, immortal4: str):
        data = load_data()
        user_id = str(interaction.user.id)
        if user_id not in data:
            await interaction.response.send_message("❌ You have no immortals saved. Use /addimmortal first.", ephemeral=True)
            return

        user_immortals = data[user_id].get("immortals", {})
        for imm in [immortal1, immortal2, immortal3, immortal4]:
            if imm not in user_immortals:
                await interaction.response.send_message(f"❌ Immortal **{imm}** not found. Use /addimmortal first.", ephemeral=True)
                return

        data[user_id]["marches"][march_name] = [immortal1, immortal2, immortal3, immortal4]
        save_data(data)
        await interaction.response.send_message(f"✅ March **{march_name}** created successfully!")

    @app_commands.command(name="showmarch", description="Show all your marches")
    async def showmarch(self, interaction: discord.Interaction):
        data = load_data()
        user_id = str(interaction.user.id)
        if user_id not in data or not data[user_id].get("marches"):
            await interaction.response.send_message("❌ You have no marches. Use /createmarch first.", ephemeral=True)
            return

        for march_name, march_immortals in data[user_id]["marches"].items():
            embed = discord.Embed(title=f"🛡️ March: {march_name}", description=f"Owner: {interaction.user.name}", color=discord.Color.blue())
            for i, imm_name in enumerate(march_immortals, start=1):
                imm = data[user_id]["immortals"].get(imm_name, {})
                embed.add_field(
                    name=f"{i}. {imm_name}",
                    value=(
                        f"**Skills:** {imm.get('skills','Not set')}\n"
                        f"**Artifact:** {imm.get('artifact','Not set')}\n"
                        f"**Attributes:** {imm.get('attributes','Not set')}"
                    ),
                    inline=False
                )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="removeimmortal", description="Remove an Immortal from your collection")
    @app_commands.describe(immortal="Immortal name to remove")
    async def removeimmortal(self, interaction: discord.Interaction, immortal: str):
        data = load_data()
        user_id = str(interaction.user.id)
        if user_id in data and immortal in data[user_id].get("immortals", {}):
            del data[user_id]["immortals"][immortal]
            # usuń też z marchy jeśli jest
            for march in data[user_id].get("marches", {}):
                data[user_id]["marches"][march] = [i for i in data[user_id]["marches"][march] if i != immortal]
            save_data(data)
            await interaction.response.send_message(f"✅ Immortal **{immortal}** removed!")
        else:
            await interaction.response.send_message(f"❌ Immortal **{immortal}** not found.", ephemeral=True)

    @app_commands.command(name="removemarch", description="Remove one of your marches")
    @app_commands.describe(march="March name to remove")
    async def removemarch(self, interaction: discord.Interaction, march: str):
        data = load_data()
        user_id = str(interaction.user.id)
        if user_id in data and march in data[user_id].get("marches", {}):
            del data[user_id]["marches"][march]
            save_data(data)
            await interaction.response.send_message(f"✅ March **{march}** removed!")
        else:
            await interaction.response.send_message(f"❌ March **{march}** not found.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UserBuilds(bot))
