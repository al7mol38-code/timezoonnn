import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1550904132695621723  # آيدي القناة المطلوبة

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TIMEZONES = {
    "🇧🇷 São Paulo": "America/Sao_Paulo",
    "🇵🇱 Warsaw": "Europe/Warsaw",
    "🇸🇦 Dammam": "Asia/Riyadh",
    "🇸🇬 Singapore": "Asia/Singapore",
    "🇯🇵 Tokyo": "Asia/Tokyo",
    "🇦🇺 Sydney": "Australia/Sydney"
}

def generate_times_message():
    msg = "**Server Region Times**\n"
    for label, tz_name in TIMEZONES.items():
        tz = pytz.timezone(tz_name)
        now_local = datetime.now(tz)
        current_time = now_local.strftime("%H:%M")
        hour = now_local.hour
        
        extra = ""
        # الشروط الزمنية المحددة لكل مدينة
        if 0 <= hour < 5:
            if any(city in label for city in ["Dammam", "Sydney", "Singapore"]):
                extra = " ⭐"
        elif 5 <= hour < 8:
            if "Warsaw" in label:
                extra = " ⭐"
        elif 8 <= hour < 18:
            if "São Paulo" in label:
                extra = " ⭐"
        elif 18 <= hour < 24:
            if "Sydney" in label:
                extra = " ⭐"

        msg += f"{label}: **{current_time}**{extra}\n"
    return msg

# هذه المهمة تعمل تلقائياً كل ساعة وتُرسل الرسالة في القناة
@tasks.loop(hours=1)
async def send_server_times():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        msg = generate_times_message()
        await channel.send(msg)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم {bot.user}')
    if not send_server_times.is_running():
        send_server_times.start()  # بدء العداد التلقائي عند تشغيل البوت

# أمر يدوي لو أردت طلبه في أي وقت بـ !times
@bot.command(name='times')
async def server_times_cmd(ctx):
    msg = generate_times_message()
    await ctx.send(msg)

bot.run(TOKEN)
