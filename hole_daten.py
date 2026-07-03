import json
import time
from datetime import datetime, timedelta, timezone
import yfinance as yf
import pandas as pd

# ==============================================================================
# HIER DEINE AKTIEN EINTRAGEN (Beliebig erweiterbar)
# ==============================================================================
AKTIEN_KONFIGURATION = [
    {"ticker": "MSFT", "tags": ["Tech", "MegaCap", "US"], "watchlist": False},
    {"ticker": "AAPL", "tags": ["Tech", "Hardware", "US"], "watchlist": False},
    {"ticker": "O", "tags": ["REIT", "Immobilien", "Monatszahler"], "watchlist": True},
    {"ticker": "NSRGY", "tags": ["Konsum", "Dividende", "CH"], "watchlist": False}
]

def berechne_historische_durchschnitte(ticker, shares_outstanding):
    """
    Holt die historischen Bilanzen (Financials) und Cashflows der letzten Jahre
    und errechnet die realen 5-Jahres-Durchschnitte für KGV und KCV.
    """
    kgv_historie = []
    kcv_historie = []
    
    try:
        # Jährliche Gewinn- und Verlustrechnung sowie Cashflow abrufen
        financials = ticker.financials
        cashflow = ticker.cashflow
        
        # 1. 5-Jahres-KGV Annäherung über den historischen Nettogewinn
        if financials is not None and not financials.empty:
            net_income_keys = [idx for idx in financials.index if 'Net Income' in str(idx)]
            if net_income_keys:
                row_key = net_income_keys[0]
                for datum in financials.columns:
                    # Zeitzone entfernen, um Berechnungen mit timedelta zu erlauben
                    datum_naive = datum.replace(tzinfo=None) if hasattr(datum, 'tzinfo') else datum
                    
                    hist_kurs_data = ticker.history(start=datum_naive - timedelta(days=5), end=datum_naive + timedelta(days=5))
                    net_income = financials.loc[row_key, datum]
                    
                    if not hist_kurs_data.empty and pd.notna(net_income) and net_income != 0:
                        hist_close = hist_kurs_data['Close'].iloc[-1]
                        hist_market_cap = hist_close * shares_outstanding
                        kgv_historie.append(hist_market_cap / net_income)

        # 2. 5-Jahres-KCV Annäherung über den operativen Cashflow
        if cashflow is not None and not cashflow.empty:
            ocf_keys = [idx for idx in cashflow.index if 'Operating Cash Flow' in str(idx) or 'Cash Flow From Operating Activities' in str(idx)]
            if ocf_keys:
                row_key = ocf_keys[0]
                for datum in cashflow.columns:
                    # Zeitzone entfernen
                    datum_naive = datum.replace(tzinfo=None) if hasattr(datum, 'tzinfo') else datum
                    
                    hist_kurs_data = ticker.history(start=datum_naive - timedelta(days=5), end=datum_naive + timedelta(days=5))
                    ocf = cashflow.loc[row_key, datum]
                    
                    if not hist_kurs_data.empty and pd.notna(ocf) and ocf != 0:
                        hist_close = hist_kurs_data['Close'].iloc[-1]
                        hist_market_cap = hist_close * shares_outstanding
                        kcv_historie.append(hist_market_cap / ocf)
                        
    except Exception as e:
        print(f"   -> Historische Kennzahlen für diesen Ticker unvollständig ({e})")

    avg_kgv = sum(kgv_historie) / len(kgv_historie) if kgv_historie else "None"
    avg_kcv = sum(kcv_historie) / len(kcv_historie) if kcv_historie else "None"
    
    return avg_kgv, avg_kcv

def daten_generieren():
    json_output = []
    
    print(f"=== STARTE AKTUALISIERUNG: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} ===")
    
    for aktie in AKTIEN_KONFIGURATION:
        symbol = aktie["ticker"]
        print(f"\nVerarbeite Ticker: {symbol}...")
        
        try:
            t = yf.Ticker(symbol)
            info = t.info
            
            # Basisinformationen auslesen
            name = info.get("longName", info.get("shortName", symbol))
            waehrung = info.get("currency", "EUR")
            aktueller_kurs = info.get("currentPrice", info.get("regularMarketPrice", 0))
            kurs_formatiert = f"{aktueller_kurs:.2f} {waehrung}" if aktueller_kurs else "-"
            
            # Historische Kurs-Performance berechnen (Tag, Monat, Jahr, 5 Jahre)
            hist_prices = t.history(period="5y")
            perf_tag, perf_monat, perf_jahr, perf_5j = 0.0, 0.0, 0.0, 0.0
            
            if not hist_prices.empty:
                heute_close = hist_prices['Close'].iloc[-1]
                
                # Performance Heute
                if len(hist_prices) > 1:
                    gestern_close = hist_prices['Close'].iloc[-2]
                    perf_tag = ((heute_close - gestern_close) / gestern_close) * 100
                
                # Performance 1 Monat
                if len(hist_prices) > 21:
                    monat_close = hist_prices['Close'].iloc[-21]
                    perf_monat = ((heute_close - monat_close) / monat_close) * 100
                    
                # Performance 1 Jahr
                if len(hist_prices) > 252:
                    jahr_close = hist_prices['Close'].iloc[-252]
                    perf_jahr = ((heute_close - jahr_close) / jahr_close) * 100
                    
                # Performance 5 Jahre
                start_5j_close = hist_prices['Close'].iloc[0]
                perf_5j = ((heute_close - start_5j_close)
