"""
necessary libs
pycord 
python3
written by wender10002
this cods have slashcommands is very necessary dowload the pycord lib and not the discord.py, is libs different. Use for code review!
you can chance commands names to your preference names!
"""

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=">")

@bot.event
async def on_ready():
    print(f"Client connect sucesfully with {bot.user}")

@bot.command()
async def ping(ctx, latencia: int):
    latencia=round(bot.latency * 1000)
    await ctx.respond(f"Pong! 🏓 {latencia}ms")


@bot.slash_command(name="blacklistar", description="blacklistar um usuário.")
async def blacklist(ctx, termo=discord.Option(str, description="username do usuário"),
             imagem=discord.Option(discord.Attachment, description="Imagem do ID do usuário"),
             guild_id=[] # your server id to fast up to date
             ):
    await ctx.defer()
    destino_id = 1392986682600718497
    canal = bot.get_channel(destino_id)
    if not canal or not isinstance(canal, discord.TextChannel):
        await ctx.respond("Canal não encontrado ou inválido favor reportar ao <@1353559998919348254>")
        return
    webhooks = await canal.webhooks()
    webhook = next((w for w in webhooks if w.name == "Blacklist Notifier"), None)
    if not webhook:
        webhook = await canal.create_webhook(name="Blacklist Notifier")

    embed = discord.Embed(
    title="Blacklisted :white_check_mark:",
    description=f"Usuário {termo} blacklistado com sucesso!",
    color=discord.Color.red()
    )
    embed.set_image(url=imagem.url)
    await webhook.send(
        embed=embed,
        username="Blacklist Notifier"
    )
    embed2 = discord.Embed(
        title="Usuário Blacklisted!",
        description=f"O usuário {termo} foi blacklistado com sucesso! Check o canal <#1392986682600718497>",
        color=discord.Color.blue()
    )
    await ctx.respond(embed=embed2, ephemeral=False)


@bot.slash_command(name="consultar", description="Consultar usuário.")
async def buscar(ctx, termo: str,):
    await ctx.defer()

    canais_ids = [1393050500982771782, 1392986682600718497, 1393436065573896223]  # [canal_comum, canal_forum]

    for canal_id in canais_ids:
        canal = bot.get_channel(canal_id)

        if canal is None:
            print(f"Aviso: o canal com o id {canal_id} não foi encontrado.")
            continue
 
        if isinstance(canal, discord.ForumChannel):
            for thread in canal.threads:
                if termo.lower() in thread.name.lower():
                    await ctx.respond(f"Encontrei o usuário {termo} no tópico: {thread.jump_url} ")
                    return
                async for mensagem in thread.history(limit=100):
                    if termo.lower() in mensagem.content.lower():
                        await ctx.respond(f"Mensagem encontrada em tópico '{thread.name}': {mensagem.jump_url}")
                        return
        else:
            async for mensagem in canal.history(limit=100):
                if termo.lower() in mensagem.content.lower():
                    await ctx.respond(f"Mensagem encontrada em <#{canal.id}>: {mensagem.jump_url}")
                    return

    await ctx.respond("Nenhum usuário encontrado com esse termo nos canais especificados.")

bot.run("") # token of your bot
