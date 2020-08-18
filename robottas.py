import os
import random
import json

import discord
from discord import guild
from discord.ext import commands
from dotenv import load_dotenv
import settings

from ir_profile_tracker.irClient import IrClient
from pyracing.client import Client
from ir_profile_tracker.models import RaceType
from ir_profile_tracker.models import SR

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

client = Client(settings.IRACING_EMAIL, settings.IRACING_PASSWORD)


@bot.event
async def on_ready(self):
    # print information of which server bot is connected to
    print(f'{self.user} has connected to {guild.name}')


# print details of connected server
@bot.event
async def on_ready():
    for bot.guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to following guild: \n'
        f'{guild.name}(id: {guild.id})\n'
    )

    # get server member details
    members = '\n - '.join([member.name for member in guild.members])
    # print server member details
    print(f'Server members:\n - {members}')


# print information that bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready')


# welcome new members with a direct message
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f' We\'re happy to have you on the team, {member.name}. Make the most of Robottas by saying !help')


# respond to user messages with a selection of different lines
@bot.command(name='go', help='Responds with racing related comments')
async def go_time(ctx):
    name = ctx.author.name

    lines = [
        'Do you need to pit for fresh tyres?',
        'OK ' + name + ', you need to push now',
        'Can you get any faster?',
        'Better luck next time',
        'It\'s lights out, and away we go!',
        'Blue flags, blue flags!',
        'Fernando is faster than you, can you confirm you understood that message?',
        name + ', are you OK?',
        'Great job ' + name + ', that\'s another fastest lap'
    ]

    # assign trigger word for random responses
    response = random.choice(lines)
    await ctx.send(response)


# bot command to fetch iracing stats by account ID
@bot.command(name='stats', help='get a drivers iRacing data with account ID. Race types:\n'
                                f'Oval = 1\n'
                                f'Road = 2\n'
                                f'Dirt Oval = 3\n'
                                f'Dirt Road = 4')
async def display_stats(ctx, member_id):
    embed = discord.Embed(
        title='Career Stats',
        description='These are the iRacing stats for the given driver',
        colour=discord.Colour.red()

    )
    stats = await client.career_stats(member_id)
    embed.add_field(name='Stats', value='TODO - tähän arvo')

    # sends stat-objects as a message, not the stat values
    await ctx.send(stats)


# bot command to get the results of the last race - WORK IN PROGRESS
@bot.command(name='lastrace', help='Get the results of your last race, argument member ID. Work in progress')
async def last_races(ctx, member_id):
    embed = discord.Embed(
        title='Last races',
        description='These are the latest results for the given driver',
        colour=discord.Colour.red()
    )

    races = await client.last_races_stats(member_id)
    response = {}
    for race in races:
        print(race.__dict__)
        embed.add_field(name='Date', value=race.date, inline=True)
        embed.add_field(name='Incidents', value=race.incidents, inline=True)
        embed.add_field(name='Laps led', value=race.laps_led, inline=True)
        embed.add_field(name='Championship points', value=race.points_champ, inline=True)
        embed.add_field(name='Club points', value=race.points_club, inline=False)
        embed.add_field(name='Finish position', value=race.pos_finish, inline=False)
        embed.add_field(name='Start position', value=race.pos_start, inline=False)
        embed.add_field(name='Series ID', value=race.series_id, inline=False)
        embed.add_field(name='Strength of field', value=race.strength_of_field, inline=False)
        embed.add_field(name='Subsession ID', value=race.subsession_id, inline=False)
        embed.add_field(name='Track name', value=race.track, inline=False)
        embed.add_field(name='Winner', value=race.winner_name, inline=False)

    await ctx.send(embed=embed)


# run the bot
bot.run(TOKEN)
