import os
import io
import asyncio
import aiohttp
import discord
from discord.ext import commands, tasks
import google.generativeai as genai
from openai import AsyncOpenAI
from lumaai import AsyncLumaAI
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. KONFIGURATION & API KEYS ---
# Tipp: Nutze Umgebungsvariablen für die Sicherheit!
GEMINI_KEY = "DEIN_GEMINI_API_KEY"
OPENAI_KEY = "DEIN_OPENAI_API_KEY"
LUMA_KEY = "DEIN_LUMA_API_KEY"
DISCORD_TOKEN = "DEIN_DISCORD_BOT_TOKEN"
FIREBASE_JSON = "firebase-adminsdk.json" # Pfad zu deiner Firebase Datei

# --- 2. INITIALISIERUNG ---
# Firebase
cred = credentials.Certificate(FIREBASE_JSON)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Gemini AI (System Prompt für Intent-Erkennung)
genai.configure(api_key=GEMINI_KEY)
system_instr = """
Du bist der Kern eines Discord-Bots. Analysiere User-Nachrichten:
1. Bildwunsch? Antworte: TYPE=IMAGE | PROMPT=[Detaillierter englischer 3D-Render Prompt]
2. Animationswunsch? Antworte: TYPE=ANIMATION | PROMPT=[Detaillierter englischer 3D-Animations Prompt]
3. Sonstiges? Antworte: NO_INTENT
"""
gemini_model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instr)

# OpenAI & Luma
openai_client = AsyncOpenAI(api_key=OPENAI_KEY)
luma_client = AsyncLumaAI(auth_token=LUMA_KEY)

# Discord Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. HILFSFUNKTIONEN (CREDITS) ---

def get_user_credits(user_id):
    user_ref = db.collection('users').document(str(user_id))
    doc = user_ref.get()
    if doc.exists:
        return doc.to_dict().get('credits', 5)
    else:
        user_ref.set({'credits': 5, 'total_gen': 0})
        return 5

def deduct_credits(user_id, amount):
    user_ref = db.collection('users').document(str(user_id))
    user_ref.update({'credits': firestore.Increment(-amount), 'total_gen': firestore.Increment(1)})

# --- 4. GENERIERUNGS-LOGIK ---

async def make_image(channel, prompt, user):
    status = await channel.send(f"🎨 {user.mention}, DALL-E 3 generiert dein 3D-Bild...")
    try:
        response = await openai_client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
        image_url = response.data[0].url
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as r:
                data = io.BytesIO(await r.read())
        await channel.send(file=discord.File(data, "image.png"))
    except Exception as e:
        await channel.send(f"Fehler: {e}")
    finally:
        await status.delete()

async def make_animation(channel, prompt, user):
    status = await channel.send(f"🎬 {user.mention}, Luma AI animiert... (Dauert ca. 1-2 Min.)")
    try:
        gen = await luma_client.generations.create(prompt=prompt, loop=True)
        while True:
            check = await luma_client.generations.get(id=gen.id)
            if check.state == "completed":
                await channel.send(f"Fertig! {user.mention}\n{check.assets.video}")
                break
            elif check.state == "failed":
                await channel.send("Animation fehlgeschlagen.")
                break
            await asyncio.sleep(15)
    except Exception as e:
        await channel.send(f"Fehler: {e}")
    finally:
        await status.delete()

# --- 5. EVENTS & TASKS ---

@tasks.loop(hours=1.0)
async def hourly_reset():
    users_ref = db.collection('users')
    batch = db.batch()
    for doc in users_ref.stream():
        batch.update(users_ref.document(doc.id), {'credits': 5})
    batch.commit()
    print("Credits stündlich resettet.")

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user}')
    hourly_reset.start()

@bot.event
async def on_message(message):
    if message.author == bot.user: return

    # Gemini Analyse
    analysis = gemini_model.generate_content(message.content).text.strip()
    
    if "TYPE=" in analysis:
        media_type = "IMAGE" if "TYPE=IMAGE" in analysis else "ANIMATION"
        prompt = analysis.split("PROMPT=")[1]
        cost = 1 if media_type == "IMAGE" else 5
        
        current_credits = get_user_credits(message.author.id)
        if current_credits >= cost:
            deduct_credits(message.author.id, cost)
            if media_type == "IMAGE":
                await make_image(message.channel, prompt, message.author)
            else:
                await make_animation(message.channel, prompt, message.author)
        else:
            await message.channel.send(f"❌ Nicht genug Credits! (Stündlich gibt es neue)")

    await bot.process_commands(message)

# Start
bot.run(DISCORD_TOKEN)
