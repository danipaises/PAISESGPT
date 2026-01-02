import os
import shutil
import asyncio
import discord
from discord.ext import commands
from metagpt.roles import SoftwareCompany
from metagpt.team import Team

# 1. Configurações de Ambiente (O Zeabur vai ler isso das Variables)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["LLM_MODEL"] = "minimax/minimax-m2.1"

# 2. Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot operando 24h: {bot.user}')

@bot.command()
async def criar(ctx, *, projeto: str):
    await ctx.send(f"🤖 **MetaGPT + MiniMax M2.1** iniciando o projeto: `{projeto}`")
    
    # Criando a pasta do projeto
    project_name = f"projeto_{ctx.author.id}"
    workspace = os.path.join("workspace", project_name)
    
    try:
        # Executando o MetaGPT (Equipe de Software)
        team = Team()
        team.hire([SoftwareCompany()])
        team.invest(investment=10.0) # Investimento fictício de tokens
        await team.run(n_round=5, idea=projeto)
        
        # O MetaGPT salva por padrão em 'storage/team' ou 'workspace/'
        # Vamos localizar e zipar
        zip_path = f"{project_name}.zip"
        shutil.make_archive(project_name, 'zip', "workspace")

        # Enviando para o Discord
        file = discord.File(f"{zip_path}")
        await ctx.send(content="✅ Aqui está seu código e o ZIP:", file=file)
        await ctx.send(f"🔗 **Preview:** (Para preview real, você precisaria integrar com a Vercel/Netlify API)")

    except Exception as e:
        await ctx.send(f"❌ Erro: {str(e)}")
    
    finally:
        # Limpeza para não encher o disco do Zeabur
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists("workspace"):
            shutil.rmtree("workspace")

bot.run(os.getenv("DISCORD_TOKEN"))
