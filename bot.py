import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Prompt builder
def get_prompt(user_input):
    return f"""
You are a Discord chatbot in a gaming server.
Speak Hinglish — modern, sarcastic, thoda flirty, bakchodi.
Talk about GTA, Valorant, BGMI, Minecraft, etc.
If someone asks for a gaming tip, give a short but helpful response.

Examples:
User: How to aim in Valorant?
Bot: Bhai pehle toh crosshair head pe rakh. Spray control kar, aur bhagwan ko yaad mat kar har round 😂

User: {user_input}
Bot:
"""

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    user_input = message.content
    prompt = get_prompt(user_input)

    try:
        # OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.9,
        )

        reply = response.choices[0].message.content.strip()
        await message.channel.send(reply)

    except Exception as e:
        print("Error:", e)
        await message.channel.send("Bhai kuch toh gadbad ho gayi 😭")

    # Allow other commands to work
    await bot.process_commands(message)

bot.run(DISCORD_BOT_TOKEN)
