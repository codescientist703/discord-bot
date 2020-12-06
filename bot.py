import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from replit import db
import requests
import random
import asyncio
import datetime
load_dotenv()
import keep_alive

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

help_command = commands.DefaultHelpCommand(
    no_category = 'All Commands',
)
bot = commands.Bot(command_prefix='#', help_command=help_command)


# Events
# 8 o'clock in the morning, UTC
time_for_thing_to_happen = datetime.time(hour=2, minute=30)


def get_problem():
    current_date = datetime.datetime.today().weekday()
    ans = ''
    if current_date in db.keys():
      ans = db[current_date]['content']
      del db[current_date]
    
    return ans


async def fetchproblem():
    while True:
        now = datetime.datetime.utcnow()
        date = now.date()
        if now.time() > time_for_thing_to_happen:
            date = now.date() + datetime.timedelta(days=1)
        then = datetime.datetime.combine(date, time_for_thing_to_happen)
        await discord.utils.sleep_until(then)
        print("pork o clock")
        problem = get_problem()     
        channel = bot.get_channel(776472204584943669)
        if problem != '':
          await channel.send(problem)
    

# errors in tasks raise silently normally so lets make them speak up


def exception_catching_callback(task):
    if task.exception():
        task.print_stack()


@bot.event
async def on_ready():
    task = asyncio.create_task(fetchproblem())
    task.add_done_callback(exception_catching_callback)
    print(datetime.datetime.utcnow())
    print(f'{bot.user.name} has connected to Discord!')


@ bot.event
async def on_member_update(before, after):

    if str(before.status) == "online":
        if str(after.status) == "offline":
            for channel in before.guild.channels:
                if channel.name == 'general':
                    await channel.send("{} has gone {}.".format(after.name, after.status))

    else:
        if str(after.status) == "online":
            for channel in before.guild.channels:
                if channel.name == 'general':
                    await channel.send("The legend {} has returned after a long journey.".format(after.name))


@ bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    message_content = message.content.lower()
    if 'bengt' in message.content.lower():
        await message.channel.send(f'How can the slave of Master AgentX help you {message.author.mention} ?')

    elif 'rating' in message_content:
        lst = ['down', 'low', 'decreases', 'decrease', 'fall', 'less', 'rip']
        for items in lst:
            if items in message_content:
                await message.channel.send(file=discord.File('rip.jpg'))
                break

    await bot.process_commands(message)

# Commands


@ bot.command(help='Generate a random joke')
async def joke(ctx):
    URL = 'http://api.icndb.com/jokes/random'
    r = requests.get(url=URL)
    data = r.json()
    joke = data['value']['joke']
    guild = ctx.guild
    names = [member.mention for member in guild.members]
    njoke = joke.replace('Chuck Norris', random.choice(names))
    await ctx.send(njoke)
    await ctx.message.delete()


@ bot.command(help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
    await ctx.message.delete()


@ bot.command(help='See when a user joined discord')
async def joined(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at}'.format(member))
    await ctx.message.delete()


@ bot.command(help='Delete last 5 messages')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@ bot.command(help='Add a problem for a specific date')
async def daily(ctx, statement, url, type, difficulty, date):
    emoji = '<:octagonal_sign:784716297413328898>'
    content = f"""
    {emoji*30} \n
    Hey @everyone, here is today's problem!
    **Description**: {statement} \n
    **Link**: {url}
    **Type**: {type}
    **Difficulty**: {difficulty}
    """
    data = {
      'content': content,
      'author': ctx.message.author.name,
    }
    db[date] = data
    await ctx.send(f'Problem successfully added by {ctx.message.author.mention}')
    await ctx.message.delete()


@ bot.command(help='Displays the schedule')
async def schedule(ctx):
    result = "``Date  Author \n"
    for row in db.keys():
      result += " " + row + "    " + db[row]['author'] + "  " + '\n'

    result += "``"
    await ctx.send(result)
    await ctx.message.delete()

@ bot.command(help='Delete a particular date schedule')
async def delete(ctx, date):
    if date in db.keys():
      del db[date]
      await ctx.send(f'Problem successfully deleted by {ctx.message.author.mention}  for the date- {date}')
    else:
      await ctx.send(f'No problem schedule found for the date- {date}')

    await ctx.message.delete()

    
   

keep_alive.keep_alive()
bot.run(TOKEN)
