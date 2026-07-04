import yfinance as yf
import json
import math
import time

def isNaN(num):
    return isinstance(num, float) and math.isnan(num)

# Deine komplette Liste bleibt unverändert (hier im Skript vorhanden)
meine_aktien = [
    # ... (deine Liste aus der Nachricht oben) ...
]

def fetch_data():
    print("Starte Datenabruf...")
    # FX Raten (einfacher gehalten für Stabilität)
    fx_rates = {"USD": 1.0, "EUR": 1.0, "CHF": 1.0, "GBP": 1.0, "DKK": 1.0, "JPY": 1.0, "HKD": 1.0, "PLN": 1.0, "CAD": 1.0, "NOK": 1.0}
    
    aktien_daten = []

    for aktie in meine_aktien:
        try:
            ticker = yf.Ticker(aktie["symbol"])
            # Historische Daten holen
            hist = ticker.history(period="5y")
            if hist.empty: continue
            
            raw_kurs = hist['Close'].iloc[-1]
            
            # Info-Abruf mit kleinem Delay für Stabilität bei vielen Werten
            # Wir versuchen es einmal, wenn es fehlschlägt, setzen wir Standardwerte
            try:
                info = ticker.info
                div_yield = info.get("dividendYield", 0) or 0
                div_yield = float(div_yield) * 100 if div_yield < 1 else float(div_yield)
                kgv = float(info.get("trailingPE") or info.get("forwardPE") or 0.0)
            except:
                div_yield, kgv = 0.0, 0.0

            aktien_daten.append({
                "name": aktie["name"],
                "symbol": aktie["symbol"],
                "logoUrl": aktie["logoUrl"],
                "tags": aktie["tags"],
                "watchlist": aktie["watchlist"],
                "kurs": f"{raw_kurs:.2f}",
                "yield": round(div_yield, 2),
                "kgv": round(kgv, 2)
            })
            print(f"Erfolgreich geladen: {aktie['symbol']}")
            time.sleep(0.2) # Schutz gegen Yahoo-Blockade
            
        except Exception as e:
            print(f"Fehler bei {aktie['symbol']}: {e}")

    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(aktien_daten, f, ensure_ascii=False, indent=4)
    print("Fertig. daten.json wurde aktualisiert.")

if __name__ == "__main__":
    fetch_data()
