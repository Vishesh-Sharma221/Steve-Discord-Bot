import discord
from discord.ext import commands
import asyncio
import cogs
from discord.utils import get

class afk(commands.Cog):
    def __init__(self,bot,*args,**kwargs):
        self.bot = bot
        self.bot.afks = {}

    @commands.command()
    async def afk(self,ctx,* ,reason="Nothing"):
        member  = ctx.author
        try:
            await asyncio.sleep(2.0)
            self.bot.afks[member.id] = [ctx.guild.id,reason]
            await member.edit(nick=f"(AFK) {member.nick}") 
        except:
            pass

        embed = discord.Embed(title=":zzz:", description=f" **{member.nick}** has gone **AFK** ", color = member.color)  
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name="**AFK NOTE** : ", value = reason)
        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self,message):
        for i in self.bot.afks.values():
            if message.guild.id in i:
                if message.author.id in self.bot.afks.keys():
                    self.bot.afks.pop(message.author.id)
                    try:
                        await message.author.edit(nick=str(message.author.nick)[6:])
                    except Exception as e:
                        print(e)
                    await message.channel.send(f"Welcome Back! **{message.author.nick}** , I removed your AFK!")

                for id, g_r in self.bot.afks.items():
                    reason = g_r[1]
                    member = get(message.guild.members, id = id)
                    try:
                        if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                            await message.reply(f"**{member.name}** is AFK! ; **NOTE** : {reason}")
                    except Exception as e:
                        print(e)
def setup(bot):
    bot.add_cog(afk(bot))
    print("Loaded afk command!")