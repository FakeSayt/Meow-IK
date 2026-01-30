# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:51:37 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands

class UserBuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_immortals = {}  # user_id -> list of immortals
        self.user_marches = {}    # user_id -> list of marches

    # ------------------- Autocomplete Functions -------------------
    async def immortal_autocomplete(self, interaction: discord.Interaction, current: str):
        user_id = interaction.user.id
        saved = self.user_immortals.get(user_id, [])
        if not saved:
            return []
        return [
            app_commands.Choice(name=imm["name"], value=imm["name"])
            for imm in saved
            if current.lower() in imm["name"].lower()
        ]

    async def march_autocomplete(self, interaction: discord.Interaction, current: str):
        user_id = interaction.user.id
        marches = self.user_marches.get(user_id, [])
        if not marches:
            return []
        return [
            app_commands.Choice(name=march["name"], value=march["name"])
            for march in marches
            if current.lower() in march["name"].lower()
        ]

    # ------------------- /addimmortal -------------------
    @app_commands.command(name="addimmortal", description="Add an immortal to your personal collection")
    @app_commands.describe(
        name="Immortal name",
        skills="Comma-separated list of skills",
        artifact="Artifact name",
        attributes="Comma-separated attributes (e.g., crit, attack, defense)"
    )
    async def addimmortal(self, interaction: discord.Interaction, name: str, skills: str, artifact: str, attributes: str):
        user_id = interaction.user.id
        immortal = {
            "name": name,
            "skills": [s.strip() for s in skills.split(",")],
            "artifact": artifact,
            "attributes": [a.strip() for a in attributes.split(",")]
        }
        self.user_immortals.setdefault(user_id, []).append(immortal)
        await interaction.response.send_message(f"✅ Immortal `{name}` added to your collection!", ephemeral=True)

    # ------------------- /editimmortal -------------------
    @app_commands.command(name="editimmortal", description="Edit skills, artifact or attributes of an immortal")
    @app_commands.describe(
        name="Immortal name",
        skills="Comma-separated list of skills",
        artifact="Artifact name",
        attributes="Comma-separated attributes"
    )
    @app_commands.autocomplete(name=immortal_autocomplete)
    async def editimmortal(self, interaction: discord.Interaction, name: str, skills: str = None, artifact: str = None, attributes: str = None):
        user_id = interaction.user.id
        saved = self.user_immortals.get(user_id, [])
        for imm in saved:
            if imm["name"].lower() == name.lower():
                if skills:
                    imm["skills"] = [s.strip() for s in skills.split(",")]
                if artifact:
                    imm["artifact"] = artifact
                if attributes:
                    imm["attributes"] = [a.strip() for a in attributes.split(",")]
                await interaction.response.send_message(f"✅ Immortal `{name}` updated.", ephemeral=True)
                return
        await interaction.response.send_message(f"❌ Immortal `{name}` not found.", ephemeral=True)

    # ------------------- /removeimmortal -------------------
    @app_commands.command(name="removeimmortal", description="Remove an immortal from your collection")
    @app_commands.describe(name="Immortal name")
    @app_commands.autocomplete(name=immortal_autocomplete)
    async def removeimmortal(self, interaction: discord.Interaction, name: str):
        user_id = interaction.user.id
        saved = self.user_immortals.get(user_id, [])
        for imm in saved:
            if imm["name"].lower() == name.lower():
                saved.remove(imm)
                await interaction.response.send_message(f"✅ Immortal `{name}` removed.", ephemeral=True)
                return
        await interaction.response.send_message(f"❌ Immortal `{name}` not found.", ephemeral=True)

    # ------------------- /createmarch -------------------
    @app_commands.command(name="createmarch", description="Create a march from your saved immortals (up to 4) and give it a name")
    @app_commands.describe(
        immortal1="Choose your first immortal",
        immortal2="Second immortal",
        immortal3="Third immortal",
        immortal4="Fourth immortal",
        name="Name of the march (e.g., Water vs Fire)"
    )
    @app_commands.autocomplete(
        immortal1=immortal_autocomplete,
        immortal2=immortal_autocomplete,
        immortal3=immortal_autocomplete,
        immortal4=immortal_autocomplete
    )
    async def createmarch(self, interaction: discord.Interaction, immortal1: str, immortal2: str, immortal3: str = None, immortal4: str = None, name: str = "Unnamed March"):
        user_id = interaction.user.id
        saved = self.user_immortals.get(user_id, [])
        if not saved:
            await interaction.response.send_message("❌ You don't have any immortals yet. Use /addimmortal first.", ephemeral=True)
            return
        name_map = {imm["name"].lower(): imm for imm in saved}
        selected_names = [immortal1, immortal2, immortal3, immortal4]
        selected_names = [n.lower() for n in selected_names if n]
        if len(selected_names) < 2:
            await interaction.response.send_message("❌ You must select at least 2 immortals.", ephemeral=True)
            return
        missing = [n for n in selected_names if n not in name_map]
        if missing:
            await interaction.response.send_message(f"❌ These immortals are not in your collection: {', '.join(missing)}", ephemeral=True)
            return

        march = {"name": name, "immortals": [name_map[n] for n in selected_names]}
        self.user_marches.setdefault(user_id, []).append(march)

        embed = discord.Embed(title=f"March Created: {name}", color=discord.Color.gold())
        for i, imm in enumerate(march["immortals"], start=1):
            embed.add_field(name=f"{i}. {imm['name']}", value=f"**Skills:** {', '.join(imm['skills'])}\n**Artifact:** {imm['artifact']}\n**Attributes:** {', '.join(imm['attributes'])}", inline=False)
        await interaction.response.send_message(embed=embed)

    # ------------------- /editmarch -------------------
    @app_commands.command(name="editmarch", description="Edit a march: name or immortals")
    @app_commands.describe(
        name="Current march name",
        new_name="New name for the march",
        immortal1="New first immortal",
        immortal2="New second immortal",
        immortal3="New third immortal",
        immortal4="New fourth immortal"
    )
    @app_commands.autocomplete(name=march_autocomplete, immortal1=immortal_autocomplete, immortal2=immortal_autocomplete, immortal3=immortal_autocomplete, immortal4=immortal_autocomplete)
    async def editmarch(self, interaction: discord.Interaction, name: str, new_name: str = None, immortal1: str = None, immortal2: str = None, immortal3: str = None, immortal4: str = None):
        user_id = interaction.user.id
        marches = self.user_marches.get(user_id, [])
        saved = self.user_immortals.get(user_id, [])
        name_map = {imm["name"].lower(): imm for imm in saved}

        for march in marches:
            if march["name"].lower() == name.lower():
                if new_name:
                    march["name"] = new_name
                selected_names = [immortal1, immortal2, immortal3, immortal4]
                selected_names = [n.lower() for n in selected_names if n]
                if selected_names:
                    missing = [n for n in selected_names if n not in name_map]
                    if missing:
                        await interaction.response.send_message(f"❌ These immortals are not in your collection: {', '.join(missing)}", ephemeral=True)
                        return
                    march["immortals"] = [name_map[n] for n in selected_names]
                await interaction.response.send_message(f"✅ March `{name}` updated.", ephemeral=True)
                return
        await interaction.response.send_message(f"❌ March `{name}` not found.", ephemeral=True)

    # ------------------- /removemarch -------------------
    @app_commands.command(name="removemarch", description="Remove a march by name")
    @app_commands.describe(name="Name of the march to remove")
    @app_commands.autocomplete(name=march_autocomplete)
    async def removemarch(self, interaction: discord.Interaction, name: str):
        user_id = interaction.user.id
        marches = self.user_marches.get(user_id, [])
        for march in marches:
            if march["name"].lower() == name.lower():
                marches.remove(march)
                await interaction.response.send_message(f"✅ March `{name}` removed.", ephemeral=True)
                return
        await interaction.response.send_message(f"❌ March `{name}` not found.", ephemeral=True)

    # ------------------- /showmarch -------------------
    @app_commands.command(name="showmarch", description="Show all your created marches with their names")
    async def showmarch(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        marches = self.user_marches.get(user_id)
        if not marches:
            await interaction.response.send_message("❌ You don't have any marches yet. Use /createmarch first.", ephemeral=True)
            return
        for idx, march in enumerate(marches, start=1):
            embed = discord.Embed(title=f"{idx}. {march['name']}", color=discord.Color.green())
            for i, imm in enumerate(march['immortals'], start=1):
                embed.add_field(name=f"{i}. {imm['name']}", value=f"**Skills:** {', '.join(imm['skills'])}\n**Artifact:** {imm['artifact']}\n**Attributes:** {', '.join(imm['attributes'])}", inline=False)
            await interaction.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserBuilds(bot))
