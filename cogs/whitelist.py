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
from pymongo import MongoClient


class whitelist(commands.Cog, name="whitelist"):
    """whitelist commands"""
    def __init__(self,bot, hidden):
        self.hidden = hidden
        self.bot = bot
        self.devs = [332443859105873920, 913546966066163712]
        
    def update_addresses():
      with open("addresses.json", "w") as f:
        json.dump(whitelisted, f)

    GUILD='Test server'
    def get_whitelist(): 
      with open("addresses.json", "r") as f:
      
        data =f.read()
        wl=json.loads(data)
      return wl

    whitelisted=get_whitelist()

    @commands.command()
    async def entries(ctx):
        if ctx.author.id in self.devs:
            pass
        else:
            return await ctx.send("You can't use this command")
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        if totalInvites//5 >= 10:
          await ctx.send(f"You have 10 entries. 0 entries remaining.")
        else:      
          await ctx.send(f"You have {totalInvites//5 +1 } entries. {9-totalInvites//5} entries remaining. Each 5 members you invite is an additional entry.")

    @commands.command()
    async def wl(ctx, arg):
        if ctx.author.id in self.devs:
            pass
        else:
            return await ctx.send("You can't use this command")
        if str(arg) in whitelisted:
          await ctx.send(f"Wallet address {arg} has been sucessfully registered and is whitelisted.")
        else:
            await ctx.send(f"Wallet address {arg} has not been registered in the google form. To whitelist this address, please use the !add_address command followed by the wallet address - Example: !add_address 0x8F36cc02AcE07d5698DB9aC0f612A3dc6647d127 .  You may also  fill out the following google form https://forms.gle/LjxXNaegCwVQ15YJ8 or If you have already submitted it in the form, please wait some time for the bot to update your submission.")
    @commands.command()        
    async def change_wl_address(ctx, old, new):
        if ctx.author.id in self.devs:
            pass
        else:
            return await ctx.send("You can't use this command")
        if str(old) in whitelisted:
          try: 
            whitelisted.remove(old)
            whitelisted.append(new)
            update_addresses()
            await ctx.send(f"Whitelisted wallet address {old} has been sucessfully changed to {new}.")
          except:
              await ctx.send("Error")
        else:
          if str(old) not in whitelisted:
            await ctx.send(f"Wallet address {old} is not in our submissions. Please submit the new address in our google form or using the !add_address command followed by the address")    
    @commands.command()        
    async def add_address(ctx, new):
        if ctx.author.id in self.devs:
            pass
        else:
            return await ctx.send("You can't use this command")
        if str(new) in whitelisted:
        
          await ctx.send(f"Whitelisted wallet address {new} has already been submitted and is successfully registered.")
        
        else:
          if str(new) not in whitelisted:
            whitelisted.append(new)
            update_addresses()
            await ctx.send(f"Wallet address {new} has been successfully added and is now whitelisted.") 

          
    @commands.command()        
    async def add_addresses(ctx, *addresses):
      if ctx.author.id in self.devs:
            pass
      else:
            return await ctx.send("You can't use this command")
      submitted=[]
      new=[]
      for address in list(addresses):
        if str(address) in whitelisted:
          submitted.append(address)
        else:
          if str(address) not in whitelisted:
            new.append(address)
            whitelisted.append(address)
            update_addresses()
      await ctx.send(f"The following addresses have already been whitelisted: {submitted}. \n The following have now been added: {new}")
        
              
    @commands.command()
    async def remove_address(ctx, old):
        if ctx.author.id in self.devs:
            pass
        else:
            return await ctx.send("You can't use this command")
        if str(old) in whitelisted:
          whitelisted.remove(old)
          update_addresses()
          await ctx.send(f"Whitelisted wallet address {old} has been successfully removed")
        
        else:
          if str(old) not in whitelisted:
            
            await ctx.send(f"Wallet address {old} is not in our records and was never submitted.")
      
      
   
      
          
        
    
        
    
  
  
    
            
    
            
            
def setup(bot):
    bot.add_cog(whitelist(bot, False))