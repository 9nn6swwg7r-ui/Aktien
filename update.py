import yfinance as yf
import json
import time

ticker_map = {
    "Microsoft": "MSFT", "TSMC": "TSM", "SAP": "SAP.DE", "Oracle": "ORCL", "Broadcom": "AVGO",
    "ASML": "ASML", "Alphabet": "GOOGL", "Qualcomm": "QCOM", "ServiceNow": "NOW", "Intuit": "INTU",
    "JPMorgan": "JPM", "HSBC": "HSBA.L", "Sanofi": "SNY", "BlackRock": "BLK", "Allianz": "ALV.DE",
    "Munich Re": "MUV2.DE", "Siemens": "SIE.DE", "Schneider Electric": "SU.PA", "Honeywell": "HON", "Caterpillar": "CAT",
    "John Deere": "DE", "ABB": "ABBN.SW", "Keyence": "6861.T", "Vinci": "DG.PA", "Parker-Hannifin": "PH",
    "Rio Tinto": "RIO", "Linde": "LIN", "Air Liquide": "AI.PA", "LVMH": "MC.PA", "TotalEnergies": "TTE",
    "NextEra Energy": "NEE", "Ørsted": "ORSTED.CO", "Veolia": "VIE.PA", "Iberdrola": "IBE.MC",
    "Eli Lilly": "LLY", "Roche": "ROG.SW", "Novartis": "NOVN.SW", "AbbVie": "ABBV", "Johnson & Johnson": "JNJ",
    "Amazon": "AMZN", "Procter & Gamble": "PG", "Nestlé": "NESN.SW", "Mondelez": "MDLZ", "Coca-Cola": "KO",
    "McDonald's": "MCD", "Walmart": "WMT", "Fuchs SE": "FPE3.DE", "Prologis": "PLD", "Krones": "KRN.DE",
    "Mayr-Melnhof": "MMK.VI", "ICICI Bank": "IBN"
}

daten = []
print("Starte Datenabruf...")

for name, sym in ticker_map.items():
    print(f"Lade {name}...")
    try:
        t = yf.Ticker(sym)
        info = t.info
        hist = t.history(period="5y")
        if hist.empty: continue
        
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        avg_5y = hist['Close'].mean()
        
        daten.append({
            "name": name,
            "price": price,
            "perf1M": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21] * 100),
            "perf1J": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-252]) / hist['Close'].iloc[-252] * 100),
            "divYield": (info.get("dividendYield", 0) or 0) * 100,
            "kgv": info.get("trailingPE", 0) or 0,
            "kcv": info.get("priceToCashflow", 0) or 0,
            "abweichung5J": ((price - avg_5y) / avg_5y) * 100
        })
        time.sleep(0.5) # WICHTIG: Verhindert Sperre
    except Exception as e:
        print(f"Fehler bei {name}: {e}")

with open("daten.json", "w", encoding="utf-8") as f:
    json.dump(daten, f, indent=4)
print("Fertig! daten.json wurde erstellt.")
