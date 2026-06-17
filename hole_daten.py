import yfinance as yf
import json
import sys

# Deine vollständige Liste der 51 angeforderten Aktien mit optimierten Ticker-Symbolen für Yahoo Finance
meine_aktien = [
    {"symbol": "MSFT", "name": "Microsoft", "logoUrl": "https://logo.clearbit.com/microsoft.com"},
    {"symbol": "TSM", "name": "TSMC", "logoUrl": "https://logo.clearbit.com/tsmc.com"},
    {"symbol": "SAP.DE", "name": "SAP", "logoUrl": "https://logo.clearbit.com/sap.com"},
    {"symbol": "ORCL", "name": "Oracle", "logoUrl": "https://logo.clearbit.com/oracle.com"},
    {"symbol": "AVGO", "name": "Broadcom", "logoUrl": "https://logo.clearbit.com/broadcom.com"},
    {"symbol": "ASML", "name": "ASML", "logoUrl": "https://logo.clearbit.com/asml.com"},
    {"symbol": "GOOGL", "name": "Alphabet", "logoUrl": "https://logo.clearbit.com/google.com"},
    {"symbol": "QCOM", "name": "Qualcomm", "logoUrl": "https://logo.clearbit.com/qualcomm.com"},
    {"symbol": "NOW", "name": "ServiceNow", "logoUrl": "https://logo.clearbit.com/servicenow.com"},
    {"symbol": "INTU", "name": "Intuit", "logoUrl": "https://logo.clearbit.com/intuit.com"},
    {"symbol": "JPM", "name": "JPMorgan Chase", "logoUrl": "https://logo.clearbit.com/jpmorganchase.com"},
    {"symbol": "HSBA.L", "name": "HSBC", "logoUrl": "https://logo.clearbit.com/hsbc.com"},
    {"symbol": "SAN.PA", "name": "Sanofi", "logoUrl": "https://logo.clearbit.com/sanofi.com"},
    {"symbol": "BLK", "name": "BlackRock", "logoUrl": "https://logo.clearbit.com/blackrock.com"},
    {"symbol": "ALV.DE", "name": "Allianz", "logoUrl": "https://logo.clearbit.com/allianz.com"},
    {"symbol": "MUV2.DE", "name": "Munich Re", "logoUrl": "https://logo.clearbit.com/munichre.com"},
    {"symbol": "SIE.DE", "name": "Siemens", "logoUrl": "https://logo.clearbit.com/siemens.com"},
    {"symbol": "SU.PA", "name": "Schneider Electric", "logoUrl": "https://logo.clearbit.com/se.com"},
    {"symbol": "HON", "name": "Honeywell", "logoUrl": "https://logo.clearbit.com/honeywell.com"},
    {"symbol": "CAT", "name": "Caterpillar", "logoUrl": "https://logo.clearbit.com/caterpillar.com"},
    {"symbol": "DE", "name": "John Deere", "logoUrl": "https://logo.clearbit.com/deere.com"},
    {"symbol": "ABBN.SW", "name": "ABB", "logoUrl": "https://logo.clearbit.com/abb.com"},
    {"symbol": "6861.T", "name": "Keyence", "logoUrl": "https://logo.clearbit.com/keyence.com"},
    {"symbol": "DG.PA", "name": "Vinci", "logoUrl": "https://logo.clearbit.com/vinci.com"},
    {"symbol": "PH", "name": "Parker-Hannifin", "logoUrl": "https://logo.clearbit.com/parker.com"},
    {"symbol": "RIO", "name": "Rio Tinto", "logoUrl": "https://logo.clearbit.com/riotinto.com"},
    {"symbol": "LIN", "name": "Linde", "logoUrl": "https://logo.clearbit.com/linde.com"},
    {"symbol": "AI.PA", "name": "Air Liquide", "logoUrl": "https://logo.clearbit.com/airliquide.com"},
    {"symbol": "MC.PA", "name": "LVMH", "logoUrl": "https://logo.clearbit.com/lvmh.com"},
    {"symbol": "TTE", "name": "TotalEnergies", "logoUrl": "https://logo.clearbit.com/totalenergies.com"},
    {"symbol": "NEE", "name": "NextEra Energy", "logoUrl": "https://logo.clearbit.com/nexteraenergy.com"},
    {"symbol": "ORSTED.CO", "name": "Ørsted", "logoUrl": "https://logo.clearbit.com/orsted.com"},
    {"symbol": "VIE.PA", "name": "Veolia", "logoUrl": "https://logo.clearbit.com/veolia.com"},
    {"symbol": "IBE.MC", "name": "Iberdrola", "logoUrl": "https://logo.clearbit.com/iberdrola.com"},
    {"symbol": "LLY", "name": "Eli Lilly", "logoUrl": "https://logo.clearbit.com/lilly.com"},
    {"symbol": "ROG.SW", "name": "Roche", "logoUrl": "https://logo.clearbit.com/roche.com"},
    {"symbol": "NOVN.SW", "name": "Novartis", "logoUrl": "https://logo.clearbit.com/novartis.com"},
    {"symbol": "ABBV", "name": "AbbVie", "logoUrl": "https://logo.clearbit.com/abbvie.com"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "logoUrl": "https://logo.clearbit.com/jnj.com"},
    {"symbol": "AMZN", "name": "Amazon", "logoUrl": "https://logo.clearbit.com/amazon.com"},
    {"symbol": "PG", "name": "Procter & Gamble", "logoUrl": "https://logo.clearbit.com/pg.com"},
    {"symbol": "NESN.SW", "name": "Nestlé", "logoUrl": "https://logo.clearbit.com/nestle.com"},
    {"symbol": "MDLZ", "name": "Mondelez", "logoUrl": "https://logo.clearbit.com/mondelezinternational.com"},
    {"symbol": "KO", "name": "Coca-Cola", "logoUrl": "https://logo.clearbit.com/coca-colacompany.com"},
    {"symbol": "MCD", "name": "McDonald's", "logoUrl": "https://logo.clearbit.com/mcdonalds.com"},
    {"symbol": "WMT", "name": "Walmart", "logoUrl": "https://logo.clearbit.com/walmart.com"},
    {"symbol": "FPE3.DE", "name": "Fuchs SE", "logoUrl": "https://logo.clearbit.com/fuchs.com"},
    {"symbol": "PLD", "name": "Prologis", "logoUrl": "https://logo.clearbit.com/prologis.com"},
    {"symbol": "KRN.DE", "name": "Krones", "logoUrl": "https://logo.clearbit.com/krones.com"},
    {"symbol": "MMK.VI", "name": "Mayr-Melnhof Karton", "logoUrl": "https://logo.clearbit.com/mm-karton.com"},
    {"symbol": "IBN", "name": "ICICI Bank", "logoUrl": "https://logo.clearbit.com/icicibank.com"}
]

aktien_daten = []

print("Starte automatische Datenabfrage von Yahoo Finance für 51 Aktien...")

for aktie in meine_aktien:
    try:
        ticker = yf.Ticker(aktie["symbol"])
        
        # Historische Daten abrufen (1 Jahr für Jahres-Perf., 1 Monat für Monats-Perf.)
        hist_1y = ticker.history(period="1y")
        hist_1m = ticker.history(period="1mo")
        
        # Fundamental-Infos laden
        info = ticker.info
        
        if not hist_1y.empty and not hist_1m.empty:
            aktueller_kurs = hist_1y['Close'].iloc[-1]
            kurs_vor_1m = hist_1m['Close'].iloc[0] if len(hist_1m) > 0 else aktueller_kurs
            kurs_vor_1y = hist_1y['Close'].iloc[0] if len(hist_1y) > 0 else aktueller_kurs
            
            # Prozentuale Performance berechnen
            perf_monat = ((aktueller_kurs - kurs_vor_1m) / kurs_vor_1m) * 100
            perf_jahr = ((aktueller_kurs - kurs_vor_1y) / kurs_vor_1y) * 100
            
            # Währungskürzel anhand des Marktplatzes bestimmen
            if ".DE" in aktie["symbol"] or ".PA" in aktie["symbol"] or ".MC" in aktie["symbol"] or ".VI" in aktie["symbol"]:
                waehrung = "€"
            elif ".SW" in aktie["symbol"]:
                waehrung = "CHF"
            elif ".L" in aktie["symbol"]:
                waehrung = "GBp"
            elif ".CO" in aktie["symbol"]:
                waehrung = "DKK"
            elif ".T" in aktie["symbol"]:
                waehrung = "¥"
            else:
                waehrung = "$"
            
            # KGV auslesen (bevorzugt das rollierende KGV, alternativ das geschätzte KGV)
            kgv = info.get("trailingPE") or info.get("forwardPE") or 0
            
            aktien_daten.append({
                "name": aktie["name"],
                "logoUrl": aktie["logoUrl"],
                "kurs": f"{aktueller_kurs:.2f} {waehrung}",
                "perfMonat": perf_monat,
                "perfJahr": perf_jahr,
                "kgv": kgv
            })
            print(f"Erfolgreich: {aktie['name']} -> KGV: {kgv}")
        else:
            print(f"Warnung: Keine Kurshistorie für {aktie['name']} ({aktie['symbol']})")
            
    except Exception as e:
        print(f"Fehler bei Aktie {aktie['name']}: {e}", file=sys.stderr)

# Speichern als JSON-Datei für das Frontend
output_filename = "daten.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(aktien_daten, f, ensure_ascii=False, indent=4)

print(f"Skript beendet. {len(aktien_daten)} Aktien in '{output_filename}' gesichert.")
