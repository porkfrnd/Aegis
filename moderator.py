import json
import asyncio
from database import ram_conn

def log_violation_to_ram(username, violation_type):
    """Increments a user's volatility count inside temporary storage."""
    cursor = ram_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS infractions (
            username TEXT PRIMARY KEY,
            count INTEGER
        )
    """)
    
    cursor.execute("SELECT count FROM infractions WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if row:
        new_count = row[0] + 1
        cursor.execute("UPDATE infractions SET count = ? WHERE username = ?", (new_count, username))
    else:
        new_count = 1
        cursor.execute("INSERT INTO infractions (username, count) VALUES (?, ?)", (username, new_count))
    
    ram_conn.commit()
    return new_count

async def evaluate_incident(client, model, username, bad_text, infraction_count):
    """Processes server violations via AI to draft clear, objective legal briefs for staff review."""
    judiciary_prompt = f"""
    You are the Chief Judicial Officer for a high-tier Discord server. 
    Analyze the following behavioral incident and issue a formal assessment for the Moderator Team.

    Accused User: {username}
    Current Incident Chat Text: "{bad_text}"
    Total Session Infractions for this User: {infraction_count}

    Evaluate the severity:
    - LOW: Mild spam, minor attitude, light swearing.
    - MEDIUM: Targeted harassment, toxic slurs, constant disruption, arguing with staff.
    - HIGH: Severe hate speech, threatening users, posting malicious links, explicit racism/doxxing.

    Determine a strict Course of Action (e.g., Warning, 2-hour Timeout, 7-day Ban, Permanent Ban).
    Scale the punishment firmly based on the infraction count.

    Output your judgment strictly as a valid JSON object with no markdown code blocks or formatting wrappers:
    {{
        "threat_level": "LOW or MEDIUM or HIGH",
        "verdict_summary": "Description of what rules the user violated.",
        "course_of_action": "Exact action recommended (e.g., Issue a 2-week ban due to repeated toxicity)"
    }}
    """
    
    loop = asyncio.get_running_loop()
    try:
        def call_judge():
            return client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": judiciary_prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
        response = await loop.run_in_executor(None, call_judge)
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Judiciary core calculation error: {e}")
        return {
            "threat_level": "MEDIUM",
            "verdict_summary": "System flagged suspected chat volatility or harassment.",
            "course_of_action": "Review chat log history manually and execute appropriate administrative actions."
        }
