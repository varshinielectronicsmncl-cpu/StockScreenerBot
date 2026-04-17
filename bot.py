import os
import yfinance as yf
import pandas_ta as ta
import requests
import warnings
warnings.filterwarnings('ignore') 

# GitHub Secrets నుండి టోకెన్స్ తీసుకుంటుంది (ఇతరులకు కనిపించవు)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

stocks_list =["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS", "INFY.NS", "ICICIBANK.NS", "ITC.NS", "LT.NS"]

buy_signals = []
sell_signals =[]

for stock in stocks_list:
    try:
        df = yf.download(stock, period="1mo", interval="1d", progress=False)
        if df.empty: continue
            
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['Prev_High'] = df['High'].shift(1)
        df['Prev_Low'] = df['Low'].shift(1)
        
        latest = df.iloc[-1]
        current_close = latest['Close']
        prev_high = latest['Prev_High']
        prev_low = latest['Prev_Low']
        current_rsi = latest['RSI']
        
        if current_close > prev_high and current_rsi > 50:
            buy_signals.append(f"🟢 *BUY*: {stock.replace('.NS', '')} | Price: ₹{current_close:.2f} | RSI: {current_rsi:.2f}")
            
        elif current_close < prev_low and current_rsi < 40:
            sell_signals.append(f"🔴 *SELL*: {stock.replace('.NS', '')} | Price: ₹{current_close:.2f} | RSI: {current_rsi:.2f}")
    except:
        pass

if buy_signals or sell_signals:
    final_message = "📊 *మార్కెట్ అలర్ట్:*\n\n"
    if buy_signals: final_message += "*BUY సిగ్నల్స్:*\n" + "\n".join(buy_signals) + "\n\n"
    if sell_signals: final_message += "*SELL సిగ్నల్స్:*\n" + "\n".join(sell_signals)
    send_telegram_message(final_message)
