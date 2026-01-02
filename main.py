import os
import shutil
import asyncio
import discord
from discord.ext import commands
from metagpt.roles import SoftwareCompany
from metagpt.team import Team

# Configuração para o Zeabur/Hospedagem ler as chaves secretas
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["LLM_MODEL"] = "minimax/minimax-m2.1"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot Online como {bot.user}')

@bot.command()
async def criar(ctx, *, ideia: str):
    await ctx.send(f"🚀 Iniciando projeto com MetaGPT e MiniMax M2.1: `{ideia}`")
    
    project_name = f"projeto_{ctx.author.id}"
    
    try:
        # Configura a equipe do MetaGPT
        team = Team()
        team.hire([SoftwareCompany()])
        team.invest(investment=10.0)
        
        # Roda o processo de criação
        await team.run(n_round=5, idea=ideia)
        
        # Cria o ZIP da pasta workspace (onde o MetaGPT salva tudo)
        shutil.make_archive(project_name, 'zip', "workspace")

        # Envia para o Discord
        with open(f"{project_name}.zip", "rb") as file:
            await ctx.send("✅ Código gerado com sucesso!", file=discord.File(file, f"{project_name}.zip"))

    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro: {str(e)}")
    
    finally:
        # Limpa os arquivos para não ocupar espaço no servidor
        if os.path.exists(f"{project_name}.zip"):
            os.remove(f"{project_name}.zip")
        if os.path.exists("workspace"):
            shutil.rmtree("workspace")

bot.run(os.getenv("DISCORD_TOKEN"))
