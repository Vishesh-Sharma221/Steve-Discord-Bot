import discord
import random
import praw 
import datetime 
import asyncio
import giphy_client
from giphy_client.rest import ApiException
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import randfacts
import pyjokes


from initials import *

reddit = praw.Reddit(client_id = client_id,
                    client_secret =client_secret,
                    username = username,
                    password = password,
                    user_agent = user_agent,
                    check_for_async=False)

from discord.ext import commands
from PIL import Image
from io import BytesIO

intents = discord.Intents.all()
DEFAULT_PREFIX = "s!"

bot = commands.Bot(intents=intents,command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),case_insensitive=True)

bot.remove_command('help')   
now = datetime.datetime.now()

# status = cycle(
#     ['s!help','Hi im steve','s!lol try it :)','You suck lol'])

@bot.event
async def on_ready():
    # change_status.start()
    print('Steve is ready!')
    await bot.change_presence( activity = discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} SERVERS | ECONOMY COMMANDS UNDER MAINTENANCE!"))


# @tasks.loop(seconds=3)
# async def change_status():
#     await bot.change_presence(activity=discord.Game(next(status)))

enabled_cogs = ['afk','help','moderation','tnd']
for cog in enabled_cogs:
  bot.load_extension(f'cogs.{cog}')


colors = [discord.Color.red(), discord.Color.blue(),discord.Color.orange(),discord.Color.green()]
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        em = discord.Embed(title=f"Calm down kid!",description=f"Try again in {error.retry_after:.2f}s.",color = random.choice(colors))
        await ctx.send(embed=em)
    elif isinstance(error,commands.CommandNotFound):
        pass
    elif isinstance(error,commands.errors.CheckFailure):
        await ctx.send("We can do that in a server, not here ")
    else:
        pass

@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None
      
bot.sniped_messages = {}

@bot.event 
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id]=(message.content, message.author, message.channel.name,message.created_at)

@bot.command()
async def snipe(ctx):
    try:
        contents,author,channel_name,time = bot.sniped_messages[ctx.guild.id]
    except:
        await ctx.channel.send("I dont see any recently edited message <:bruh:821754904216600617>")
        return 
    embed = discord.Embed(title="CAUGHT IN 4K",description=contents,color = random.choice(colors),timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text="lol")

    await ctx.channel.send(embed=embed)

editsnipes = dict()
editsnipess = dict()

@bot.event
async def on_message_edit(before, after):
    editsnipes[before.channel] = before
    editsnipess[after.channel] = after

@bot.command()
async def editsnipe(ctx):
    try:
        message = editsnipes[ctx.channel]
        edited_message = editsnipess[ctx.channel]
    except:
        await ctx.channel.send("I dont see any recently edited message <:bruh:821754904216600617>")
        return
    embed = discord.Embed(title="CAUGHT IN 4K",description=f"Changed from **{message.content}** to **{edited_message.content}**" ,color = random.choice(colors),timestamp=message.created_at)

    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_footer(text="Today at " + datetime.datetime.utcnow().strftime('%I:%M %p UTC'))

    await ctx.send(embed=embed)

@bot.command()
async def m(ctx,subred="memes"):
    try:
        subreddit = reddit.subreddit(subred)
        all_subs = []
        hot = subreddit.hot(limit = 30)

        for submission in hot: 
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url 

        embed = discord.Embed(title=name ,color = random.choice(colors))  
        embed.set_image(url = url)
        embed.set_footer(text=f"from r/{subreddit}")
        await ctx.send(embed = embed) 
    except:
        await ctx.send("Subreddit does not exist or something went wrong <:crross:860384058583023616>")

@bot.command()
async def cursed(ctx):
    list1 = ["cursedcomments","cursedimages"]
    subreddit = reddit.subreddit(random.choice(list1))
    all_subs = []
    hot = subreddit.hot(limit = 30)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url 

    embed = discord.Embed(title=name , color = random.choice(colors))  
    embed.set_image(url = url)
    embed.set_footer(text=f"from r/{subreddit}")
    await ctx.send(embed = embed) 

@bot.command(aliases=['av'])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    embed = discord.Embed(title=f"Avatar for {member.name}",description=f"**Link as**\n[png]({member.avatar_url_as(format='png', size=1024)}) | [jpg]({member.avatar_url_as(format='jpg', size=1024)}) | [webp]({member.avatar_url_as(format='webp', size=1024)})", colour=discord.Color.blurple())
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def lol(ctx):
    await ctx.send(file = discord.File("img/tenor.gif"))

@bot.command()
async def elle(ctx):
    await ctx.send(file = discord.File("img/tenor.gif"))

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*100)} ms :ping_pong:')

@bot.command(aliases = ['hey','Hello'])
async def hi(ctx):
    await ctx.send(f'Hi,I am steve how are you? :smile:')

@bot.command() 
async def bye(ctx):
    await ctx.send('Goodbye ! Take care :) :wave:')

@bot.command()
async def facts(ctx):
    x = randfacts.get_fact()
    await ctx.send(f"_{x}_")

@bot.command()
async def jokes(ctx):
    x = pyjokes.get_joke()
    await ctx.send(f"_{x}_")

@bot.command()
async def gif(ctx,*,q="random"):

    api_key="yCdvfFDNGpQ3M501D6z5tG08RIJdSIfO"
    api_instance = giphy_client.DefaultApi()

    try: 
    # Search Endpoint 
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='pg')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=f"here is a {q} gif for you",color = random.choice(colors))
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb) 
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

@bot.command()
async def rip(ctx, user:discord.Member=None):
    if user==None:
        user=ctx.author

    rip=Image.open("img/rip.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((214,250))

    rip.paste(pfp,(64,60))
    rip.save("img/profile.jpg")

    await ctx.send(file = discord.File("img/profile.jpg"))

@bot.command()
async def hug(ctx,*, member : discord.Member):
    
    author_name = ctx.message.author.name

    hugs = ["https://acegif.com/wp-content/gif/anime-hug-38.gif",
            "https://i.imgur.com/r9aU2xv.gif?noredirect",
            "https://i.gifer.com/2QEa.gif",
            "https://1.bp.blogspot.com/-JUqgHJmjyDs/YG76cI82URI/AAAAAAAAD_w/0QtzGkpiel0OlTVEdRCDLmK5Ot46rEq8QCLcBGAsYHQ/s300/romantic%2Banime%2Bhug%2Bgif1.gif",
            "https://gifimage.net/wp-content/uploads/2018/10/anime-girl-hugging-gif-7.gif",
            "https://thumbs.gfycat.com/GratefulComplexGlassfrog-size_restricted.gif",
            "https://media.tenor.com/images/8f44c083c55620c02f59c6bea378dca4/tenor.gif"]

    embed = discord.Embed(title=f'{author_name} hugs {member.display_name}...Aww ', color=random.choice(colors))
    embed.set_image(url = random.choice(hugs))
    await ctx.send(embed=embed)

@bot.command()
async def pat(ctx,*,member : discord.Member):

    author_name = ctx.message.author.name

    pats = ["https://media.tenor.com/images/ad8357e58d35c1d63b570ab7e587f212/tenor.gif",
            "https://media.tenor.com/images/385a8d13c1ee5213e560e07d12320d02/tenor.gif",
            "https://i.pinimg.com/originals/d7/c3/26/d7c326bd43776f1e0df6f63956230eb4.gif",
            "https://i.pinimg.com/originals/2e/27/d5/2e27d5d124bc2a62ddeb5dc9e7a73dd8.gif",
            "https://media.tenor.com/images/374a3ed006e9dd52a874e40a459a9cae/tenor.gif",
            "https://i.imgur.com/d9CH89Q.gif",
            "https://pa1.narvii.com/6401/e11bc915114f632da1d2cc70716b7cb86478c130_hq.gif"]

    embed = discord.Embed(title=f'{author_name} pats {member.display_name}...', color=random.choice(colors))
    embed.set_image(url = random.choice(pats))
    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx,*,member : discord.Member):

    author_name = ctx.message.author.name

    kills = ["https://giffiles.alphacoders.com/696/69649.gif",
            "http://37.media.tumblr.com/8aac647e8c1bae75b43d38991f3945df/tumblr_nah08lNX2V1sijhkdo1_500.gif",
            "https://i.imgur.com/7et8lYx.gif",
            "https://media1.tenor.com/images/3fd96f4dcba48de453f2ab3acd657b53/tenor.gif?itemid=14358509",
            "https://i.gifer.com/ATNm.gif",
            "https://i.pinimg.com/originals/be/4d/f5/be4df5722e9916492e09ef72e109a968.gif",
            "https://i.gifer.com/63P0.gif",
            "https://image.myanimelist.net/ui/D7ahedOlctZp9mcCPCIwK_Ecb3sRiVT2GZ6rB8qrAL0QEJVN4mo6dfFGgTRtIat8dAN_p2cznA6Nqhj_NYCqZkuE1lu2g-YyQoAFLN4cegXTEH6zFIr62Kg5yqrUXSPW"]

    embed = discord.Embed(title=f'{author_name} kills {member.display_name}... RIP', color=random.choice(colors))
    embed.set_image(url = random.choice(kills))
    await ctx.send(embed=embed)

@bot.command()
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 1000:
            await ctx.send("I dont think im allowed to go above 1000 seconds.")
            raise BaseException
        if secondint <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        message = await ctx.send(f"Timer: {seconds}")
        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="Ended!")
                break
            await message.edit(content=f"Timer: {secondint}")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command(aliases=["ttt"])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one dummy")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn......SMH")
    else:
        await ctx.send("Please start a new game using the s!tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Enter a position you would like to mark!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Does this look like an integer to you ..")

@bot.command(pass_context=True)
async def stfu(ctx):
    await ctx.send(file = discord.File("img/stfu.gif"))
    await ctx.message.delete()
@bot.command(pass_context=True)
async def lmao(ctx):
    await ctx.send(file = discord.File("img/funi.png"))
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(manage_channels=True)
@commands.cooldown(2, 10, commands.BucketType.user)
async def rename(ctx, channel: discord.TextChannel, *, new_name):
    await channel.edit(name=new_name)
    await ctx.send(f"Successfully changed to `{new_name}`")


bot.run(token)
