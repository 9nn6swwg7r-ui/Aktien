import json
import time
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from curl_cffi import requests

session = requests.Session(impersonate="chrome")

AKTIEN_KONFIGURATION = [
    # --- DEINE DEPOT-AKTIEN ---
    {"ticker": "MSFT", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "TSM", "tags": ["Tech", "Taiwan"], "watchlist": False},
    {"ticker": "SAP.DE", "tags": ["Tech", "DE"], "watchlist": False},
    {"ticker": "ORCL", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "AVGO", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "ASML.AS", "tags": ["Tech", "NL"], "watchlist": False},
    {"ticker": "GOOGL", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "QCOM", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "NOW", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "INTU", "tags": ["Tech", "US"], "watchlist": False},
    {"ticker": "JPM", "tags": ["Finanzen", "US"], "watchlist": False},
    {"ticker": "HSBA.L", "tags": ["Finanzen", "UK"], "watchlist": False},
    {"ticker": "SAN.PA", "tags": ["Gesundheit", "FR"], "watchlist": False},
    {"ticker": "BLK", "tags": ["Finanzen", "US"], "watchlist": False},
    {"ticker": "ALV.DE", "tags": ["Finanzen", "DE"], "watchlist": False},
    {"ticker": "MUV2.DE", "tags": ["Finanzen", "DE"], "watchlist": False},
    {"ticker": "SIE.DE", "tags": ["Industrie", "DE"], "watchlist": False},
    {"ticker": "SU.PA", "tags": ["Industrie", "FR"], "watchlist": False},
    {"ticker": "HON", "tags": ["Industrie", "US"], "watchlist": False},
    {"ticker": "CAT", "tags": ["Industrie", "US"], "watchlist": False},
    {"ticker": "DE", "tags": ["Industrie", "US"], "watchlist": False},
    {"ticker": "ABBN.SW", "tags": ["Industrie", "CH"], "watchlist": False},
    {"ticker": "6861.T", "tags": ["Tech", "JP"], "watchlist": False},
    {"ticker": "DG.PA", "tags": ["Industrie", "FR"], "watchlist": False},
    {"ticker": "PH", "tags": ["Industrie", "US"], "watchlist": False},
    {"ticker": "RIO.L", "tags": ["Rohstoffe", "UK"], "watchlist": False},
    {"ticker": "LIN", "tags": ["Chemie", "US"], "watchlist": False},
    {"ticker": "AI.PA", "tags": ["Chemie", "FR"], "watchlist": False},
    {"ticker": "MC.PA", "tags": ["Luxus", "FR"], "watchlist": False},
    {"ticker": "TTE.PA", "tags": ["Energie", "FR"], "watchlist": False},
    {"ticker": "NEE", "tags": ["Utilities", "US"], "watchlist": False},
    {"ticker": "ORSTED.CO", "tags": ["Utilities", "DK"], "watchlist": False},
    {"ticker": "VIE.PA", "tags": ["Utilities", "FR"], "watchlist": False},
    {"ticker": "IBE.MC", "tags": ["Utilities", "ES"], "watchlist": False},
    {"ticker": "LLY", "tags": ["Gesundheit", "US"], "watchlist": False},
    {"ticker": "ROG.SW", "tags": ["Gesundheit", "CH"], "watchlist": False},
    {"ticker": "NOVN.SW", "tags": ["Gesundheit", "CH"], "watchlist": False},
    {"ticker": "ABBV", "tags": ["Gesundheit", "US"], "watchlist": False},
    {"ticker": "JNJ", "tags": ["Gesundheit", "US"], "watchlist": False},
    {"ticker": "AMZN", "tags": ["Consumer", "US"], "watchlist": False},
    {"ticker": "PG", "tags": ["Consumer", "US"], "watchlist": False},
    {"ticker": "NESN.SW", "tags": ["Consumer", "CH"], "watchlist": False},
    {"ticker": "MDLZ", "tags": ["Consumer", "US"], "watchlist": False},
    {"ticker": "KO", "tags": ["Consumer", "US"], "watchlist": False},
    {"ticker": "MCD", "tags": ["Consumer", "US"], "watchlist": False},
    {"ticker": "WMT", "tags": ["Consumer", "US"], "watchlist": False},
    {"ticker": "FPE3.DE", "tags": ["Specialty", "DE"], "watchlist": False},
    {"ticker": "PLD", "tags": ["REIT", "US"], "watchlist": False},
    {"ticker": "KRN.DE", "tags": ["Maschinenbau", "DE"], "watchlist": False},
    {"ticker": "MMK.VI", "tags": ["Packaging", "AT"], "watchlist": False},
    {"ticker": "IBN", "tags": ["Finanzen", "IN"], "watchlist": False},

    # --- WATCHLIST ---
    {"ticker": "POWL", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "ROK", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "SPGI", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "AOS", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "VZ", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "V", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "WY", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "CRWD", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DDOG", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "IBM", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "KEYS", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "KHC", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "MPWR", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "PM", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "PDD", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "ADBE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "MO", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "ANET", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "ADSK", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "CSL", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "CHD", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "NET", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "CGNX", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "6506.T", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "EQNR", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DNB.OL", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "YAR.OL", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DNP.WA", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "PKO.WA", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "ERIC-B.ST", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "D05.SI", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "RI.PA", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DSY.PA", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "SHEL", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "8001.T", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "9984.T", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "6367.T", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "6954.T", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "8058.T", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "RWE.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "SIX2.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "VIB3.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "LHA.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "HNR1.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "VNA.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "EOAN.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "KGX.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "BMW3.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "BEI.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "EVD.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DHL.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DTE.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "EKF.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "FRA.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "DEZ.DE", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "STR.VI", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "VER.VI", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "FIH-U.TO", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "ABBN.SW", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "SREN.SW", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "SIKA.SW", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "1398.HK", "tags": ["Watchlist"], "watchlist": True},
    {"ticker": "2318.HK", "tags": ["Watchlist"], "watchlist": True}
]

def daten_generieren():
    json_output = []
    print(f"=== STARTE AKTUALISIERUNG FÜR {len(AKTIEN_KONFIGURATION)} AKTIEN ===")
    
    for aktie in AKTIEN_KONFIGURATION:
        symbol = aktie["ticker"]
        print(f"Verarbeite: {symbol}...")
        try:
            t = yf.Ticker(symbol, session=session)
            hist_prices = t.history(period="5d")
            if hist_prices.empty:
                hist_prices = t.history(period="1mo")

            if hist_prices.empty:
                continue

            aktueller_kurs = float(hist_prices['Close'].iloc[-1])
            info = t.info or {}
            
            name = info.get("longName", symbol)
            kgv = info.get("trailingPE")
            kcv = info.get("operatingCashflow") # bzw. aus Kennzahlen
            dividendenrendite = info.get("dividendYield")
            if dividendenrendite:
                dividendenrendite = float(dividendenrendite) * 100

            # Ex-Tag und Auszahlungstag falls vorhanden
            ex_dividende = info.get("exDividendDate")
            ex_dividende_str = datetime.fromtimestamp(ex_dividende).strftime('%Y-%m-%d') if ex_dividende else "-"
            
            payout_date = info.get("payoutDate")
            payout_str = datetime.fromtimestamp(payout_date).strftime('%Y-%m-%d') if payout_date else "-"

            aktie_daten = {
                "name": str(name),
                "ticker": str(symbol),
                "kurs": float(aktueller_kurs),
                "kgv": float(kgv) if kgv else None,
                "dividendenrendite": float(dividendenrendite) if dividendenrendite else None,
                "exDividendDate": ex_dividende_str,
                "payoutDate": payout_str,
                "watchlist": bool(aktie["watchlist"]),
                "tags": aktie["tags"]
            }
            json_output.append(aktie_daten)
            print(f"   -> OK: {name} ({aktueller_kurs:.2f})")
        except Exception as e:
            print(f"   -> Fehler bei {symbol}: {e}")
        time.sleep(0.2)
        
    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
    print("=== FERTIG! daten.json aktualisiert. ===")

if __name__ == "__main__":
    daten_generieren()
