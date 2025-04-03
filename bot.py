from flask import Flask, request, jsonify
from threading import Thread
import discord
from discord.ext import commands
import asyncio

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")  # Replace this with your bot token
GUILD_ID = 1357177503894077481     # Replace with your Discord server ID
CATEGORY_NAME = "ai-logs"

# === INTENTS ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

# === WEB ENDPOINT ===
@app.route('/log', methods=['POST'])
def log_message():
    data = request.json
    ip = data.get("ip", "unknown")
    content = data.get("content", "")
    print(f"📥 Received from IP {ip}: {content}")
    asyncio.run_coroutine_threadsafe(bot_log(ip, content), bot.loop)
    return jsonify({"status": "ok"})

# === DISCORD LOGGING FUNCTION ===
async def bot_log(ip, content):
    print("📡 Running bot_log()...")
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found! Check GUILD_ID and that the bot is in the server.")
        return

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        print("📁 Creating category:", CATEGORY_NAME)
        category = await guild.create_category(CATEGORY_NAME)

    safe_ip = ip.replace('.', '-').replace(':', '-')
    channel = discord.utils.get(category.channels, name=safe_ip)
    if not channel:
        print(f"📂 Creating new channel for IP: {ip}")
        channel = await guild.create_text_channel(safe_ip, category=category)

    await channel.send(f"**Log from `{ip}`:**\n{content}")

# === START FLASK IN BACKGROUND ===
def run_flask():
    print("🚀 Starting Flask server on http://localhost:5050")
    app.run(port=5050)

# === BOT READY ===
@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

# === START EVERYTHING ===
Thread(target=run_flask).start()
bot.run(TOKEN)
