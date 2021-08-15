import discord 
from discord.ext import commands
import random 
import cogs
import os 


from cogs import tnd_resources
from cogs.tnd_resources import *

class tnd(commands.Cog):
    def __init__(self,bot,*args,**kwargs):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message):         
        if message.content.startswith('<@!806453196205064192> ,') or message.content.startswith('<@806453196205064192> ,'):
            if "what" in message.content.lower():
                await message.channel.send(random.choice(what))
            elif "why" in message.content.lower():
                await message.channel.send(random.choice(why))
            elif "developer" in message.content.lower():
                await message.channel.send(random.choice(dev))
            elif "no" in message.content.lower():
                await message.channel.send(random.choice(no))
            elif "yes" in message.content.lower():
                await message.channel.send(random.choice(yes))
            elif "ok" in message.content.lower():
                await message.channel.send(random.choice(ok))
            elif "stfu" in message.content.lower():
                await message.channel.send(random.choice(stfu))
            elif "do" in message.content.lower():
                await message.channel.send(random.choice(do))
            elif "when" in message.content.lower():
                await message.channel.send(random.choice(when))
            elif "you" in message.content.lower() or "u" in message.content.lower():
                await message.channel.send(random.choice(you))
            elif "are you" in message.content.lower():
                await message.channel.send(random.choice(are_you))
            elif "can you" in message.content.lower():
                await message.channel.send(random.choice(can_you))
            elif "can i" in message.content.lower():
                await message.channel.send(random.choice(can_i))
            else:
                await message.channel.send(random.choice(misc))

        elif message.content.startswith('<@!806453196205064192>') or message.content.startswith('<@806453196205064192>'):
            await message.channel.send(f"Hi! My prefix is `s!` or just use me by mentioning me, For any help you can use `s!help`")

    @commands.command(aliases=["t"])
    async def truth(self,ctx):
        await ctx.send(random.choice(truths))

    @commands.command(aliases=["P"])
    async def paranoia(self,ctx,*,member:discord.Member):
        await ctx.send("Check DMs !")

        ques = random.choice(paranoia)
        embed = discord.Embed(title="Question",description=ques, colour=discord.Color.orange())
        await member.send(embed=embed)
        await member.send("Answer this question here !")

        def check(m):
            return m.author == ctx.author and not m.guild

        lis = ["Kept Secret!" , random.choice(ques)]
        msg = await self.bot.wait_for('message', check=check)
        await ctx.send(f'''The Question is Kept Secret!
        {msg.author.name} said '{msg.content}' ''')
            


 
def setup(bot):
    bot.add_cog(tnd(bot))
    print("Loaded steve and tnd commands!")