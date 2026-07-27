import json
import time
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

# ==============================================================================
# VOLLSTÄNDIGE DEPOT-AKTIEN-KONFIGURATION
# ==============================================================================
AKTIEN_KONFIGURATION = [
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
    {"ticker": "IBN", "tags": ["Finanzen", "IN"], "watchlist": False}
]

def berechne_historische_durchschnitte(ticker, shares_outstanding):
    kgv_historie = []
    kcv_historie = []
    
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
                            hist_market_cap = hist_close * shares_outstanding
                            kgv_historie.append(hist_market_cap / net_income)
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
                            hist_close = h_data['Close'].iloc[-1]
                            hist_market_cap = hist_close * shares_outstanding
                            kcv_historie.append(hist_market_cap / ocf)
                    except:
                        continue
                        
    except Exception as e:
        print(f"   -> Historische Kennzahlen unvollständig: {e}")

    avg_kgv = sum(kgv_historie) / len(kgv_historie) if kgv_historie else None
    avg_kcv = sum(kcv_historie) / len(kcv_historie) if kcv_historie else None
    
    return avg_kgv, avg_kcv

def daten_generieren():
    json_output = []
    
    print(f"=== STARTE AKTUALISIERUNG FÜR {len(AKTIEN_KONFIGURATION)} AKTIEN: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} ===")
    
    for aktie in AKTIEN_KONFIGURATION:
        symbol = aktie["ticker"]
        print(f"\nVerarbeite Ticker: {symbol}...")
        
        try:
            t = yf.Ticker(symbol)
            
            # 1. Kurs & Historie laden mit Fallback
            hist_prices = t.history(period="1y")
            if hist_prices.empty:
                print(f"   ⚠️ Keine Historie für {symbol}, versuche Fast Info...")
                aktueller_kurs = t.fast_info.get('lastPrice', 0.0) if hasattr(t, 'fast_info') else 0.0
            else:
                aktueller_kurs = float(hist_prices['Close'].iloc[-1])

            if not aktueller_kurs or aktueller_kurs == 0:
                print(f"   ❌ Konnte keinen Kurs für {symbol} ermitteln. Überspringe.")
                continue

            # Performance Standardwerte
            perf_tag, perf_monat, perf_jahr, perf_5j = 0.0, 0.0, 0.0, 0.0
            if not hist_prices.empty and len(hist_prices) > 1:
                heute_close = hist_prices['Close'].iloc[-1]
                perf_tag = ((heute_close - hist_prices['Close'].iloc[-2]) / hist_prices['Close'].iloc[-2]) * 100
                if len(hist_prices) > 21:
                    perf_monat = ((heute_close - hist_prices['Close'].iloc[-21]) / hist_prices['Close'].iloc[-21]) * 100
                if len(hist_prices) > 252:
                    perf_jahr = ((heute_close - hist_prices['Close'].iloc[-252]) / hist_prices['Close'].iloc[-252]) * 100
                perf_5j = ((heute_close - hist_prices['Close'].iloc[0]) / hist_prices['Close'].iloc[0]) * 100

            # Fundamentaldaten sicher auslesen
            shares_outstanding = 1
            market_cap = None
            try:
                if hasattr(t, 'fast_info') and t.fast_info:
                    shares_outstanding = t.fast_info.get('shares', 1)
                    market_cap = t.fast_info.get('marketCap')
            except:
                pass
                
            if not market_cap or market_cap == 0:
                market_cap = aktueller_kurs * shares_outstanding

            # Dividende berechnen
            dividende = 0.0
            try:
                divs = t.dividends
                if not divs.empty:
                    tz_info = divs.index.tz
                    now_tz = datetime.now(tz_info) if tz_info else datetime.now()
                    one_year_ago = now_tz - timedelta(days=365)
                    divs_filtered = divs[divs.index > one_year_ago] if tz_info else divs[divs.index.replace(tzinfo=None) > one_year_ago]
                    if not divs_filtered.empty:
                        dividende = float(divs_filtered.sum() / aktueller_kurs)
            except:
                pass

            # KGV & KCV ermitteln
            kgv, kcv = None, None
            try:
                financials = t.financials
                if financials is not None and not financials.empty:
                    net_income_keys = [idx for idx in financials.index if 'Net Income' in str(idx)]
                    if net_income_keys:
                        letzter_gewinn = financials.loc[net_income_keys[0]].iloc[0]
                        if letzter_gewinn and letzter_gewinn != 0:
                            kgv = market_cap / letzter_gewinn
            except:
                pass

            try:
                cashflow = t.cashflow
                if cashflow is not None and not cashflow.empty:
                    ocf_keys = [idx for idx in cashflow.index if 'Operating Cash Flow' in str(idx) or 'Cash Flow From Operating Activities' in str(idx)]
                    if ocf_keys:
                        letzter_ocf = cashflow.loc[ocf_keys[0]].iloc[0]
                        if letzter_ocf and letzter_ocf != 0:
                            kcv = market_cap / letzter_ocf
            except:
                pass

            # Historische Durchschnitte (mit Fehler-Sicherung)
            kgv_5j, kcv_5j = None, None
            try:
                kgv_5j, kcv_5j = berechne_historische_durchschnitte(t, shares_outstanding)
            except:
                pass

            # Name und Termine
            name = symbol
            ex_date, payout_date = "-", "-"
            try:
                info = t.info
                if info:
                    if info.get("longName"):
                        name = info.get("longName")
                    if info.get("exDividendDate"):
                        ex_date = datetime.fromtimestamp(info.get("exDividendDate")).strftime('%d.%m.%Y')
                    if info.get("dividendDate"):
                        payout_date = datetime.fromtimestamp(info.get("dividendDate")).strftime('%d.%m.%Y')
            except:
                pass

            def clean(val):
                if val is None or pd.isna(val) or str(val).lower() == "nan": return 0.0
                return float(val)

            aktie_daten = {
                "name": str(name),
                "ticker": str(symbol),
                "kurs": clean(aktueller_kurs),
                "perfTag": clean(perf_tag),
                "perfMonat": clean(perf_monat),
                "perfJahr": clean(perf_jahr),
                "perf5J": clean(perf_5j),
                "dividende": clean(dividende),
                "kgv": clean(kgv),
                "kgv5y": clean(kgv_5j),
                "kcv": clean(kcv),
                "kcv5y": clean(kcv_5j),
                "exDate": ex_date,
                "payoutDate": payout_date,
                "watchlist": bool(aktie["watchlist"]),
                "tags": aktie["tags"]
            }
            
            json_output.append(aktie_daten)
            print(f"   -> {name} erfolgreich erfasst! (Kurs: {aktueller_kurs:.2f})")
            
        except Exception as e:
            print(f"❌ Fehler bei Ticker {symbol}: {e}")
        
        time.sleep(0.3)
        
    # Sicherheitsnetz: Nur speichern, wenn auch wirklich Daten da sind!
    if len(json_output) > 0:
        with open("daten.json", "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)
        print(f"\n=== FERTIG! 'daten.json' mit {len(json_output)} Aktien generiert. ===")
    else:
        print("\n❌ ABBRUCH: Keine einzige Aktie konnte geladen werden. 'daten.json' wird nicht überschrieben!")

if __name__ == "__main__":
    daten_generieren()
