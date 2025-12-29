"""
AI Assistant for Notepad (Professional implementation)
Supports OpenAI, Groq, OpenRouter, and Free fallbacks.
"""

import requests
import json
import re
import traceback
from typing import List, Dict, Optional
from datetime import datetime
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL

# Fallback free endpoint
FREE_AI_URL = "https://text.pollinations.ai/"

def _call_llm(prompt: str, system_message: str = "You are a helpful assistant for a Notepad app.") -> str:
    """
    Core function to call AI. Prioritizes Keyed API, falls back to Free API.
    """
    
    # 1. Try Professional API (OpenAI/Groq/etc) if key is present
    if AI_API_KEY:
        try:
            url = f"{AI_BASE_URL.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=20, verify=False)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                print(f"Professional API Error ({response.status_code}): {response.text}")
                # Log to traceback for debugging
                import traceback
                traceback.print_exc()
        except Exception as e:
            print(f"Professional API Exception: {e}")

    # 2. Fallback to Free Pollinations API
    try:
        # Prompt engineering for free API: Combine system and user more naturally
        combined_prompt = f"### System: {system_message}\n\n### User: {prompt}"
        
        response = requests.post(
            FREE_AI_URL,
            data=combined_prompt.encode("utf-8"),
            headers={"Content-Type": "text/plain"},
            timeout=15,
            verify=False
        )
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
    except Exception as e:
        print(f"Free API Error: {e}")

    if not AI_API_KEY:
        return "I'm in basic mode. I can see your notes but my AI connection is quiet. Add an API key in the backend for full chat!"
    return "I'm having trouble connecting to your AI provider. Check your API key or internet!"

# ============================================
# USE CASES
# ============================================

def generate_task_summary(tasks: List[Dict]) -> str:
    if not tasks:
        return "Your notepad is clear! Start adding some notes."
    
    task_list = "\n".join([f"- {t['title']} ({t['status']})" for t in tasks[:15]])
    prompt = f"Summarize these notes for me in a friendly, concise way:\n{task_list}"
    
    return _call_llm(prompt, "You are a helpful and encouraging notepad assistant.")

def suggest_priorities(tasks: List[Dict]) -> Dict[str, any]:
    pending = [t for t in tasks if t['status'] == 'pending']
    if not pending:
        return {"suggestions": [], "reasoning": "You've finished everything! Time for a break?"}
    
    task_list = "\n".join([f"- {t['title']} (Due: {t.get('due_date', 'None')})" for t in pending[:10]])
    prompt = f"Which 3 notes from this list should I focus on? Explain why briefly:\n{task_list}"
    
    ans = _call_llm(prompt, "You are a productivity expert.")
    
    # Try to extract the first 3 lines/bullet points as suggestions
    suggestions = [t['title'] for t in pending[:3]]
    
    return {
        "suggestions": suggestions,
        "reasoning": ans,
        "total_pending": len(pending)
    }

def parse_task_draft(text: str) -> Dict[str, any]:
    """Parse natural language into a note draft."""
    today = datetime.now().strftime("%Y-%m-%d (%A)")
    prompt = f"Today is {today}. Convert this text into a JSON object for a note. Text: \"{text}\". Return ONLY JSON with keys: title, description, due_date (YYYY-MM-DD or null)."
    
    # We want a more deterministic response for parsing
    res = _call_llm(prompt, "You are a data extractor. Return only valid JSON.")
    
    draft = {"title": text[:50], "description": None, "due_date": None, "confidence": 0.5}
    try:
        # Improved JSON extraction logic
        match = re.search(r'\{.*\}', res.replace('\n', ''), re.DOTALL)
        if match:
            json_str = match.group(0)
            parsed = json.loads(json_str)
            draft.update({
                "title": parsed.get("title", draft["title"]),
                "description": parsed.get("description"),
                "due_date": parsed.get("due_date"),
                "confidence": 0.9
            })
    except:
        pass
    return draft

def chat_with_task_context(user_message: str, tasks: List[Dict]) -> str:
    """Conversational chat with context of all notes."""
    task_context = "USER NOTES:\n" + "\n".join([f"- {t['title']} ({t['status']})" for t in tasks[:20]])
    
    full_prompt = f"{task_context}\n\nUser Question: {user_message}"
    
    return _call_llm(full_prompt, "You are a helpful companion for this notepad app. You know all the user's notes and you're here to help them brainstorm, organize, or just chat.")

def generate_daily_plan(tasks: List[Dict]) -> str:
    return _call_llm("Look at my notes and give me a quick plan for today.", "You are a daily planner.")
