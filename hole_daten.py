import json
import time
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from curl_cffi import requests

session = requests.Session(impersonate="chrome")

AKTIEN_KONFIGURATION = [
    # --- DEINE BEREITS VORHANDENEN AKTIEN (Depot) ---
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

    # --- WATCHLIST (AUS DEINEN SCREENSHOTS) ---
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

# (Die restlichen Funktionen bleiben exakt gleich wie im vorherigen Skript)
def berechne_historische_durchschnitte(ticker, shares_outstanding):
    kgv_historie, kcv_historie = [], []
    try:
        financials = ticker.financials
        cashflow = ticker.cashflow
        if financials is not None and not financials.empty:
            net_income_keys = [idx for idx in financials.index if 'Net Income' in str(idx)]
            if net_income_keys:
                row_key = net_income_keys[0]
                for datum in financials.columns:
                    datum_naive = datum.replace(tzinfo=None) if hasattr(datum, 'tzinfo') else datum
                    try:
                        h_data = ticker.history(start=datum_naive - timedelta(days=7), end=datum_naive + timedelta(days=7))
                        net_income = financials.loc[row_key, datum]
                        if not h_data.empty and pd.notna(net_income) and net_income != 0:
                            hist_close = h_data['Close'].iloc[-1]
                            kgv_historie.append((hist_close * shares_outstanding) / net_income)
                    except:
                        continue
        if cashflow is not None and not cashflow.empty:
            ocf_keys = [idx for idx in cashflow.index if 'Operating Cash Flow' in str(idx) or 'Cash Flow From Operating Activities' in str(idx)]
            if ocf_keys:
                row_key = ocf_keys[0]
                for datum in cashflow.columns:
                    datum_naive = datum.replace(tzinfo=None) if hasattr(datum, 'tzinfo') else datum
                    try:
                        h_data = ticker.history(start=datum_naive - timedelta(days=7), end=datum_naive + timedelta(days=7))
                        ocf = cashflow.loc[row_key, datum]
                        if not h_data.empty and pd.notna(ocf) and ocf != 0:
                            kcv_historie.append((hist_close * shares_outstanding) / ocf)
                    except:
                        continue
    except:
        pass
    return (sum(kgv_historie)/len(kgv_historie) if kgv_historie else None), (sum(kcv_historie)/len(kcv_historie) if kcv_historie else None)

def daten_generieren():
    json_output = []
    print(f"=== STARTE AKTUALISIERUNG FÜR {len(AKTIEN_KONFIGURATION)} AKTIEN ===")
    
    for aktie in AKTIEN_KONFIGURATION:
        symbol = aktie["ticker"]
        print(f"Verarbeite: {symbol}...")
        try:
            t = yf.Ticker(symbol, session=session)
            hist_prices = t.history(period="1y")
            aktueller_kurs = float(hist_prices['Close'].iloc[-1]) if not hist_prices.empty else (t.fast_info.get('lastPrice', 0.0) if hasattr(t, 'fast_info') else 0.0)
            
            if not aktueller_kurs or aktueller_kurs == 0:
                continue

            shares_outstanding = t.fast_info.get('shares', 1) if hasattr(t, 'fast_info') else 1
            market_cap = t.fast_info.get('marketCap') if hasattr(t, 'fast_info') else None
            if not market_cap: market_cap = aktueller_kurs * shares_outstanding

            name = symbol
            try:
                info = t.info
                if info and info.get("longName"): name = info.get("longName")
            except:
                pass

            aktie_daten = {
                "name": str(name),
                "ticker": str(symbol),
                "kurs": float(aktueller_kurs),
                "watchlist": bool(aktie["watchlist"]),
                "tags": aktie["tags"]
            }
            json_output.append(aktie_daten)
            print(f"   -> OK: {name} ({aktueller_kurs:.2f})")
        except Exception as e:
            print(f"   -> Fehler bei {symbol}: {e}")
        time.sleep(0.3)
        
    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
    print("=== FERTIG! daten.json aktualisiert. ===")

if __name__ == "__main__":
    daten_generieren()
