from flask import Flask, request, jsonify
from threading import Thread
import discord
from discord.ext import commands
import asyncio

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")  # Replace this with your bot token
GUILD_ID = 1357177503894077481     # Replace with your Discord server ID
CATEGORY_NAME = "ai-logs"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_message():
    data = request.json
    ip = data.get("ip", "unknown")
    content = data.get("content", "")
    print(f"[FLASK] IP: {ip}")
    print(f"[FLASK] Message: {content}")
    future = asyncio.run_coroutine_threadsafe(bot_log(ip, content), bot.loop)
    try:
        future.result(timeout=10)
    except Exception as e:
        print(f"[ERROR] Coroutine failed: {e}")
    return jsonify({"status": "ok"})

async def bot_log(ip, content):
    print(f"[BOT] Logging from {ip}...")
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found!")
        return

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        category = await guild.create_category(CATEGORY_NAME)

    safe_ip = ip.replace('.', '-').replace(':', '-')
    channel = discord.utils.get(category.channels, name=safe_ip)
    if not channel:
        channel = await guild.create_text_channel(safe_ip, category=category)

    try:
        await channel.send(f"**Log from `{ip}`:**\n{content}")
{content}")
        print(f"✅ Sent to #{safe_ip}")
    except Exception as e:
        print(f"❌ Error sending message: {e}")

def run_flask():
    print("🚀 Flask running on http://localhost:5050")
    app.run(host="0.0.0.0", port=5050)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

Thread(target=run_flask).start()
bot.run(TOKEN)
