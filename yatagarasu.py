from discord.ext import tasks,commands
from discord.utils import get
import discord
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

initial_extension = ['cogs.balance','cogs.mod']



bot = commands.Bot(command_prefix=".")

cmdPre = bot.command_prefix

if __name__ == '__main__':
	for extension in initial_extension:
		bot.load_extension(extension)
	
date = 0
joinedH = 0
joinedM = 0
joinedS = 0

@bot.event
async def on_ready():
	print(f"{bot.user.name} has joined")
	date = datetime.datetime.now()
	joinedH = date.hour
	joinedM = date.minute
	joinedS = date.second

Admin = 721232246186573876
BotChannel = 721371169176944651

@bot.check
def custom_check(ctx):
	if str(Admin) in str(ctx.author.roles) and str(ctx.channel.id) not in str(BotChannel):
		return True
	elif str(ctx.channel.id) not in str(BotChannel):
		return False
	else:
		return True

@bot.event
async def on_member_join(member):
	channel = bot.get_channel(721229234894274630)
	await member.add_roles(get(member.guild.roles,id=721969975446863872))
	await channel.send(f"Welcome {member.mention}, We hope you have fun here!")
	print("Member Joined")

@bot.event
async def on_member_remove(member):
	channel = bot.get_channel(721229234894274630)
	await channel.send(f"**{member}** has just left the server, Goodbye!")
	print("Member leaves")


@bot.command()
@commands.has_role("Admin")
async def test(ctx):
	print([i.name for i in ctx.author.roles])
	print([i.name for i in ctx.guild.members])
	print(cmdPre)

@bot.command()
@commands.has_role("Admin")
async def clear(ctx, msg:int):
	channel = ctx.channel
	deleted = await channel.purge(limit=msg)
	card = discord.Embed(
	colour = discord.Colour.from_rgb(129,255,129),
	description=f"Successfully deleted {len(deleted)} message"
	)
	await ctx.send(embed=card,delete_after=3)
	
@bot.command(name='dc')
@commands.has_role("Admin")
async def disconnect(ctx):
	card = discord.Embed(
	colour=discord.Colour.from_rgb(120,255,120),
	)
	card.set_author(name="Disconnected!",icon_url=bot.user.avatar_url)
	await ctx.send(embed=card)
	await bot.logout()

@tasks.loop(seconds=10)
async def getMember(ctx):
	print([i.name for i in ctx.guild.members])

@bot.command()
@commands.has_role("Admin")
async def run(ctx):
	card = discord.Embed(
	color=ctx.author.color,
	)
	card.set_author(name="Running loops",icon_url=ctx.author.avatar_url_as(static_format='png'))
	getMember.start(ctx)
	await ctx.send(embed=card)
	ctx.command.enabled = False

@bot.command(aliases=["stats","stat"])
@commands.has_role("Admin")
async def status(ctx):
	now = datetime.datetime.now()
	print(now.hour)
	card = discord.Embed(
	colour=ctx.author.color,
	description=f"Bot has been active since {int(now.hour)-int(joinedH)}h {int(now.minute)-int(joinedM)}m {int(now.second)-int(joinedS)}s ago!"
	)
	await ctx.send(embed=card)
	
			
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, (commands.MissingRole,commands.MissingAnyRole,)):
		card = discord.Embed(
		colour = discord.Colour.from_rgb(255,0,0),
		description="Missing Role: Admin"
		)
		await ctx.send(embed=card)
	elif isinstance(error, commands.CheckFailure):
		card = discord.Embed(
		colour=discord.Colour.from_rgb(255,0,0),
		description="You cannot use command on this channel!"
		)
		await ctx.send(embed=card)
	else:
		raise error



bot.run(TOKEN)