import discord
import datetime
import json
import psutil
import cpuinfo
from discord.ext import commands

client = commands.Bot(command_prefix="g!", intents=discord.Intents.all())

client.remove_command("help")

with open('config.json') as json_file:
    data = json.load(json_file)

BOT_TOKEN = data["BOT_TOKEN"]
NODE_NAME = data["SERVER_NAME"]
IP = data["SERVER_IP"]


@client.event
async def on_ready():
    print(f"ready {client.user} !")

start_time = datetime.datetime.utcnow()


@client.command(aliases=[NODE_NAME])
async def stats(ctx):
    now = datetime.datetime.utcnow()  # Timestamp of when uptime function is run
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "{d}d {h}h {m}m {s}s"
    else:
        time_format = "{h}h {m}m {s}s"
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    cpu = cpuinfo.get_cpu_info()["brand_raw"]

    embed = discord.Embed(title=f"{NODE_NAME} Stats", description=f"**----- Node Info ----**\n**```\nCPU Usage: {psutil.cpu_percent(interval=1)}% \nRam Usage: {round(psutil.virtual_memory().used/1000000000, 2)}GB / {round(psutil.virtual_memory().total/1000000000, 2)}GB\nSWAP Usage: {round(psutil.swap_memory().used/1000000000, 2)}GB / {round(psutil.swap_memory().total/1000000000, 2)}GB\nDisk Usage: {round(psutil.disk_usage('/').used/1000000000, 2)}GB / {round(psutil.disk_usage('/').total/1000000000, 2)}GB```**\n**----- Physical Info -----**\n**```\nCPU: {cpu}\nIP: {IP}```**", color=discord.Color.blue())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"https://client.galaxichost.com  ||  Uptime: {uptime_stamp}", icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)


client.run(BOT_TOKEN)
