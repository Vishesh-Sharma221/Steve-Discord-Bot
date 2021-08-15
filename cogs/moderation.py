import discord 
from discord.ext import commands
import random 
import time 
import asyncio 
import cogs

class ModCog(commands.Cog):
    def __init__(self,bot,*args,**kwargs):
        self.bot = bot

    @commands.command()
    async def clear(self,ctx, ammount=0):
        try:
            if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
                if ammount == 0:
                    await ctx.send("Ok, How many you want?")
                else:
                    await ctx.channel.purge(limit= ammount+1)
                    msg = await ctx.send(f"cleared {ammount} messages!") 
                    await asyncio.sleep(10)
                    await msg.delete()
            else:
                await ctx.send('Sorry you are not allowed to use this command!')
        except:
            await ctx.send('Sorry you are not allowed to use this command!')

    @commands.command()
    async def kick(self,ctx,member:discord.Member, reason = None):
        if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
            await member.kick(reason=reason)
            await ctx.send(f"Succesfully Kicked {member}! **REASON**{reason}")
            await asyncio.sleep(10)
            await msg.delete()
        else:
            await ctx.semd('Sorry you are not allowed to use this command!')

    @commands.command()
    async def ban(self,ctx,member:discord.Member, reason = None):
        if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
            await member.ban(reason=reason)
            await ctx.send(f"Succesfully banned {member}! **REASON**{reason}")
            await asyncio.sleep(10)
            await msg.delete()
        else:
            await ctx.send('Sorry you are not allowed to use this command!')



def setup(bot):
    bot.add_cog(ModCog(bot))
    print("Loaded moderation commands!")