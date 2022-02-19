import discord
import datetime
import json
import requests
import psutil
from uptime import uptime
import cpuinfo
from discord.ext import commands


with open('config.json') as json_file:
    data = json.load(json_file)

BOT_TOKEN = data["TOKEN"]
NODE_NAME = data["SERVER_NAME"]
PREFIX = data["PREFIX"]

client = commands.Bot(command_prefix=PREFIX)

client.remove_command("help")

@client.event
async def on_ready():
    print(f"ready {client.user} !")

start_time = datetime.datetime.utcnow()


@client.command(aliases=[NODE_NAME])
async def stats(ctx):
    up = uptime()
    time = float(up)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    uptime_stamp = ("%dd %dh %dm %ds" % (day, hour, minutes, seconds))
    cpu = cpuinfo.get_cpu_info()["brand_raw"]
    threads = cpuinfo.get_cpu_info()["count"]
    cpu_usage = f"CPU Usage: {psutil.cpu_percent(interval=1)}%"
    ram_usage = f"Ram Usage: {round(psutil.virtual_memory().used/1000000000, 2)}GB / {round(psutil.virtual_memory().total/1000000000, 2)}GB"
    swap_usage = f"SWAP Usage: {round(psutil.swap_memory().used/1000000000, 2)}GB / {round(psutil.swap_memory().total/1000000000, 2)}GB"
    disk_usage = f"Disk Usage: {round(psutil.disk_usage('/').used/1000000000, 2)}GB / {round(psutil.disk_usage('/').total/1000000000, 2)}GB"
    response = requests.get(f"http://ip-api.com/json/").json()
    physical_info = f"CPU: {threads} Threads | {cpu}\nIP: {response['query']}"


    embed = discord.Embed(title=f"{NODE_NAME} Stats", description=f"**----- Node Info ----**\n**```\n{cpu_usage} \n{ram_usage}\n{swap_usage}\n{disk_usage}```**\n**----- Physical Info -----**\n**```\n{physical_info}```**", color=discord.Color.blue())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Uptime: {uptime_stamp}", icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)


client.run(BOT_TOKEN)
