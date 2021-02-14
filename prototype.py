import discord, matplotlib.pyplot as plt, numpy as np
import random
from math import *
from discord.ext import commands
import database
import search

client = discord.Client()

intents = discord.Intents.all()
intents.members = True  
client = commands.Bot(command_prefix='~', intents=intents)
# testing server id: 810149199488352256

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

questions = []
q = ['']

@client.event
async def on_message(message):
  id = client.get_guild(810149199488352256)
  guild = client.get_guild(810149199488352256)

  if message.author == client.user:
    return

  ########################## BASIC FUNCTIONALITIES ##############################

  # SAYING HI
  if message.content.startswith('~hi'):
    await message.channel.send("hey")
  
  # MAKING AN ANNOUNCEMENT
  if message.content.startswith('~announcement'):
    await message.channel.purge(limit=1)
    await message.channel.send(f"@everyone\n```diff\n+Announcement\n{message.content[14:]}```")

  # ASSEMBLE STUDENTS AT THE SAME CLASSROOM
  if message.content.startswith('~assemble') and 'Professor' in str(message.author.roles):
    channel = client.get_channel(810226322625265704) 
    member = message.author
    for member in guild.members:
      if 'Student' in str(member.roles):
        try:
          await member.move_to(channel)
        except:
          pass
  
  # PUT STUDENTS INTO BREAKOUT ROOMS
  if message.content.startswith('~breakout') and 'Professor' in str(message.author.roles):
    for member in guild.members:
      if 'Student' in str(member.roles):
        if random.random() < 0.3333:
          channel = client.get_channel(810214075912421427) 
        elif random.random() < 0.6666:
          channel = client.get_channel(810214372592713759)
        else:
          channel = client.get_channel(810214406636961854)
        try:
          await member.move_to(channel)
        except:
          pass
  
  # MUTES EVERY STUDENT
  if message.content.startswith('~mute') and 'Professor' in str(message.author.roles):
    for member in guild.members:
      if 'Student' in str(member.roles):
        try:
          await member.edit(mute=True)
        except:
          pass

  # UNMUTES EVERY MEMBER
  if message.content.startswith('~unmute') and 'Professor' in str(message.author.roles):
    for member in guild.members:
      try:
        await member.edit(mute=False)
      except:
        pass

  # CREATES A QUESTION DATABASE
  if message.content.startswith('~question'):
    questions.append(message.content[10:])
    questions.append(message.author)

  # SHOWS THE QUESTIONS 
  if message.content.startswith('~show_questions'):
    q[0] = ''
    for i in range(0, len(questions) - 1, 2):
      q[0] += f"{str(int(i/2 + 1))}: {questions[i]} | {questions[i+1]}\n"
    await message.channel.send(f"```{q[0]}```")

  # ANSWERS A QUESTION
  if message.content.startswith('~answer'):
    index = (int(message.content.split()[1]) - 1) * 2
    await message.channel.send(f"{questions[index + 1].mention} here is the answer to *'{questions[index]}'* : {message.content[9:]}")
    questions.pop(index)
    questions.pop(index)

  # CREATE A POLL
  if message.content.startswith('~poll'):
    await message.add_reaction('👍')
    await message.add_reaction('👎')

  # SEARCH ENGINE
  if message.content.startswith('~search'):
    await message.channel.send(search.communicate(message.content[8:]))

  # ADD ASSIGNMENT TO CALENDAR
  if message.content.startswith('~assignment'):
    event, deadline = message.content.split()[1], message.content.split()[2]
    database.insert_event(event, deadline)

  # SEE CALENDAR
  if message.content.startswith('~see_assignments'):
    await message.channel.send(database.print_calendar())
      

  ########################## INTEGRATED CALCULATOR ##############################

  # ADDITION
  if message.content.startswith('~add'):
    a, b = int(message.content.split()[1]), int(message.content.split()[2])
    await message.channel.send(str(a + b))

  # SUBTRACTION
  if message.content.startswith('~sub'):
    a, b = int(message.content.split()[1]), int(message.content.split()[2])
    await message.channel.send(str(a - b))

  # MULTIPLICATION
  if message.content.startswith('~mult'):
    a, b = int(message.content.split()[1]), int(message.content.split()[2])
    await message.channel.send(str(a * b))

  # DIVISION
  if message.content.startswith('~div'):
    a, b = int(message.content.split()[1]), int(message.content.split()[2])
    await message.channel.send(str(a / b))

  # MARK~
  if message.content.startswith('~mark'):
    a, b = int(message.content.split()[1]), int(message.content.split()[2])
    await message.channel.send(f"{str(round(100 * (a / b), 2))}%")

  # SQUARE ROOT 
  if message.content.startswith('~sqrt'):
    a = int(message.content.split()[1])
    await message.channel.send(f"{str(a ** (1/2))}")

  # POWER 
  if message.content.startswith('~pow'):
    a, b = int(message.content.split()[1]), int(message.content.split()[2])
    await message.channel.send(str(a ** b))

  # AVERAGE
  if message.content.startswith('~avg'):
    total = 0;
    for number in message.content.split()[1:]:
      total += int(number)
    await message.channel.send(str(total / len(message.content.split()[1:])))

client.run('Token Goes Here')
