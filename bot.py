import os
import requests

# GitHub Secrets నుండి టోకెన్స్ తీసుకుంటుంది
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    # మెసేజ్ పంపడం
    response = requests.post(url, data=payload)
    
    # రిజల్ట్ ప్రింట్ చేయడం (ఎర్రర్ వస్తే గిట్‌హబ్‌లో చూడటానికి)
    print("Status Code:", response.status_code)
    print("Response:", response.text)

# మనం పంపాలనుకుంటున్న టెస్ట్ మెసేజ్
test_msg = "🔔 *TESTING:* నమస్కారం! మీ టెలిగ్రామ్ బాట్ విజయవంతంగా కనెక్ట్ అయ్యింది. సిస్టమ్ పర్ఫెక్ట్‌గా పనిచేస్తోంది! 🚀"

send_telegram_message(test_msg)
print("✅ టెస్ట్ మెసేజ్ పంపే ప్రాసెస్ పూర్తయింది.")
