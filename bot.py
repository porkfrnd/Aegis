import os
import json
import asyncio
import random
import aiohttp
import base64
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from openai import OpenAI
import discord
from discord.ext import commands
from duckduckgo_search import DDGS
from huggingface_hub import InferenceClient

# Link backend system layers
import database
import moderator

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_FALLBACK_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_FALLBACK_KEY")
HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_FALLBACK_HF_TOKEN")
MOD_CHANNEL_ID = int(os.getenv("MOD_CHANNEL_ID", "0"))

BOT_NAME = "Aegis"
MAIN_MODEL = "google/gemini-2.5-flash" 

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Connect to Hugging Face serverless hub (100% free speech-to-text)
hf_client = InferenceClient(api_key=HF_TOKEN)

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# ====================================================================
# RENDER FREE TIER KEEP-ALIVE WEB SERVER
# ====================================================================
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Aegis Core Protocol Operational.")
        
    def log_message(self, format, *args):
        return # Suppress connection spam logs in the console

def run_web_server():
    # Render binds web services to port 10000 by default
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    server.serve_forever()

# Spin server off in a daemon thread so it doesn't halt the Discord client execution loop
threading.Thread(target=run_web_server, daemon=True).start()

# ====================================================================
# PERMANENTLY FREE TRANSLATION ENGINE
# ====================================================================
async def transcribe_voice_msg(audio_url):
    """Downloads a Discord voice attachment and runs it through serverless Whisper Large v3."""
    loop = asyncio.get_running_loop()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url) as resp:
                if resp.status != 200: return ""
                audio_data = await resp.read()

        def call_huggingface():
            output = hf_client.automatic_speech_recognition(
                audio_data, 
                model="openai/whisper-large-v3"
            )
            return output.text

        transcript = await loop.run_in_executor(None, call_huggingface)
        return transcript.strip()
    except Exception as e:
        print(f"Hugging Face pipeline error: {e}")
        return ""

# ====================================================================
# CORE SYSTEM UTILITIES
# ====================================================================
def live_web_search(query_text):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query_text, max_results=3)]
            if not results: return "No real-time web results found."
            return "\n\n".join([f"Result: {res['title']}\nSnippet: {res['body']}" for res in results])
    except Exception: return "Failed to retrieve web data."

async def analyze_room_async(bot_name, raw_history, permanent_summary, new_message):
    if not raw_history: return "REPLY", "", "Talk normally.", "NORMAL", "FALSE"
    context_str = "\n".join([msg["content"] for msg in raw_history[-5:]])
    
    eval_prompt = f"""
    You are the social analytical core for a Discord user bot named '{bot_name}'.
    Analyze the recent text exchange, the permanent summary, and the incoming message.

    Channel Knowledge Summary:
    {permanent_summary}

    Recent Chat Stream:
    {context_str}

    New Message:
    {new_message}

    Determine:
    1. ACTION: 'SEARCH', 'REPLY', or 'IGNORE'.
    2. SEARCH_QUERY: Concise 3-4 word query if ACTION is SEARCH, else "".
    3. TONE PROFILE: 1-sentence style directive.
    4. HOSTILITY_LEVEL: 'HOSTILE' if the user message is toxic, insulting, cyberbullying, or breaking guidelines, else 'NORMAL'.
    5. IS_MATH: 'TRUE' if it involves equations, complex variables, physics derivations, calculations, or explicit technical logic, else 'FALSE'.

    Output strictly as a valid JSON object. No markdown wrappers.
    {{
        "action": "SEARCH or REPLY or IGNORE",
        "search_query": "query here or empty string",
        "tone": "tone instruction here",
        "hostility_level": "HOSTILE or NORMAL",
        "is_math": "TRUE or FALSE"
    }}
    """
    loop = asyncio.get_running_loop()
    try:
        def call_analyzer():
            return client.chat.completions.create(model=MAIN_MODEL, messages=[{"role": "user", "content": eval_prompt}], temperature=0.1, response_format={"type": "json_object"})
        raw_response = await loop.run_in_executor(None, call_analyzer)
        result = json.loads(raw_response.choices[0].message.content.strip())
        return (result.get("action", "IGNORE").upper(), result.get("search_query", ""), result.get("tone", "Talk normally."), result.get("hostility_level", "NORMAL").upper(), result.get("is_math", "FALSE").upper())
    except Exception: return "REPLY", "", "Talk normally.", "NORMAL", "FALSE"

# ====================================================================
# MASTER DISCORD CONTROLLER
# ====================================================================
@bot.event
async def on_ready():
    database.init_databases()
    print(f"=========================================")
    print(f" SYSTEM SECURE: {BOT_NAME} PROTOCOL CORE ")
    print(f" HF Voice Processing Matrix: STABLE     ")
    print(f" Keep-Alive Web Server Port: ACTIVE     ")
    print(f"=========================================\n")

@bot.event
async def on_message(message):
    if message.author == bot.user: return

    channel_id = message.channel.id
    user_text = message.content.strip()
    username = message.author.display_name
    
    has_image = len(message.attachments) > 0 and message.attachments[0].content_type.startswith("image/")
    is_voice = len(message.attachments) > 0 and (message.attachments[0].content_type.startswith("audio/") or "voice-message" in message.attachments[0].filename)

    if not user_text and not has_image and not is_voice: return
    if len(user_text) <= 2 and user_text.lower() in ["ok", "hi", "yo", "no", "gg", "lol"] and not is_voice: return

    # 🔊 VOICE COGNITION PIPELINE
    if is_voice:
        async with message.channel.typing():
            voice_url = message.attachments[0].url
            transcription = await transcribe_voice_msg(voice_url)
            if not transcription: return
            user_text = f"[Sent Voice Memo]: {transcription}"

    # 📢 EXECUTIVE ANN-DRAFT COMMAND OVERRIDE
    if channel_id == MOD_CHANNEL_ID and BOT_NAME.lower() in user_text.lower() and "announcement" in user_text.lower():
        async with message.channel.typing():
            announcement_prompt = f"You are {BOT_NAME}, the elite tactical manager of this Discord server. An administrator has commanded you to draft a professional community update announcement based on these instructions:\n\"{user_text}\"\n\nFormat with clean Discord headers and markdown. Provide only the final broadcast-ready text:"
            try:
                loop = asyncio.get_running_loop()
                def call_draft(): return client.chat.completions.create(model=MAIN_MODEL, messages=[{"role": "user", "content": announcement_prompt}], temperature=0.3)
                response = await loop.run_in_executor(None, call_draft)
                await message.reply(f"📁 **{BOT_NAME} Executive Service: Automated Announcement Draft Generated**\n\n{response.choices[0].message.content}")
                return
            except Exception as e: print(f"Announcement engine error: {e}")

    # Standard Chat Stream Processing
    log_text = user_text if not has_image else (f"{user_text} [Sent an Image]" if user_text else "[Sent an Image]")
    database.log_chat_to_ram(channel_id, "user", username, log_text)
    raw_history, permanent_summary = database.get_channel_context(channel_id)

    action, search_query, tone_directive, hostility_level, is_math = await analyze_room_async(
        BOT_NAME, raw_history, permanent_summary, f"{username}: {log_text}"
    )

    # 🚨 SECURITY SCANNERS (Applies to regular text AND voice transcriptions)
    if hostility_level == "HOSTILE":
        infraction_count = moderator.log_violation_to_ram(username, "TOXICITY")
        judgment = await moderator.evaluate_incident(client, MAIN_MODEL, username, log_text, infraction_count)
        
        mod_channel = bot.get_channel(MOD_CHANNEL_ID)
        if mod_channel:
            color_map = {"LOW": discord.Color.yellow(), "MEDIUM": discord.Color.orange(), "HIGH": discord.Color.red()}
            chosen_color = color_map.get(judgment["threat_level"], discord.Color.blue())
            
            embed = discord.Embed(title=f"⚠️ {BOT_NAME.upper()} SECURITY INCIDENT BRIEF", color=chosen_color)
            embed.add_field(name="Accused User", value=message.author.mention, inline=True)
            embed.add_field(name="Threat Level", value=f"**{judgment['threat_level']}**", inline=True)
            embed.add_field(name="Total Strikes", value=str(infraction_count), inline=True)
            embed.add_field(name="Evidence Logs", value=f'"{log_text}"', inline=False)
            embed.add_field(name="Verdict Case Summary", value=judgment["verdict_summary"], inline=False)
            embed.add_field(name="RECOMMENDED COURSE OF ACTION", value=f"🔴 `{judgment['course_of_action']}`", inline=False)
            embed.set_footer(text=f"{BOT_NAME} Judicial Matrix v3.0")
            
            await mod_channel.send(embed=embed)

    # GENERATION RESPONSE LOOP
    if action in ["REPLY", "SEARCH"] or has_image:
        search_results = ""
        if action == "SEARCH" and search_query:
            async with message.channel.typing():
                loop = asyncio.get_running_loop()
                search_results = await loop.run_in_executor(None, live_web_search, search_query)

        system_rules = f"You are a regular friend named {BOT_NAME} hanging out in this channel.\nKNOWLEDGE BANK:\n{permanent_summary}\nSTYLE MATRIX: {tone_directive}"
        if hostility_level == "HOSTILE":
            system_rules += "\nOVERRIDE: This user is toxic. Give them a sharp, snappy reality check back."
        if is_math == "TRUE":
            system_rules += "\nMATH MODE ACTIVE: Break down calculations, scientific formulas, or logical derivations step-by-step cleanly before outlining the final answer."
        if search_results:
            system_rules += f"\n\nLIVE SEARCH RESULTS:\n{search_results}"

        messages_payload = [{"role": "system", "content": system_rules}]

        if has_image:
            async with message.channel.typing():
                try:
                    image_url = message.attachments[0].url
                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_url) as resp:
                            if resp.status == 200:
                                img_bytes = await resp.read()
                                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                                vision_content = [
                                    {"type": "text", "text": f"{username}: {user_text}"},
                                    {"type": "image_url", "image_url": {"url": f"data:{message.attachments[0].content_type};base64,{base64_image}"}}
                                ]
                                messages_payload += raw_history[:-1] + [{"role": "user", "content": vision_content}]
                except Exception: messages_payload += raw_history
        else:
            messages_payload += raw_history

        async with message.channel.typing():
            try:
                loop = asyncio.get_running_loop()
                def call_completion(): return client.chat.completions.create(model=MAIN_MODEL, messages=messages_payload)
                response = await loop.run_in_executor(None, call_completion)
                ai_reply = response.choices[0].message.content
                
                if ai_reply.lower().startswith(f"{BOT_NAME.lower()}:"):
                    ai_reply = ai_reply[len(BOT_NAME)+1:].strip()

                await asyncio.sleep(random.uniform(0.1, 0.25))
                database.log_chat_to_ram(channel_id, "assistant", BOT_NAME, ai_reply)
                await message.reply(ai_reply)
            except Exception as e: print(f"Generation error: {e}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
