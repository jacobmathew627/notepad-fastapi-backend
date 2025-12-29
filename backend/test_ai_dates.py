import sys
import os
from datetime import datetime

# Add the current directory to the path so we can import ai_assistant
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from ai_assistant import parse_task_draft

def test_date_parsing():
    print("--- AI DATE LOGIC TEST ---")
    today = datetime.now().strftime("%Y-%m-%d (%A)")
    print(f"System Today: {today}")
    
    test_cases = [
        "Buy milk tomorrow",
        "Dinner with John next Friday",
        "Meeting on Jan 5th",
        "Project deadline in 2 days"
    ]
    
    for text in test_cases:
        print(f"\nInput: \"{text}\"")
        try:
            draft = parse_task_draft(text)
            print(f"Result Title: {draft.get('title')}")
            print(f"Result Date:  {draft.get('due_date')} (Extracted)")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_date_parsing()
