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
                        hist_kurs_data = ticker.history(start=datum_naive - timedelta(days=7), end=datum_naive + timedelta(days=7))
                        net_income = financials.loc[row_key, datum]
                        if not hist_kurs_data.empty and pd.notna(net_income) and net_income != 0:
                            hist_close = hist_kurs_data['Close'].iloc[-1]
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
                        hist_kurs_data = ticker.history(start=datum_naive - timedelta(days=7), end=datum_naive + timedelta(days=7))
                        ocf = cashflow.loc[row_key, datum]
                        if not hist_kurs_data.empty and pd.notna(ocf) and ocf != 0:
                            hist_close = hist_kurs_data['Close'].iloc[-1]
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
    
    print(f"=== STARTE AKTUALISIERUNG: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} ===")
    
    for aktie in AKTIEN_KONFIGURATION:
        symbol = aktie["ticker"]
        print(f"\nVerarbeite Ticker: {symbol}...")
        
        try:
            t = yf.Ticker(symbol)
            info = {}
            try:
                info = t.info
            except Exception as e:
                print(f"   ⚠️ Warnung: Konnte .info für {symbol} nicht vollständig laden ({e})")
            
            # Basisdaten sichern
            name = info.get("longName", info.get("shortName", symbol)) if info else symbol
            waehrung = info.get("currency", "USD") if info else "USD"
            aktueller_kurs = info.get("currentPrice", info.get("regularMarketPrice", 0)) if info else 0
            kurs_formatiert = f"{aktueller_kurs:.2f} {waehrung}" if aktueller_kurs else "-"
            
            # Performance-Berechnung absichern
            perf_tag, perf_monat, perf_jahr, perf_5j = 0.0, 0.0, 0.0, 0.0
            try:
                hist_prices = t.history(period="5y")
                if not hist_prices.empty:
                    heute_close = hist_prices['Close'].iloc[-1]
                    if len(hist_prices) > 1:
                        perf_tag = ((heute_close - hist_prices['Close'].iloc[-2]) / hist_prices['Close'].iloc[-2]) * 100
                    if len(hist_prices) > 21:
                        perf_monat = ((heute_close - hist_prices['Close'].iloc[-21]) / hist_prices['Close'].iloc[-21]) * 100
                    if len(hist_prices) > 252:
                        perf_jahr = ((heute_close - hist_prices['Close'].iloc[-252]) / hist_prices['Close'].iloc[-252]) * 100
                    perf_5j = ((heute_close - hist_prices['Close'].iloc[0]) / hist_prices['Close'].iloc[0]) * 100
            except Exception as e:
                print(f"   ⚠️ Kurs-Performance fehlerhaft für {symbol}: {e}")

            # Dividende absichern
            dividende = None
            if info:
                dividende = info.get("dividendYield", info.get("trailingAnnualDividendYield"))
            
            # KGV & KCV absichern
            kgv = None
            if info:
                kgv = info.get("trailingPE", info.get("forwardPE"))
                
            kcv = None
            if info:
                market_cap = info.get("marketCap")
                operating_cashflow = info.get("operatingCashflow")
                if market_cap and operating_cashflow:
                    kcv = market_cap / operating_cashflow
                
            # Historische 5J-Werte absichern
            shares_outstanding = info.get("sharesOutstanding", 1) if info else 1
            kgv_5j, kcv_5j = berechne_historische_durchschnitte(t, shares_outstanding)
            
            # Ex-Date absichern
            ex_date = "-"
            if info and info.get("exDividendDate"):
                try:
                    ex_date = datetime.fromtimestamp(info["exDividendDate"], tz=timezone.utc).strftime('%d.%m.%Y')
                except:
                    pass
            
            # Logo URL via Fallback-Dienst generieren (yfinance liefert oft keine funktionierenden Logos mehr)
            logo_symbol = symbol.split(".")[0].lower()
            logo_url = f"https://logo.clearbit.com/{logo_symbol}.com"
            
            # Sauberes Datenpaket packen
            aktie_daten = {
                "name": name,
                "ticker": symbol,
                "kurs": kurs_formatiert,
                "perfTag": float(perf_tag),
                "perfMonat": float(perf_monat),
                "perfJahr": float(perf_jahr),
                "perf5J": float(perf_5j),
                "dividende": float(dividende) if isinstance(dividende, (int, float)) else None,
                "kgv": float(kgv) if isinstance(kgv, (int, float)) else None,
                "kgv5J": float(kgv_5j) if isinstance(kgv_5j, (int, float)) else None,
                "kcv": float(kcv) if isinstance(kcv, (int, float)) else None,
                "kcv5J": float(kcv_5j) if isinstance(kcv_5j, (int, float)) else None,
                "watchlist": aktie["watchlist"],
                "tags": aktie["tags"],
                "logoUrl": logo_url,
                "monate": "-", 
                "frequenz": "-",
                "exDate": ex_date
            }
            
            json_output.append(aktie_daten)
            print(f"   -> {name} erfolgreich hinzugefügt.")
            
        except Exception as e:
            print(f"❌ Fehler bei Ticker {symbol}: {e}")
        
        time.sleep(1)
        
    # Datei schreiben
    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
        
    print(f"\n=== FERTIG! 'daten.json' wurde erfolgreich generiert ({len(json_output)} Aktien). ===")

if __name__ == "__main__":
    daten_generieren()
