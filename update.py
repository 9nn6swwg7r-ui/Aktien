import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Hier sind alle deine Ticker. Füge einfach weitere in die Liste hinzu.
TICKER_LISTE = [
    "MSFT", "AAPL", "O", "NSRGY", "KO", "JNJ", "PG", "PEP", "MCD", "V", 
    "MA", "TSLA", "AMZN", "GOOGL", "META", "NVDA", "ASML", "SAP", "VOW3.DE"
]

def daten_generieren():
    json_output = []
    print(f"Starte Update für {len(TICKER_LISTE)} Aktien...")
    
    for ticker in TICKER_LISTE:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1mo")
            if hist.empty: continue
            
            kurs = hist['Close'].iloc[-1]
            
            # Dividende
            divs = t.dividends
            div_yield = (divs[divs.index > (datetime.now() - timedelta(days=365))].sum() / kurs) if not divs.empty else 0
            
            aktie = {
                "name": ticker,
                "ticker": ticker,
                "kurs": f"{kurs:.2f}",
                "perfTag": 0.0, "perfMonat": 0.0, "perfJahr": 0.0, "perf5J": 0.0,
                "dividende": float(div_yield),
                "kgv": 0.0, "kgv5J": 0.0, "kcv": 0.0, "kcv5J": 0.0,
                "watchlist": False, "tags": ["Tech"], "logoUrl": "",
                "monate": "-", "frequenz": "-", "exDate": "-"
            }
            json_output.append(aktie)
            print(f"Erfolgreich: {ticker}")
        except Exception as e:
            print(f"Fehler bei {ticker}: {e}")

    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4)
    print("Fertig! 'daten.json' wurde gespeichert.")

if __name__ == "__main__":
    daten_generieren()
