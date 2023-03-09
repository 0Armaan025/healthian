import discord
import json
import os
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents = intents)

user_data = {}

food_database = {
    'apple': {
        'name': 'apple',
        'calories': 95
    },
    'banana': {
        'name': 'banana',
        'calories': 105
    },
    'broccoli': {
        'name': 'broccoli',
        'calories': 55
    },
    'carrot': {
        'name': 'carrot',
        'calories': 30
    },
    'chicken breast': {
        'name': 'chicken breast',
        'calories': 165
    },
    'eggs': {
        'name': 'eggs',
        'calories': 155
    },
    'salmon': {
        'name': 'salmon',
        'calories': 245
    },
    'spinach': {
        'name': 'spinach',
        'calories': 7
    }
}

@bot.command(name='logfood')
async def log_food(ctx, *, food_query):
    food = None
    for key in food_database.keys():
        if food_query.lower() == key:
            food = food_database[key]
            break

    if food:
        await ctx.send(f"How much {food['name']} did you eat? (in grams)")
        try:
            response = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            amount = int(response.content)
    
            if str(ctx.author.id) not in user_data:
                user_data[str(ctx.author.id)] = []
            user_data[str(ctx.author.id)].append({
                'food': food,
                'amount': amount,
                'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            })
            await ctx.send(f"Logged {amount}g of {food['name']}.")
        except:
            await ctx.send("Sorry, I didn't get a response in time.")
    else:
        await ctx.send("Sorry, I don't have information about that food.")

@bot.command()
async def info(ctx):
    await ctx.send(f"_This app is created by **Armaan** for **GHW SOCIAL WEEK GOOD**, we focus on providing user with **how much food they eat** so that they can have a proper diet and not be a victim of diseases_");        

@bot.command(name='calories')
async def get_calories(ctx):
    if str(ctx.author.id) not in user_data:
        await ctx.send("You haven't logged any food yet.")
    else:
        total_calories = sum([item['food']['calories'] * item['amount'] / 100 for item in user_data[str(ctx.author.id)]])
        await ctx.send(f"You have consumed {round(total_calories)} calories today.")

bot.run('xxxxxxx')