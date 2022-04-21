import discord
import json
import random
import aiohttp
from discord.ext import commands
from keep_alive import keep_alive
intents = discord.Intents.all()

#client
client = discord.Client()
client = commands.Bot(command_prefix = ".", intents=intents) 

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_member_remove(member, message):
  await message.send(#text here)

@client.event
async def on_message(message):
  if message.author.bot:
    return
  await client.process_commands(message)
  if "#text" in message.content.lower():
    if "#text" in message.content:
      return False
    await message.channel.send("#text")
    return
  elif "#text" in message.content.lower():
    if message.content.lower() != "#text":
      return False
    await message.channel.send("#text")
    return

@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    coins_amt = users[str(user.id)]["coins"]
    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.blue())
    em.add_field(name = "Coins", value =  coins_amt)
    await ctx.send(embed = em)

async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False 
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["coins"] = 0
    with open ("bank.json","w") as f:
        json.dump(users,f)
    return True
        
async def get_bank_data():
    with open ("bank.json","r") as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0,mode = "coins"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open ("bank.json","w") as f:
        json.dump(users,f)
    bal = users[str(user.id)]["coins"]
    return bal

@client.command()
async def give(ctx,member:discord.Member,amount = None):
    await open_account(member)
    if member == ctx.author:
      return False
    if amount == None:
        await ctx.send("#text")
        return 
    await update_bank(member)
    amount = int(amount)
    if amount<0: 
        await ctx.send("#text")
        return
    await update_bank(member,amount,"coins")

@client.command()
async def remove(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("#text")
        return 
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal:
        await ctx.send("#text")
        return
    if amount<0:
        await ctx.send("#text")
        return
    await update_bank(ctx.author,-1*amount,"coins")

@client.command(aliases=["8Ball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.", 
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "I don't know",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "Most likely.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command(aliases=["#text"])
async def inspire(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.quotable.io/random') as q:
            js = await q.json()
            await ctx.send(f' {js["content"]}')

keep_alive() 
#run the client on the server using token
client.run('token')
