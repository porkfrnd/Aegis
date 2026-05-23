import os
import sqlite3
from supabase import create_client, Client

# Pull cloud database credentials safely from Render Environment Variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "YOUR_FALLBACK_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "YOUR_FALLBACK_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Shared global volatile RAM connection for rapid text logging
ram_conn = sqlite3.connect("file:livecache?mode=memory&cache=shared", uri=True)

def init_databases():
    """Initializes high-speed RAM database buffers."""
    ram_cursor = ram_conn.cursor()
    ram_cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            role TEXT,
            username TEXT,
            content TEXT
        )
    """)
    ram_cursor.execute("CREATE INDEX IF NOT EXISTS idx_ram_channel ON raw_logs (channel_id)")
    ram_conn.commit()

def log_chat_to_ram(channel_id, role, username, text):
    """Instantly caches message lines to RAM and drops anything older than 40 lines."""
    cursor = ram_conn.cursor()
    formatted_content = f"{username}: {text}" if role == "user" else text
    str_cid = str(channel_id)
    
    cursor.execute("INSERT INTO raw_logs (channel_id, role, username, content) VALUES (?, ?, ?, ?)", 
                   (str_cid, role, username, formatted_content))
    cursor.execute("""
        DELETE FROM raw_logs WHERE id IN (
            SELECT id FROM raw_logs WHERE channel_id = ? 
            ORDER BY id DESC LIMIT -1 OFFSET 40
        )
    """, (str_cid,))
    ram_conn.commit()

def get_channel_context(channel_id):
    """Fetches hot short term rows from RAM and structural context from Supabase cloud."""
    str_cid = str(channel_id)
    
    # 1. Grab short-term rolling matrix
    ram_cursor = ram_conn.cursor()
    ram_cursor.execute("SELECT role, content FROM raw_logs WHERE channel_id = ? ORDER BY id ASC", (str_cid,))
    raw_history = [{"role": r[0], "content": r[1]} for r in ram_cursor.fetchall()]
    
    # 2. Grab long-term memory summary sheets from the cloud
    try:
        response = supabase.table("permanent_knowledge").select("summary_data").eq("channel_id", str_cid).execute()
        permanent_summary = response.data[0]["summary_data"] if response.data else "No historic long-term memories established yet."
    except Exception as e:
        print(f"Cloud Read Disruption: {e}")
        permanent_summary = "No historic long-term memories established yet."
        
    return raw_history, permanent_summary

def save_permanent_summary(channel_id, summary_text):
    """Pushes permanent channel summaries cleanly to the cloud database."""
    str_cid = str(channel_id)
    try:
        supabase.table("permanent_knowledge").upsert({
            "channel_id": str_cid,
            "summary_data": summary_text
        }).execute()
    except Exception as e:
        print(f"Cloud Write Disruption: {e}")
