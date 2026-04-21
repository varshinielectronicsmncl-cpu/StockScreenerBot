import os
import yfinance as yf
import requests
import warnings
warnings.filterwarnings('ignore') 

# GitHub Secrets నుండి టోకెన్స్ తీసుకుంటుంది
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# స్టాక్ పేరు మరియు మన టార్గెట్ ధరలు (మీకు కావాల్సినట్లు మార్చుకోవచ్చు)
stock_symbol = "RELIANCE.NS"
lower_target = 1355  # కిందకు వస్తే
upper_target = 1368  # పైకి వెళితే

try:
    # ఈ రోజుటి లైవ్ ధరను (1 నిమిషం డేటా) తీసుకోవడం
    df = yf.download(stock_symbol, period="1d", interval="1m", progress=False)
    
    # డేటా ఉందో లేదో చెక్ చేయడం
    if not df.empty:
        current_price = df['Close'].iloc[-1]
        print(f"{stock_symbol} ప్రస్తుత ధర: ₹{current_price:.2f}")

        # 1. ధర కిందకు పడిపోతే (Down Alert)
        if current_price <= lower_target:
            msg = f"📉 *PRICE DROP ALERT!*\n\n{stock_symbol} ధర కిందకు పడిపోయింది.\nప్రస్తుత ధర: *₹{current_price:.2f}*\nమీ టార్గెట్: ₹{lower_target}"
            send_telegram_message(msg)
            print("కింది స్థాయి అలర్ట్ పంపబడింది.")
            
        # 2. ధర పైకి పెరిగితే (Up Alert)
        elif current_price >= upper_target:
            msg = f"🚀 *PRICE UP ALERT!*\n\n{stock_symbol} ధర పైకి పెరిగింది.\nప్రస్తుత ధర: *₹{current_price:.2f}*\nమీ టార్గెట్: ₹{upper_target}"
            send_telegram_message(msg)
            print("పై స్థాయి అలర్ట్ పంపబడింది.")
            
        # 3. టార్గెట్ మధ్యలో ఉంటే
        else:
            print(f"ధర {lower_target} మరియు {upper_target} మధ్యలో ఉంది. కాబట్టి మెసేజ్ పంపలేదు.")

except Exception as e:
    print(f"ఎర్రర్: {e}")
