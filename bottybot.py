import discord
import os
from numpy import random
import asyncio
from discord.ext import commands
from config import config
from dotenv import load_dotenv

#loads discord token from 'acc.env'
load_dotenv('acc.env')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents)
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
    if message.content in config.bother:
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
                                      "\n- help: shows this message\n"
                                      "- hentai: for me to DM a random comic to you ;)\n"
                                      "- howgay: to measure your gayness\n"
                                      "- id: request ID of another person\n"
                                      "- profile: Shows information about mentioned user\n"
                                      "- echo: Checks if command execution is working\n"
                                      "- invite: Links the invite to the server\n"
                                      "- report: Used to report members\n"
                                      "- chonk: Used for chonk\n"
                                      "- ban: Bans mentioned user\n"
                                      "- unban: Unbans give user, name#1234 format\n"
                                      "- kick: Kicks mentioned user\n"
                                      "- clear: Clears up to 10 messages", color=discord.Color.purple())

    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url=bot.user.avatar_url)

    await ctx.channel.send(embed=embed)

#shows ID of mentioned user
@bot.command(name='id')
async def id(ctx, member: discord.Member):
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
    embed.add_field(name="**User ID**", value=str(personid),
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
    if ctx.author.id == config.ungayid:
        x = 0
    embed = discord.Embed(title="Sheeeeeeesh",
                          description="<@" + str(ctx.author.id) + "> is " + str(x) + "% gay.",
                          color=discord.Color.purple())
    await ctx.channel.send(embed=embed)

#this command is just there to see if somethings blocking command execution, idk it helped me
@bot.command(name='echo')
async def echo(ctx):
    embed = discord.Embed(title="Code 200",
                          description="Command execution works!",
                          color=discord.Color.purple())

    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url)

    await ctx.channel.send(embed=embed, delete_after=5)

#a command to request the invite link to your server, put link in config file
@bot.command(name='invite')
async def invite(ctx):
    embed = discord.Embed(title="????Here is the server invite!????",
                                description="Thanks for inviting new members!\n"
                                           + config.invitelnk,
                                color=discord.Color.purple())
    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url)
    await ctx.channel.send(embed=embed)

#can send reports with reasons to a specified channel for mods
@bot.command(name='report')
async def report(ctx, member : discord.Member, *, args = None):
    repid = member.id
    if args == None:
        embed = discord.Embed(title="Reason required",
                              description="Please provide a reason for your report. Like @Member + reason",
                              color=discord.Color.purple())
        await ctx.channel.send(embed=embed, delete_after=5)
    else:
        channel = await bot.fetch_channel(config.mod_channel)
        embed = discord.Embed(title="Report Submitted",
                              description="<@" + str(ctx.author.id) + ">" + " reported <@" + str(repid) + "> for " + "".join(args[:]) + ".",
                              color=discord.Color.purple())
        await channel.send(embed=embed)

#he is thicc
@bot.command(name='chonk')
async def chonk(ctx):
    embed = discord.Embed(title="Chonkers.",  color=discord.Color.purple())
    embed.set_image(url=config.chonklnk)
    await ctx.channel.send(embed=embed)

#Bans if you have the ban perm
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="User banned",
                          description=f'{member} has been banned by ' + "<@" + str(ctx.author.id) + ">",
                          color=discord.Color.purple())
    await ctx.channel.send(embed=embed, delete_after=5)
    await member.ban(reason=reason)

#unbans if you have the ban perm
@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            embed = discord.Embed(title="User unbanned",
                                  description=f"{user.mention} has been unbanned",
                                  color=discord.Color.purple())
            await ctx.channel.send(embed=embed, delete_after=5)
            await ctx.guild.unban(user)

#Kicks if you have the kick perm
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="User kicked",
                            description=f'{member} has been kicked by ' + "<@" + str(ctx.author.id) + ">",
                            color=discord.Color.purple())
    await ctx.channel.send(embed=embed, delete_after=5)
    await member.kick(reason=reason)

#clears messages up to 10 messages per command, if you go higher things will start to break, bc discord is stoopid
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount):
    mlimit = 10
    amount = int(amount)
    if (amount > mlimit):
        embed = discord.Embed(title="Exceeded deletion limit",
                              description="The limit of messages to be deleted is 10",
                              color=discord.Color.purple())
        await ctx.channel.send(embed=embed, delete_after=5)

    else:
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Messages cleared!",
                              description="Deleted the last " + str(amount) + " messages",
                              color=discord.Color.purple())
        await ctx.channel.send(embed=embed, delete_after=5)

#runs bot
bot.run(DISCORD_TOKEN)
