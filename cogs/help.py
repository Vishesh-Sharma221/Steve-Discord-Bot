import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self,ctx):
        member = ctx.author
        await ctx.message.add_reaction("<:tick:860371854689959966>")

        embed = discord.Embed(
            title="Hi! Read the embed to see how to use me :slight_smile:",
            colour=discord.Colour.blue()
        )
        embed.add_field(
            name="**My prefix :**", value="`s!`", inline=False)
        embed.add_field(
            name="**Moderation Commands:**", value="`clear/kick/ban`", inline=True)
        embed.add_field(
            name="**clear:**", value="`s!clear [number of messages u wanna clear]`")
        embed.add_field(
            name="**kick/ban**", value="`s!kick [user] or s!ban [user]`", inline=True)
        embed.add_field(
            name="**Ask questions from steve :**", value='`s!steve [question]`', inline=True)
        embed.add_field(
            name="**talk to steve:**", value="`s!hi/hello/bye`", inline=True)
        embed.add_field(
            name="**ping**", value="`returns pong :)`", inline=True)
        embed.add_field(
            name="**snipe and editsnipe**", value="`s!snipe and s!editsnipe to expose the last deleted or edited message`", inline=True)
        embed.add_field(
            name="**reddit**", value="`s!m for random memes, s!m {a topic} for topic-wise memes :wink:`", inline=True)
        embed.add_field(
            name="**truth n dare**", value="`s!t or s!truth (dare commands coming soon)`", inline=True)
        embed.add_field(
            name="**hug/kiss/pat**", value="`s!hug / s!kiss / s!pat`", inline=True)
        embed.add_field(
            name="**Timer**", value="`s!timer {seconds}`", inline=True)
        embed.add_field(
            name="**check someone's avatar**", value="`s!avatar`", inline=True)
        embed.add_field(
            name="**Get any gif from giphy**", value="`s!gif {the gif u want}`", inline=True)
        embed.add_field(
            name="**Jokes/facts**", value="`s!jokes` and `s!facts`", inline=True)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.set_footer(text="Have a nice one :)")

        await member.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))
    print("Loaded help commands!")