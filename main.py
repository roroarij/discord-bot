import keep_alive
import discord
import os
import random
import json
from colour import color
from discord.ext import commands
from discord.utils import get
import traceback
import difflib
import sys
from datetime import datetime
import time
import asyncio
TOKEN = os.environ['token']
GUILD='Test server'
def get_whitelist(): 
 with open("addresses.json", "r") as f:
   
  data =f.read()
  wl=json.loads(data)
 return wl

whitelisted=get_whitelist()

bot = commands.Bot(command_prefix='!')

#region colours
blue = color.BLUE
endc = color.END
bold = color.BOLD
purple = color.PURPLE
green = color.GREEN
red = color.RED
yellow = color.YELLOW
#endregion

def printProgressBar(iteration, total, prefix= '', suffix = '', decimals = 1, length = 100, fill = "█", printEnd = "\r"):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	if iteration == total: 
		print(f'\r{purple}Loading Complete:             |{bar}| {percent}% {suffix}{endc}', end = printEnd)
	elif iteration in [0, 1]:
		print(f'\r{purple}{prefix} |{bar}| {percent}%   {suffix}{endc}', end = printEnd)
	else:
		print(f'\r{purple}{prefix} |{bar}| {percent}%  {suffix}{endc}', end = printEnd)

cogs = ['cogs.util', 'cogs.usage']

def update_addresses():
  with open("addresses.json", "w") as f:
     json.dump(whitelisted, f)

@bot.command()
async def entries(ctx):
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    if totalInvites//5 >= 10:
     await ctx.send(f"You have 10 entries. 0 entries remaining.")
    else:      
     await ctx.send(f"You have {totalInvites//5 +1 } entries. {9-totalInvites//5} entries remaining. Each 5 members you invite is an additional entry.")

@bot.command()
async def wl(ctx, arg):
    if str(arg) in whitelisted:
      await ctx.send(f"Wallet address {arg} has been sucessfully registered and is whitelisted.")
    else:
        await ctx.send(f"Wallet address {arg} has not been registered in the google form. To whitelist this address, please use the !add_address command followed by the wallet address - Example: !add_address 0x8F36cc02AcE07d5698DB9aC0f612A3dc6647d127 .  You may also  fill out the following google form https://forms.gle/LjxXNaegCwVQ15YJ8 or If you have already submitted it in the form, please wait some time for the bot to update your submission.")
@bot.command()        
async def change_wl_address(ctx, old, new):
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
@bot.command()        
async def add_address(ctx, new):
    if str(new) in whitelisted:
     
      await ctx.send(f"Whitelisted wallet address {new} has already been submitted and is successfully registered.")
    
    else:
      if str(new) not in whitelisted:
        whitelisted.append(new)
        update_addresses()
        await ctx.send(f"Wallet address {new} has been successfully added and is now whitelisted.") 

       
@bot.command()        
async def add_addresses(ctx, *addresses):
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
    
          
@bot.command()
async def remove_address(ctx, old):
    if str(old) in whitelisted:
     whitelisted.remove(old)
     update_addresses()
     await ctx.send(f"Whitelisted wallet address {old} has been successfully removed")
    
    else:
      if str(old) not in whitelisted:
        
        await ctx.send(f"Wallet address {old} is not in our records and was never submitted.")   

@bot.event
async def on_command_error(ctx, exception):
	if type(exception) == commands.CommandOnCooldown:
		await ctx.send("{} is on cooldown for {:0.2f} seconds.".format(ctx.command, exception.retry_after), delete_after=5)
	elif type(exception) == commands.CommandNotFound:
		cmd = ctx.message.content.split()[0][1:]
		try:
			closest = difflib.get_close_matches(cmd.lower(), list(bot.all_commands))[0]
		except IndexError:
			await ctx.send("{} is not a known command.".format(cmd), delete_after=5)
		else:
			await ctx.send("{} is not a command, did you mean {}?".format(cmd, closest), delete_after=5)
	elif type(exception) == commands.CheckFailure:
		await ctx.send("You failed to meet a requirement for that ""command.", delete_after=5)
	elif type(exception) == commands.MissingRequiredArgument:
		await ctx.send("You are missing a required argument for that ""command.", delete_after=5)
	elif type(exception) == commands.BadArgument:
		await ctx.send("Invalid Argument.", delete_after=5)
	elif type(exception) == commands.MissingRole:
		await ctx.send("You don't have the required roles to perform that.", delete_after=5)
	elif type(exception) == commands.MissingPermissions:
		await ctx.send("You don't have the required permissions to perform that.", delete_after=5)
	else:
		print(exception)
	print('Ignoring exception in command {}'.format(ctx.command),
		  file=sys.stderr)
	traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr) 

@bot.event
async def on_ready():
    bot.remove_command("help")
    print(f"{yellow}Loading the beast: {bot.user.name}!{endc}\n")
    time.sleep(1)
    l = len(cogs)
    printProgressBar(0, l, prefix = f'\nInitializing:                ', suffix = 'Complete', length = 50)
    for i, cog in enumerate(cogs):
        time.sleep(0.3)
        printProgressBar(i + 1, l, prefix = f'Loading:{" " * (20 - len(cog))} {cog}', suffix = 'Complete', length = 50)
        bot.load_extension(cog)
    print(f"{yellow}\nInitializing Bot, Please wait...{endc}\n")
    time.sleep(2)
    print(f'{green}Cogs loaded... Bot is now ready and waiting for prefix "."{endc}')

    print(f'{green}\n√ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √  {endc}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Lava | !help"))
    return

@bot.command(name='reload',
			 description='Reloads bot',
			 aliases=['-r'],
			 hidden=True,
			 case_insensitive=True)
async def reload(ctx):
	# await ctx.channel.purge(limit=int(1))
	""" Reloads cogs while bot is still online """
	user = ctx.author
	roles = ctx.message.author.roles
	server_id = ctx.guild.id
	updated_cogs = ''
	#clearterm()
	l = len(cogs)
	#await add_command(ctx.guild.id)
	printProgressBar(0, l, prefix = '\nInitializing:', suffix = 'Complete', length = 50)
	for i, cog in enumerate(cogs):
		printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
		bot.unload_extension(cog)
		#print("Reloading", cog)
		bot.load_extension(cog)
		updated_cogs += f'{cog}\n'
	print((f"\nInitializing Bot, Please wait...\n", "purple"))
	print((f'Cogs loaded... Bot is now ready and waiting for prefix "."', "green"))
	await ctx.send(f"`Cogs reloaded by:` <@{user.id}>")
                  
keep_alive.keep_alive()
bot.run(TOKEN, bot=True, reconnect=True)     

