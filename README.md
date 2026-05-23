# ⚡ **AEGIS** — The Ultimate Discord Bot Evolution ⚡

> **Your server's new best friend AND iron-fisted judiciary overlord. Lightning-fast AI conversations. Bulletproof moderation. Zero lag. Pure serverless magic.**

---

## 🚀 **What is Aegis?**

Aegis is a **high-speed, advanced modular Discord bot** engineered for peak performance on minimal hardware. It seamlessly blends two personalities:

1. **Casual Conversational Companion** — A witty, intelligent chatbot that vibes with your community in real-time
2. **Automated Judicial Backend** — A silent sentinel that monitors server health, logs toxicity incidents, and enforces moderation with surgical precision

Powered by **dual-brain architecture**, Aegis combines **microsecond-level RAM caching** (SQLite) with **permanent cloud storage** (Supabase PostgreSQL) to deliver **zero local lag** and **24/7 reliability on weak hardware or free cloud tiers** like Render.

✨ **In short:** Lightning-fast conversations + bulletproof moderation + cloud-native intelligence = the server assistant you didn't know you needed.

---

## 🎯 **Key Core Features**

### **🧠 Dual-Brain Architecture**

| Mode | Purpose | Behavior |
|------|---------|----------|
| **Conversational Buddy** | Community engagement | Responds to natural language queries, tells jokes, analyzes questions, provides information |
| **Elite Tactical Judge** | Automated moderation | Monitors messages for toxicity, logs incidents, assigns threat levels, recommends judicial action |

---

### **⚖️ Automated Judiciary System**

Aegis runs **real-time toxicity monitoring** on every message. When an incident is detected:

✅ **Automatic Logging** — Captured immediately to a private staff channel  
✅ **Threat Classification** — Assigned a threat level: 🟢 **Low** | 🟡 **Medium** | 🔴 **High**  
✅ **Judicial Recommendation** — Precise action suggested (e.g., *2-week ban*, *mute 24h*, *warning logged*)  
✅ **Evidence Trail** — Full context stored permanently in Supabase for audit trails  

**Example Incident Report:**
```
🚨 TOXICITY ALERT 🚨
User: @BadActor#1234
Message: [offensive content]
Threat Level: 🔴 HIGH
Recommended Action: Temporary Ban (14 days)
Evidence: Stored in permanent_knowledge DB
```

---

### **🎙️ Permanently Free Voice Cognition**

Aegis intercepts **Discord voice messages** automatically:

🔊 **Background Processing** — Downloads voice memos without user intervention  
📝 **Seamless Transcription** — Converts to text via **Hugging Face Serverless API** (OpenAI Whisper Large v3)  
📊 **Automated Chat Logging** — Transcribed content indexed in permanent cloud database  
🛡️ **Moderation Ready** — Toxicity scanning applied to voice content just like text  

**Zero cost. Zero manual intervention. Pure automation.**

---

### **📢 Executive Commands**

Private channel admin overrides for instant power:

💼 **On-Demand Drafting** — Generate high-quality server announcements automatically  
🎨 **Customizable Format** — Specify tone, audience, and key points  
⚡ **One-Command Execution** — Deploy announcements to your entire server instantly  

```
/announce topic:"New Rules" tone:"professional" audience:"everyone"
```

---

### **👁️ Multimodal Vision Core**

Aegis can parse and analyze **any media type** completely free:

🖼️ **Image Analysis** — Understand visual content, detect objects, analyze diagrams  
📊 **Code Metrics** — Parse code snippets, identify patterns, suggest optimizations  
📈 **Graphics & Charts** — Extract data from visual representations  

---

### **🧮 Math & Logic Derivation Core**

Detect equations and physics concepts automatically:

✓ Recognizes mathematical expressions in chat  
✓ Forces step-by-step analytical breakdowns  
✓ Explains logic chains in human-readable format  
✓ Perfect for study servers, engineering communities, and technical discussions  

---

## 🏗️ **The Tech Stack (Under the Hood)**

Aegis is built on a **production-grade, serverless-optimized architecture**:

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Core Bot Framework** | `discord.py` | Native Discord API integration |
| **AI Backbone** | OpenRouter API (`google/gemini-2.5-flash`) | Fast, intelligent reasoning engine |
| **Voice Processing** | Hugging Face Inference API (`Whisper Large v3`) | Real-time speech-to-text |
| **Hot Storage** | SQLite (In-Memory Shared Cache) | Microsecond-latency chat logs & session data |
| **Cold Storage** | Supabase (PostgreSQL) | Permanent cloud database for compliance & audits |
| **Runtime** | Python 3.10+ | Modern, async-first execution |

---

## ✅ **Prerequisites & Tools Required**

Before you deploy Aegis, gather these essentials:

### **Development Environment**
- ✓ **Python 3.10+** — [Install here](https://www.python.org/downloads/)
- ✓ **Git** — For cloning the repository
- ✓ **A terminal/command line** — PowerShell, Bash, Zsh, etc.

### **Discord Setup**
- ✓ **Discord Developer Portal Bot Token** — [Create here](https://discord.com/developers/applications)
  - Enable **Message Content Intent**
  - Enable **Server Members Intent**
  - Copy your token (keep it SECRET!)

### **API Keys (All Free Tiers Available)**
- ✓ **OpenRouter API Key** — [Get here](https://openrouter.ai/)
  - Free credits for testing available
  
- ✓ **Hugging Face User Access Token** — [Create here](https://huggingface.co/settings/tokens)
  - Free tier includes 25,000 inference requests/month
  
- ✓ **Supabase Project URL & Service Key** — [Setup here](https://supabase.com/)
  - Free tier: 500MB storage, unlimited row reads
  - Service Key (NOT the anon key!) for server-side auth

### **Database Initialization**
- ✓ **Supabase Table: `permanent_knowledge`**
  ```sql
  CREATE TABLE permanent_knowledge (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    server_id BIGINT NOT NULL,
    message_content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    threat_level VARCHAR(20),
    moderation_action TEXT
  );
  ```

---

## 📦 **Installation & Local Deployment**

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/porkfrnd/Aegis.git
cd Aegis
```

### **Step 2: Create Project Structure**

Ensure your project directory looks like this:

```
Aegis/
├── bot.py              # Main bot entry point
├── moderator.py        # Moderation/judiciary logic
├── database.py         # Supabase + SQLite integration
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (keep SECRET!)
└── README.md           # Documentation
```

### **Step 3: Create `requirements.txt`**

```txt
discord.py==2.4.0
python-dotenv==1.0.0
openrouter==0.1.0
requests==2.31.0
supabase==2.3.5
```

### **Step 4: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 5: Configure Environment Variables**

Create a `.env` file in the root directory with:

```env
DISCORD_BOT_TOKEN=your_bot_token_here
OPENROUTER_API_KEY=your_openrouter_key_here
HF_TOKEN=your_huggingface_token_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_key_here
MOD_CHANNEL_ID=123456789012345678
```

**⚠️ CRITICAL:** Never commit `.env` to version control. Add to `.gitignore`:

```
.env
__pycache__/
*.pyc
```

---

## 🔧 **Environment Configuration Variables**

| Variable | Example | Description |
|----------|---------|-------------|
| `DISCORD_BOT_TOKEN` | `MTkxNjIyNDcyOTk1ODI4NzY4.Clwa7A.abc123...` | Your Discord bot's authentication token |
| `OPENROUTER_API_KEY` | `sk-or-v1-abc123...` | API key for AI model access via OpenRouter |
| `HF_TOKEN` | `hf_abc123...` | Hugging Face token for voice transcription |
| `SUPABASE_URL` | `https://abcxyz.supabase.co` | Your Supabase project URL |
| `SUPABASE_KEY` | `eyJhbGc...` | Supabase service key (NOT anon key!) |
| `MOD_CHANNEL_ID` | `987654321098765432` | Discord channel ID for moderation alerts |

---

## 🎬 **Running the System**

### **Local Development**

Start Aegis with a single command:

```bash
python bot.py
```

**Expected Output:**
```
✅ AEGIS ONLINE ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Bot is live and listening
🧠 Dual-brain architecture active
📊 SQLite cache initialized
☁️ Supabase connection established
🎙️ Voice interceptor armed
⚖️ Judiciary system online
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The bot will:
- ✅ Connect to Discord
- ✅ Initialize SQLite RAM cache
- ✅ Establish Supabase connection
- ✅ Begin monitoring messages in all guilds where it has permissions
- ✅ Listen for voice messages automatically

### **Stopping the Bot**

Press `CTRL+C` in your terminal to gracefully shut down.

---

## ☁️ **Cloud Production Deployment (Render)**

Host Aegis **24/7 on Render's free tier** using Background Workers:

### **Step 1: Push to GitHub**

Ensure your repository is on GitHub with all code committed:

```bash
git add .
git commit -m "Deploy Aegis to Render"
git push origin main
```

### **Step 2: Create Render Background Worker**

1. Go to [render.com](https://render.com) → Sign in
2. Click **+ New** → Select **Background Worker**
3. **Connect your GitHub repo** (`porkfrnd/Aegis`)
4. Configure settings:
   - **Name:** `aegis-bot`
   - **Runtime:** `Python 3.10`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

### **Step 3: Inject Environment Variables**

In Render dashboard → **Settings** → **Environment**:

| Key | Value |
|-----|-------|
| `DISCORD_BOT_TOKEN` | Paste your token |
| `OPENROUTER_API_KEY` | Paste your key |
| `HF_TOKEN` | Paste your token |
| `SUPABASE_URL` | Paste your URL |
| `SUPABASE_KEY` | Paste your service key |
| `MOD_CHANNEL_ID` | Paste channel ID |

**Deploy!** Render will automatically:
- ✅ Pull latest code from GitHub
- ✅ Install dependencies
- ✅ Start the bot
- ✅ Keep it running 24/7 on their free tier
- ✅ Auto-restart on crashes
- ✅ Auto-redeploy on git push

---

## 📚 **Usage Examples**

### **Conversational Mode**

```
User: @Aegis explain quantum entanglement
Aegis: Quantum entanglement is a phenomenon where two particles become correlated...
```

### **Moderation in Action**

```
User: [sends toxic message]
Aegis (in mod channel): 🚨 TOXICITY ALERT
Threat Level: 🔴 HIGH
Recommended: 7-day ban
Evidence logged to permanent_knowledge
```

### **Voice Transcription**

```
User: [sends Discord voice message]
Aegis (background): Transcribes using Whisper → Logs to Supabase → Applies moderation
Staff: See transcript in mod channel with threat level
```

---

## 🤝 **Contributing & Support**

Have ideas? Found a bug? Let's build together!

- **Issues:** [Report bugs here](https://github.com/porkfrnd/Aegis/issues)
- **Discussions:** [Ideas & feedback](https://github.com/porkfrnd/Aegis/discussions)
- **Pull Requests:** Contributions welcome with clear descriptions

---

## 📄 **License**

Aegis is open-source and available for personal and community use. Check `LICENSE` for details.

---

## 🎉 **You're Ready!**

Your server is about to get **lightning-fast, intelligent, and bulletproof**. Deploy Aegis today and watch your moderation become effortless while your community enjoys the smoothest bot experience on Discord.

**Questions?** Check the [GitHub Discussions](https://github.com/porkfrnd/Aegis/discussions) or open an issue.

---

**Built with ⚡ by the Aegis team**  
*Making Discord servers smarter, one message at a time.*
