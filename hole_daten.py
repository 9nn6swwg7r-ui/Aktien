import json
import time
from datetime import datetime, timedelta, timezone
import yfinance as yf
import pandas as pd

# ==============================================================================
# HIER DEINE AKTIEN EINTRAGEN
# ==============================================================================
AKTIEN_KONFIGURATION = [
    {"ticker": "MSFT", "tags": ["Tech", "MegaCap", "US"], "watchlist": False},
    {"ticker": "AAPL", "tags": ["Tech", "Hardware", "US"], "watchlist": False},
    {"ticker": "O", "tags": ["REIT", "Immobilien", "Monatszahler"], "watchlist": True},
    {"ticker": "NSRGY", "tags": ["Konsum", "Dividende", "CH"], "watchlist": False}
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
    
    print(f"=== STARTE REPARIERTE AKTUALISIERUNG: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} ===")
    
    for aktie in AKTIEN_KONFIGURATION:
        symbol = aktie["ticker"]
        print(f"\nVerarbeite Ticker: {symbol}...")
        
        try:
            t = yf.Ticker(symbol)
            
            # 1. Kurs & Historie laden (Der stabilste Endpunkt bei Yahoo)
            hist_prices = t.history(period="5y")
            if hist_prices.empty:
                print(f"   ❌ Keine Kursdaten für {symbol} gefunden. Überspringe.")
                continue
                
            aktueller_kurs = float(hist_prices['Close'].iloc[-1])
            
            # Währung bestimmen über Metadaten
            waehrung = "USD"
            try:
                if hasattr(t, 'history_metadata') and t.history_metadata:
                    waehrung = t.history_metadata.get('currency', 'USD')
                elif hasattr(t, 'fast_info') and t.fast_info:
                    waehrung = t.fast_info.get('currency', 'USD')
            except:
                pass
                
            kurs_formatiert = f"{aktueller_kurs:.2f} {waehrung}"
            
            # 2. Performance berechnen
            perf_tag, perf_monat, perf_jahr, perf_5j = 0.0, 0.0, 0.0, 0.0
            heute_close = hist_prices['Close'].iloc[-1]
            if len(hist_prices) > 1:
                perf_tag = ((heute_close - hist_prices['Close'].iloc[-2]) / hist_prices['Close'].iloc[-2]) * 100
            if len(hist_prices) > 21:
                perf_monat = ((heute_close - hist_prices['Close'].iloc[-21]) / hist_prices['Close'].iloc[-21]) * 100
            if len(hist_prices) > 252:
                perf_jahr = ((heute_close - hist_prices['Close'].iloc[-252]) / hist_prices['Close'].iloc[-252]) * 100
            perf_5j = ((heute_close - hist_prices['Close'].iloc[0]) / hist_prices['Close'].iloc[0]) * 100

            # 3. Fundamentaldaten & Cashflow laden
            financials = t.financials
            cashflow = t.cashflow
            
            # Anteile für die Marktkapitalisierung bestimmen
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

            # 4. Dividendenrendite manuell aus den realen Ausschüttungen berechnen (365 Tage)
            dividende = None
            try:
                divs = t.dividends
                if not divs.empty:
                    tz_info = divs.index.tz
                    now_tz = datetime.now(tz_info) if tz_info else datetime.now()
                    one_year_ago = now_tz - timedelta(days=365)
                    divs_filtered = divs[divs.index > one_year_ago] if tz_info else divs[divs.index.replace(tzinfo=None) > one_year_ago]
                    
                    if not divs_filtered.empty:
                        dividende = divs_filtered.sum() / aktueller_kurs
            except:
                pass

            # 5. Aktuelles KGV berechnen (Market Cap / Letzter Jahresgewinn)
            kgv = None
            try:
                if financials is not None and not financials.empty:
                    net_income_keys = [idx for idx in financials.index if 'Net Income' in str(idx)]
                    if net_income_keys:
                        letzter_gewinn = financials.loc[net_income_keys[0]].iloc[0]
                        if letzter_gewinn and letzter_gewinn != 0:
                            kgv = market_cap / letzter_gewinn
            except:
                pass

            # 6. Aktuelles KCV berechnen (Market Cap / Operativer Cashflow)
            kcv = None
            try:
                if cashflow is not None and not cashflow.empty:
                    ocf_keys = [idx for idx in cashflow.index if 'Operating Cash Flow' in str(idx) or 'Cash Flow From Operating Activities' in str(idx)]
                    if ocf_keys:
                        letzter_ocf = cashflow.loc[ocf_keys[0]].iloc[0]
                        if letzter_ocf and letzter_ocf != 0:
                            kcv = market_cap / letzter_ocf
            except:
                pass
                
            # 7. Historische 5J-Durchschnitte ermitteln
            kgv_5j, kcv_5j = berechne_historische_durchschnitte(t, shares_outstanding)
            
            # Name bestimmen
            name = symbol
            try:
                if hasattr(t, 'info') and t.info and t.info.get("longName"):
                    name = t.info.get("longName")
            except:
                pass

            def clean(val):
                if val is None or pd.isna(val) or val == "None": return None
                return float(val)

            # Paket schnüren
            aktie_daten = {
                "name": str(name),
                "ticker": str(symbol),
                "kurs": str(kurs_formatiert),
                "perfTag": clean(perf_tag) or 0.0,
                "perfMonat": clean(perf_monat) or 0.0,
                "perfJahr": clean(perf_jahr) or 0.0,
                "perf5J": clean(perf_5j) or 0.0,
                "dividende": clean(dividende),
                "kgv": clean(kgv),
                "kgv5J": clean(kgv_5j),
                "kcv": clean(kcv),
                "kcv5J": clean(kcv_5j),
                "watchlist": bool(aktie["watchlist"]),
                "tags": aktie["tags"],
                "logoUrl": f"https://logo.clearbit.com/{symbol.split('.')[0].lower()}.com",
                "monate": "-", 
                "frequenz": "-",
                "exDate": "-"
            }
            
            json_output.append(aktie_daten)
            print(f"   -> {name} erfolgreich mit echten Werten erfasst! ({kurs_formatiert})")
            
        except Exception as e:
            print(f"❌ Fehler bei Ticker {symbol}: {e}")
        
        time.sleep(1)
        
    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
        
    print(f"\n=== FERTIG! 'daten.json' wurde erfolgreich generiert ({len(json_output)} Aktien). ===")

if __name__ == "__main__":
    daten_generieren()
