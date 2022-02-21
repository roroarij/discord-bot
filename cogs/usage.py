from discord.ext import commands, tasks
from random import randint
import json
import asyncio
import discord
import aiohttp
import random
from discord.ext.commands.cooldowns import BucketType
import time
import math
import pymongo
import nltk
from pymongo import MongoClient
import sqlite3


sqliteConnection = sqlite3.connect('messages.db')
cursor = sqliteConnection.cursor()

class usage(commands.Cog, name="Usage"):
    """How to use the bot"""
    def __init__(self,bot, hidden):
        self.hidden = hidden
        self.bot = bot
        self.devs = [332443859105873920, 913546966066163712]
        
        
    @commands.command(aliases=['q','ask'])
    async def question(self,ctx,*,question):
        with open('index.json') as f:
          index = json.load(f)
        key = list(ctx.message.content.split(" "))
        w = open('stopwords.txt', 'r')
        potentialanswers = []
        for k in key:
          if k in w:
            key.remove(k)
        for x in key:
          for i in index["main"]:
            if x == i:
              # embed = discord.Embed(title=f"Potential answers to your question", color=0x00FF00)
              for z in index["main"][i]:
                # embed.add_field(name="** **",value=z[0],inline=False)
                potentialanswers.append(z)

        match = []
        count = 0
        key.remove(key[0])
        for j in potentialanswers:
          count = 0
          for l in str(j[1]).split(" "):
            if l in key:
              count += 1
          for b in str(j[0]).split(" "):
            if b in key:
              count += 1
          match.append([count, j])
        high = [0]
        for e in match:
          if e[0] > high[0]:
            high = e
        embed = discord.Embed(title="Potential Answer to your question",color=0x0000FF)
        try:
          embed.add_field(name=f"Original Question: {high[1][1]}", value=f"Answer: {high[1][0]}")
        except:
          return await ctx.send("Could not find any answers to your question.")
        await ctx.send(embed=embed)

        
          
          
                
#         try:
#           await ctx.send(embed=embed)
#         except:
#           await ctx.send("Could not find any answers matching your query")
        
          
        
      
    # @commands.command()
    # async def query(self,ctx,*,keyword):
    #     if ctx.author.id in self.devs:
    #       pass
    #     else:
    #       return await ctx.send("You can't use this command")
        
    #     with open('index.json') as f:
    #       index = json.load(f)
    #     index["main"][keyword] = []
        
        for x in ctx.guild.text_channels:
          messageList = await x.history(limit=10000).flatten()
          for i in messageList:
            if i.author.id == 913546966066163712:
              msg = list(i.content.split(" "))
              if msg[0].startswith("!"):
                pass
              else:
                if keyword in msg:
                  try:
                    imsg = i.content.replace("@everyone", " ")
                  except:
                    imsg = i.content
                  await ctx.send(imsg)
                  if i.content in index["main"][keyword]:
                    pass
                  else:
                    try:
                      ref = await x.fetch_message(int(i.reference.message_id))
                      ref = ref.content
                    except:
                      ref = ["None", "None"]
                    index["main"][keyword].append([i.content, ref])
            else:
              pass
    #     with open('index.json', 'w') as f:
    #       json.dump(index,f)

    @commands.command()
    async def dbadd(self,ctx):
        if ctx.author.id in self.devs:
          pass
        else:
          return await ctx.send("You can't use this")
        mc = 0
        edi = await ctx.send(f"Messages Added: {mc}")
        for x in ctx.guild.text_channels:
          messageList = await x.history(limit=10000).flatten()
          for i in messageList:
            if i.author.id == 913546966066163712:
              if msg[0].startswith("!"):
                pass
              else:
                  try:
                    imsg = i.content.replace("@everyone", " ")
                  except:
                    imsg = i.content
                  try:
                    ref = await x.fetch_message(int(i.reference.message_id))
                    ref = ref.content
                  except:
                    ref = ["None", "None"]
                  index["main"][keyword].append([i.content, ref])
            else:
              pass
          
    @commands.command(hidden=True)
    async def dev(self,ctx):
      if ctx.author.id in self.devs:
        pass
      else:
        return await ctx.send("You can't use this")
      with open('index.json') as f:
        i = json.load(f)
      await ctx.send(i)
      
   
      
          
        
    
        
    
  
  
    
            
    
            
            
def setup(bot):
    bot.add_cog(usage(bot, False))