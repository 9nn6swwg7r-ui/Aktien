import yfinance as yf
import json

# Deine vollständige Liste
symbole = ["MSFT", "TSM", "SAP.DE", "ORCL", "AVGO", "ASML", "GOOGL", "QCOM", "NOW", "INTU", "JPM", "HSBA.L", "SAN.PA", "BLK", "ALV.DE", "MUV2.DE", "SIE.DE", "SU.PA", "HON", "CAT", "DE", "ABBN.SW", "6861.T", "DG.PA", "PH", "RIO", "LIN", "AI.PA", "MC.PA", "TTE", "NEE", "ORSTED.CO", "VIE.PA", "IBE.MC", "LLY", "ROG.SW", "NOVN.SW", "ABBV", "JNJ", "AMZN", "PG", "NESN.SW", "MDLZ", "KO", "MCD", "WMT", "FPE3.DE", "PLD", "KRN.DE", "MMK.VI", "IBN", "1398.HK", "TPE.WA", "DNP.WA", "LHA.DE", "FIH-U.TO", "EOAN.DE", "CMCSA", "KHC", "VNA.DE", "PKO.WA", "DNB.OL", "6506.T", "6954.T", "YAR.OL", "VZ", "DHL.DE", "EVD.DE", "VER.VI", "CGNX", "EUK3.DE", "BMW3.DE", "PDD", "BEI.DE", "SIX2.DE", "ABBN.SW", "STR.VI", "FRM.DE", "6367.T", "ADSK", "ADBE", "SIKA.SW", "TER", "ROK"]

daten = []

for sym in symbole:
    try:
        t = yf.Ticker(sym)
        info = t.info
        hist = t.history(period="1mo")
        price = info.get("currentPrice") or info.get("regularMarketPrice", 0)
        
        daten.append({
            "name": info.get("longName", sym),
            "symbol": sym,
            "tags": info.get("industry", "N/A"), # Platzhalter für Branchen-Tags
            "price": price,
            "currency": info.get("currency", "USD"),
            "changeHeute": info.get("regularMarketChangePercent", 0),
            "perfMonat": ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100) if not hist.empty else 0,
            "divYield": (info.get("dividendYield", 0) or 0) * 100,
            "kgv": info.get("trailingPE", 0) or 0,
            "kcv": info.get("priceToCashflow", 0) or 0
        })
    except:
        continue

with open("daten.json", "w", encoding="utf-8") as f:
    json.dump(daten, f, indent=4)
