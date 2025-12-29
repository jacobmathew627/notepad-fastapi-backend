import requests
import json
import os
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL

def test_groq_direct():
    print("--- AI DIAGNOSTIC TOOL ---")
    print(f"Checking Connection to: {AI_BASE_URL}")
    print(f"Model: {AI_MODEL}")
    print(f"Key Present: {'Yes' if AI_API_KEY else 'No'}")
    
    if not AI_API_KEY:
        print("\n[!] ERROR: No AI_API_KEY found in config.py")
        return

    url = f"{AI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a test script."},
            {"role": "user", "content": "Hello, are you working?"}
        ]
    }

    try:
        print("\nSending request (SSL Verify = False)...")
        response = requests.post(url, headers=headers, json=payload, timeout=15, verify=False)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            reply = data['choices'][0]['message']['content']
            print("\nSUCCESS!")
            print(f"AI Response: {reply}")
        else:
            print(f"\nFAILED! Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            
    except Exception as e:
        print(f"\nEXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_groq_direct()
