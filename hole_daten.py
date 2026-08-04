import json
import time
from datetime import datetime
import yfinance as yf
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
    {"ticker": "RO.SW", "tags": ["Gesundheit", "CH"], "watchlist": False},
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

    # --- WATCHLIST (MIT KORREKTEN TAGS & WATCHLIST=TRUE) ---
    {"ticker": "PKO.WA", "tags": ["Finanzen", "PL"], "watchlist": True},
    {"ticker": "VNA.DE", "tags": ["Real Estate", "DE"], "watchlist": True},
    {"ticker": "6367.T", "tags": ["Industrie", "JP"], "watchlist": True},
    {"ticker": "UBSG.SW", "tags": ["Finanzen", "CH"], "watchlist": True},
    {"ticker": "STR.VI", "tags": ["Bau", "AT"], "watchlist": True},
    {"ticker": "SCRPF", "tags": ["Industrie", "SG"], "watchlist": True},
    {"ticker": "D05.SI", "tags": ["Finanzen", "SG"], "watchlist": True},
    {"ticker": "8001.T", "tags": ["Trading", "JP"], "watchlist": True},
    {"ticker": "O39.SI", "tags": ["Finanzen", "SG"], "watchlist": True},
    {"ticker": "RI.PA", "tags": ["Consumer", "FR"], "watchlist": True},
    {"ticker": "HNR1.DE", "tags": ["Finanzen", "DE"], "watchlist": True},
    {"ticker": "BAS.DE", "tags": ["Chemie", "DE"], "watchlist": True}
]

def daten_generieren():
    json_output = []
    print(f"=== STARTE AKTUALISIERUNG FÜR {len(AKTIEN_KONFIGURATION)} AKTIEN ===")
    
    for i, aktie in enumerate(AKTIEN_KONFIGURATION):
        symbol = aktie["ticker"]
        try:
            t = yf.Ticker(symbol, session=session)
            
            hist_5y = t.history(period="5y")
            if hist_5y.empty:
                hist_5y = t.history(period="1y")
            if hist_5y.empty:
                hist_5y = t.history(period="5d")

            if hist_5y.empty:
                print(f"[{i+1}/{len(AKTIEN_KONFIGURATION)}] {symbol}: Keine Kursdaten gefunden.")
                continue

            aktueller_kurs = float(hist_5y['Close'].iloc[-1])
            avg_5y_kurs = float(hist_5y['Close'].mean())
            abweichung_5y = ((aktueller_kurs - avg_5y_kurs) / avg_5y_kurs) * 100

            name = symbol
            kgv = None
            kcv = None
            dividendenrendite = None
            ex_dividende_str = "-"
            payout_str = "-"

            try:
                info = t.info or {}
                name = info.get("longName", symbol)
                kgv = info.get("trailingPE")
                kcv = info.get("priceToCashflow")
                
                div_yield = info.get("dividendYield")
                if div_yield:
                    dividendenrendite = float(div_yield) * 100 if float(div_yield) < 1 else float(div_yield)

                ex_div = info.get("exDividendDate")
                if ex_div:
                    ex_dividende_str = datetime.fromtimestamp(ex_div).strftime('%Y-%m-%d')
                
                pay_date = info.get("payoutDate")
                if pay_date:
                    payout_str = datetime.fromtimestamp(pay_date).strftime('%Y-%m-%d')
            except Exception:
                pass 

            aktie_daten = {
                "name": str(name),
                "ticker": str(symbol),
                "kurs": float(aktueller_kurs),
                "kgv": float(kgv) if kgv else None,
                "kcv": float(kcv) if kcv else None,
                "dividendenrendite": float(dividendenrendite) if dividendenrendite else None,
                "abweichung5y": float(abweichung_5y),
                "exDividendDate": ex_dividende_str,
                "payoutDate": payout_str,
                "watchlist": bool(aktie["watchlist"]),
                "tags": aktie["tags"]
            }
            json_output.append(aktie_daten)
            print(f"[{i+1}/{len(AKTIEN_KONFIGURATION)}] OK: {symbol} ({aktueller_kurs:.2f})")
            
        except Exception as e:
            print(f"[{i+1}/{len(AKTIEN_KONFIGURATION)}] Fehler bei {symbol}: {e}")
            
        time.sleep(0.8)
        
    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
    print(f"=== FERTIG! daten.json mit {len(json_output)} Einträgen gespeichert. ===")

if __name__ == "__main__":
    daten_generieren()
