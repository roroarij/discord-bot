from discord.ext import commands
from random import randint
import json
import asyncio
import discord
import aiohttp
import random
from discord.ext.commands.cooldowns import BucketType
import time
import math
from pymongo import MongoClient


class util(commands.Cog):
    """Utilities"""
    def __init__(self, bot, hidden):
        self.hidden = hidden
        self.bot = bot
        
    @commands.command()
    async def help(self, ctx, *cog):
        """Displays the help command
        Anything in angled brackets <> is a required argument. Square brackets [] mark an optional argument"""
        if not ctx.guild:
            prefix = "!"
        else:
            prefix = "!"
            # guild = guilds.find_one({"_id": ctx.guild.id})
            # prefix = guild["prefix"]
        if not cog:
            embed = discord.Embed(title="Help", description=f"use `{prefix}help [category|command]` for more info", color=0x00FF00)
            embed.set_footer(text=f"Created by Tense#7987 and core_#6969")
            cog_desc = ''
            for x in self.bot.cogs:
                if not self.bot.cogs[x].hidden:
                    cmd = ''
                    cog_desc += f"__**{x}**__: {self.bot.cogs[x].__doc__}\n"
                    for y in self.bot.get_cog(x).get_commands():
                        cmd += f"`{prefix}{y}`,  "
                    embed.add_field(name=f"__**{x}**__: {self.bot.cogs[x].__doc__}", value=cmd, inline=False)
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                await ctx.send("That is not a valid category")
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            #title="Help", description=f"**Category {cog[0]}:** {self.bot.cogs[cog[0]].__doc__}", 
                            embed = discord.Embed(title="Help", color=0x00FF00)
                            scog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f"\n**`{c.name}`**: {c.help}\n"
                            embed.add_field(name=f"\n{cog[0]} Category:\n{self.bot.cogs[cog[0]].__doc__}\n ", value=f"\n{scog_info}\n", inline=False)
                            found = True

            if not found:
                for x in self.bot.cogs:
                    for c in self.bot.get_cog(x).get_commands():
                        if c.name == cog[0]:
                            embed = discord.Embed(color=0x00FF00)
                            embed.add_field(name=f"{c.name}: {c.help}", value=f"Usage:\n `{prefix}{c.qualified_name} {c.signature}`")
                            found = True
            if not found:
                embed = discord.Embed(description="Command not found. Check that you have spelt it correctly and used capitals where appropriate")
            await ctx.send(embed=embed)
            

            #     @commands.command()
#     @commands.cooldown(1,600, BucketType.guild) 
#     async def suggest(self, ctx, *, answer:str):
#         suggestion = discord.Embed(title=answer, color=0x00FF00)
#         suggestion.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
#         sugChannel = self.bot.get_channel(715373572943773736)
#         sugmsg = await sugChannel.send(embed=suggestion)
#         await sugmsg.add_reaction(u"\u2705")
#         await sugmsg.add_reaction(u"\u274C")
#         await ctx.send(ctx.author.mention + ", suggestion logged, check <#691456328853356544> to see its prgoress", delete_after=5)
#         await ctx.message.delete()
    
#     @commands.command()
#     async def help(self, ctx, category:str=None):
#         if not category:
#             helpmsg = discord.Embed(title="Help", description="type `s!help [category]` for more info on a category", color=0x00FF00)
#             helpmsg.add_field(name="leveling", value="gain levels through engaging in chat", inline=False)
#             helpmsg.add_field(name="utilites", value="command to improve your time in the server", inline=False)
#             helpmsg.add_field(name="scammer", value="commands to help prevent scams", inline=False)
#             await ctx.send(embed=helpmsg)
#         elif category.lower() == "leveling":
#             helpmsg = discord.Embed(title="Leveling", description="earn levels through engaging in chat", color=0x00FF00)
#             level5 = ctx.guild.get_role(709335896637308939)
#             level10 = ctx.guild.get_role(709336217610747955)
#             level15 = ctx.guild.get_role(709336451577544747)
#             level25 = ctx.guild.get_role(709336750958313483)
#             level35 = ctx.guild.get_role(709337343278186606)
#             level50 = ctx.guild.get_role(709337566779801621)
#             helpmsg.add_field(name="Level 5", value=level5.mention, inline=False)
#             helpmsg.add_field(name="Level 10", value=level10.mention, inline=False)
#             helpmsg.add_field(name="Level 15", value=level15.mention, inline=False)
#             helpmsg.add_field(name="Level 25", value=level25.mention, inline=False)
#             helpmsg.add_field(name="Level 35", value=level35.mention, inline=False)
#             helpmsg.add_field(name="Level 50", value=level50.mention, inline=False)
#             helpmsg.add_field(name="Commands", value="`s!rank`/`s!leaderboard`", inline=False)
#             await ctx.send(embed=helpmsg)
#         elif category.lower() == "utilities":
#             helpmsg = discord.Embed(title="Utilities", description="Commands to make your life easier", color=0x00FF00)
#             helpmsg.add_field(name="`s!suggest [suggestion]`", value="log a suggestion for the server. Cooldown applies", inline=False)
#             helpmsg.add_field(name="`s!help`", value="Guide to commands", inline=False)
#             await ctx.send(embed=helpmsg)
#         elif category.lower() == "admin":
#             helpmsg = discord.Embed(title="Admin", description="Admin commands", color=0x00FF00)
#             helpmsg.add_field(name="`s!ban [user] [reason]", value="Ban a user for a specific reason", inline=False)
#             helpmsg.add_field(name="`s!warn [user] [reason]`", value="Warn a user for a specific reason", inline=False)
#             helpmsg.add_field(name="`s!ReactionRole [message id] [role name]", value="Set up a reaction role")
#         elif category.lower() == "scammer":
#             helpmsg = discord.Embed(title="Scammer commands", description="commands to help prevent scams", color=0x00FF00)
#             helpmsg.add_field(name="`s!report [user] [reason]`", value="report a minecraft user for scamming/griefing", inline=False)
#             helpmsg.add_field(name="`s!check [user]`", value="Check a user against our scammer list", inline=False)
#             await ctx.send(embed=helpmsg)

def setup(bot):
    bot.add_cog(util(bot, False))