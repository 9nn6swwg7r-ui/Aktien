import yfinance as yf
import json
import datetime

# Deine Liste der 51 Werte mit korrekten Ticker-Anhängseln
ticker_map = {
    "MSFT": "MSFT", "TSM": "TSM", "SAP": "SAP.DE", "ORCL": "ORCL", "AVGO": "AVGO",
    "ASML": "ASML", "GOOGL": "GOOGL", "QCOM": "QCOM", "NOW": "NOW", "INTU": "INTU",
    "JPM": "JPM", "HSBA": "HSBA.L", "Sanofi": "SNY", "BLK": "BLK", "ALV": "ALV.DE",
    "MUV2": "MUV2.DE", "SIE": "SIE.DE", "SU": "SU.PA", "HON": "HON", "CAT": "CAT",
    "DE": "DE", "ABBN": "ABBN.SW", "6861": "6861.T", "DG": "DG.PA", "PH": "PH",
    "RIO": "RIO", "LIN": "LIN", "AI": "AI.PA", "LVMH": "MC.PA", "TTE": "TTE",
    "NEE": "NEE", "ORSTED": "ORSTED.CO", "VIE": "VIE.PA", "IBE": "IBE.MC",
    "LLY": "LLY", "ROG": "ROG.SW", "NOVN": "NOVN.SW", "ABBV": "ABBV", "JNJ": "JNJ",
    "AMZN": "AMZN", "PG": "PG", "NESN": "NESN.SW", "MDLZ": "MDLZ", "KO": "KO",
    "MCD": "MCD", "WMT": "WMT", "FPE3": "FPE3.DE", "PLD": "PLD", "KRN": "KRN.DE",
    "MMK": "MMK.VI", "Icici": "IBN"
}

daten = []

for name, sym in ticker_map.items():
    try:
        t = yf.Ticker(sym)
        info = t.info
        hist = t.history(period="5y")
        
        price = info.get("currentPrice") or info.get("regularMarketPrice", 0)
        avg_5y = hist['Close'].mean()
        
        daten.append({
            "name": info.get("longName", name),
            "price": price,
            "perf1M": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21] * 100),
            "perf1J": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-252]) / hist['Close'].iloc[-252] * 100),
            "divYield": (info.get("dividendYield", 0) or 0) * 100,
            "kgv": info.get("trailingPE", 0) or 0,
            "kcv": info.get("priceToCashflow", 0) or 0,
            "abweichung5J": ((price - avg_5y) / avg_5y) * 100,
            "exDate": info.get("exDividendDate", "N/A")
        })
    except: continue

with open("daten.json", "w", encoding="utf-8") as f:
    json.dump(daten, f, indent=4)
