# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 17:00:42 2026

@author: theve
"""

import discord
from discord.ext import commands
from discord import app_commands

ROLES = ["mage", "attack"]
BUILDS = {
    "mage": ["crit", "nonchase"],
    "attack": ["ultimate", "physical"]
}

class BestArtifact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def role_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=r, value=r) for r in ROLES if current.lower() in r.lower()]

    async def build_autocomplete(self, interaction: discord.Interaction, current: str):
        role = getattr(interaction.namespace, "role", "").lower()
        options = BUILDS.get(role, [])
        return [app_commands.Choice(name=b, value=b) for b in options if current.lower() in b.lower()]

    @app_commands.command(
        name="bestartifact",
        description="Best artifact rolls for Mages and Attack Immortals"
    )
    @app_commands.describe(role="Select your role", build="Select your build")
    @app_commands.autocomplete(role=role_autocomplete, build=build_autocomplete)
    async def bestartifact(self, interaction: discord.Interaction, role: str, build: str):
        role = role.lower()
        build = build.lower()

        if role not in ROLES:
            await interaction.response.send_message(f"❌ Invalid role. Available: {', '.join(ROLES)}", ephemeral=True)
            return

        if build not in BUILDS.get(role, []):
            await interaction.response.send_message(f"❌ Invalid build. Available: {', '.join(BUILDS[role])}", ephemeral=True)
            return

        embed = discord.Embed(title=f"Best Artifact - {role.title()} ({build.title()})", color=discord.Color.purple())

        if role == "mage":
            if build == "crit":
                embed.description = (
                    "🔮 **Mage – Crit (Chase) Build**\n\n"
                    "Priority Rolls: Crit Rate → Magical Attack → Crit Damage → Magical Defense\n"
                    "💡 Best if VIP 13+"
                )
            elif build == "nonchase":
                embed.description = (
                    "🔮 **Mage – Non-Chase Build**\n\n"
                    "Priority Rolls: Magical Attack → Magical Attack Value → Crit Rate → Crit Damage → Defenses\n"
                    "💡 Focus on pure % damage"
                )
        elif role == "attack":
            if build == "ultimate":
                embed.description = (
                    "⚔️ **Attack – Ultimate DPS**\n\n"
                    "Top Priority: Physical Attack → Surge → Iron Fist → Magical Defense → Accuracy → Physical Defense\n"
                    "📌 Examples: Herald, William, Attila, Ramesses, Hippolyta"
                )
            elif build == "physical":
                embed.description = (
                    "⚔️ **Attack – Physical DPS**\n\n"
                    "Top Priority: Physical Attack → Rapid (Alex/Hannibal) → Accuracy → Physical Defense → Crit\n"
                    "📌 Examples: Alexander, Hannibal, Manco, Saladin"
                )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BestArtifact(bot))
