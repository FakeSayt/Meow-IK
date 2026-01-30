# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 19:59:41 2026

@author: fakey
"""
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "user_marches.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class MarchSelect(discord.ui.Select):
    def __init__(self, marches):
        self.marches = marches
        options = [
            discord.SelectOption(
                label=f"{m['name']} — by {m['author']}", 
                value=m["id"]
            )
            for m in marches
        ]
        super().__init__(placeholder="Select a march to view...", options=options)

    async def callback(self, interaction: discord.Interaction):
        march_id = self.values[0]
        march = next(m for m in self.marches if m["id"] == march_id)

        embed = discord.Embed(
            title=f"🛡️ {march['author']}'s March: {march['name']}",
            description=f"Created by **{march['author']}**",
            color=discord.Color.blue()
        )
        for i, immortal in enumerate(march["immortals"], start=1):
            embed.add_field(
                name=f"• {immortal['name']}",
                value=(
                    f"**Artifact:** {immortal.get('artifact','Not set')}\n"
                    f"**Skills:** {immortal.get('skills','Not set')}\n"
                    f"**Attributes:** {immortal.get('attributes','Not set')}"
                ),
                inline=False
            )
        await interaction.response.send_message(embed=embed)

class MarchHelpView(discord.ui.View):
    def __init__(self, marches):
        super().__init__(timeout=60)  # <--- timeout 60s
        self.add_item(MarchSelect(marches))

class MarchHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="marchhelp",
        description="Browse marches created by other players"
    )
    async def marchhelp(self, interaction: discord.Interaction):
        data = load_data()
        marches = []

        for user_id, user_data in data.items():
            username = user_data.get("username", "Unknown")
            immortals = user_data.get("immortals", {})
            user_marches = user_data.get("marches", {})

            for march_name, march_immortals in user_marches.items():
                detailed_immortals = []
                for name in march_immortals:
                    im = immortals.get(name, {})
                    detailed_immortals.append({
                        "name": name,
                        "skills": im.get("skills","Not set"),
                        "artifact": im.get("artifact","Not set"),
                        "attributes": im.get("attributes","Not set")
                    })
                marches.append({
                    "id": f"{user_id}:{march_name}",
                    "name": march_name,
                    "author": username,
                    "immortals": detailed_immortals
                })

        if not marches:
            await interaction.response.send_message("❌ No marches shared yet.", ephemeral=True)
            return

        await interaction.response.send_message(
            "📋 **Select a march to view details:**",
            view=MarchHelpView(marches)
        )

async def setup(bot):
    await bot.add_cog(MarchHelp(bot))

