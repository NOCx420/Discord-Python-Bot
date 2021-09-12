import discord
import os
from numpy import random
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
import asyncio
from config import config
from dotenv import load_dotenv

#loads discord token from 'acc.env'
load_dotenv('acc.env')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "-", intents=intents)
bot.remove_command('help')

#changes status. The values are in config.py
async def status_task():
    while True:
        await asyncio.sleep(60)
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(random.choice(config.status)))

@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print('We have logged in as {0.user}'.format(bot))


#Personal feature, you can delete if you want. Its basically if someone types my name
#it pings me that someone wants to annoy me. Values in config.py
@bot.listen('on_message')
async def no(message):
    if  message.content in config.bother:
        await message.channel.send(config.no)

    if message.author == bot.user:
        return

#error handler, not much to say
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Invalid Argument",
                          description="Please enter a valid argument :l",
                          color=discord.Color.purple())
        await ctx.channel.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="420 Member Not Found",
                          description="I can't seem to find that member",
                          color=discord.Color.purple())
        await ctx.channel.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Insufficient Permission",
                          description="You don't have the required Permissions :l",
                          color=discord.Color.purple())
        await ctx.channel.send(embed=embed)

#chunky help command
@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="__**Commands**__",
                          description="Use - to execute the commands listed below:\n"
                                      "\n- help: shows this message\n- hentai: for me"
                                      " to DM a random comic to you ;)\n- myid: to req"
                                      "uest your Discord ID (Good for dev)\n- howgay: "
                                      "to measure your gayness\n- id: request ID of another person"
                                      "\n- profile: shows information about mentioned user\n"
                                      "- echo: check if command execution is working(I use this a lot\n"
                                      "- invite: links the invite to the server)\n"
                                      "- report: usage: -report @MEMBER REASON", color=discord.Color.purple())

    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url=bot.user.avatar_url)

    await ctx.channel.send(embed=embed)

#shows your ID
@bot.command(name='myid')
async def myid(ctx):
        authid = ctx.author.id
        embed = discord.Embed(title="__**ID**__",
                              description="Your Discord ID is: " + str(authid),
                              color=discord.Color.purple())

        embed.set_author(name=ctx.author,
                         icon_url=ctx.author.avatar_url)

        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

#shows ID of mentioned user
@bot.command(name='id')
async def id(ctx, member : discord.Member):
    person = member
    personname = f"{member}"
    personid = member.id
    embed = discord.Embed(title="__**ID**__",
                          description=f"The Discord ID of {member} is: " + str(personid),
                          color=discord.Color.purple())

    embed.set_author(name=personname,
                     icon_url=person.avatar_url)

    embed.set_thumbnail(url=person.avatar_url)
    await ctx.channel.send(embed=embed)

#more detailed information on mentioned user
@bot.command(name="profile")
async def profile(ctx, *, member : discord.Member):
    person = member
    personname = f"{member}"
    personid = member.id
    top_role = member.top_role.id
    role = discord.utils.get(ctx.guild.roles,
                             id=top_role)

    embed = discord.Embed(description=person.mention,
                          color=discord.Color.purple())

    embed.set_author(name=personname,
                     icon_url=person.avatar_url)

    embed.set_thumbnail(url=person.avatar_url)
    embed.add_field(name="**User ID**", value=personid,
                    inline=False)

    embed.add_field(name="**Joined Discord**",
                    value=person.created_at.__format__('%A, %d. %B %Y @ %H:%M'),
                    inline=False)
    embed.add_field(name="**Joined Server**",
                    value=person.joined_at.__format__('%A, %d. %B %Y @ %H:%M'),
                    inline=False)
    embed.add_field(name="**Highest Role**",
                    value=role.mention,
                    inline=False)

    await ctx.channel.send(embed=embed)

#The first command I made. It may seem stupid, but this was the most useful command I could
#come up with. Tho I learned a lot, this was the only thing I could do at the time
@bot.command(name='hentai')
async def hentai(ctx):
    limit = 1
    x = limit + random.randint(550000)
    num = str(x)
    embed = discord.Embed(title="Here is your link:",
                          description="https://www.nhentai.net/g/" + num,
                          color=discord.Color.purple())
    await ctx.author.send(embed=embed)

#I saw a bot do this so I wanted it myself
@bot.command(name='howgay')
async def howgay(ctx):
    x = random.randint(100)
    embed = discord.Embed(title="Sheeeeeeesh",
                          description="<@" + str(ctx.author.id) + ">" " you are " + str(x) + "% gay.",
                          color=discord.Color.purple())
    await ctx.channel.send(embed=embed)

#this command is just there to see if somethings blocking command execution, idk it helped me
@bot.command(name='echo')
async def echo(ctx):
    embed = discord.Embed(title="Code 200 Boi",
                          description="Command execution seems to be working as far as this one goes,"
                                      " if the other ones don't work than that's gonna be a pain in the ass to fix",
                          color=discord.Color.purple())

    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url)

    await ctx.channel.send(embed=embed)

#a command to request the invite link to your server, put link in config file
@bot.command(name='invite')
async def invite(ctx):
    embed = discord.Embed(title="🍞Here is the server invite!🍞",
                                description="Thanks for inviting new members!\n"
                                           + config.invitelnk,
                                color=discord.Color.purple())
    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command(name='report')
async def report(ctx, member : discord.Member, *, args):
    repid = member.id
    if args == None:
        embed = discord.Embed(title="Reason required",
                              description="Please provide a reason for your report.",
                              color=discord.Color.purple())
        ctx.channel.send(embed)
    channel = await bot.fetch_channel(config.mod_channel)
    embed = discord.Embed(title="Report Submitted",
                          description="<@" + str(ctx.author.id) + ">" + " reported <@" + str(repid) + "> for " + "".join(args[:]) + ".",
                          color=discord.Color.purple())
    await channel.send(embed=embed)

bot.run(DISCORD_TOKEN)
