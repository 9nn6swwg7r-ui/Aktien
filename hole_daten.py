import yfinance as yf
import json
import sys

meine_aktien = [
    {"symbol": "MSFT", "name": "Microsoft", "logoUrl": "https://logo.clearbit.com/microsoft.com", "tags": ["Software", "Cloud", "KI"]},
    {"symbol": "TSM", "name": "TSMC", "logoUrl": "https://logo.clearbit.com/tsmc.com", "tags": ["Halbleiter", "Chips", "Tech"]},
    {"symbol": "SAP.DE", "name": "SAP", "logoUrl": "https://logo.clearbit.com/sap.com", "tags": ["ERP-Software", "Cloud", "B2B"]},
    {"symbol": "ORCL", "name": "Oracle", "logoUrl": "https://logo.clearbit.com/oracle.com", "tags": ["Datenbanken", "Cloud", "Infrastruktur"]},
    {"symbol": "AVGO", "name": "Broadcom", "logoUrl": "https://logo.clearbit.com/broadcom.com", "tags": ["Chips", "Netzwerk", "Software"]},
    {"symbol": "ASML", "name": "ASML", "logoUrl": "https://logo.clearbit.com/asml.com", "tags": ["Lithographie", "Tech", "Halbleiter"]},
    {"symbol": "GOOGL", "name": "Alphabet", "logoUrl": "https://logo.clearbit.com/google.com", "tags": ["Suche", "Werbung", "KI"]},
    {"symbol": "QCOM", "name": "Qualcomm", "logoUrl": "https://logo.clearbit.com/qualcomm.com", "tags": ["Mobilfunk", "Prozessoren", "5G"]},
    {"symbol": "NOW", "name": "ServiceNow", "logoUrl": "https://logo.clearbit.com/servicenow.com", "tags": ["Workflow", "Cloud", "SaaS"]},
    {"symbol": "INTU", "name": "Intuit", "logoUrl": "https://logo.clearbit.com/intuit.com", "tags": ["Finanzsoftware", "Steuern", "KMU"]},
    {"symbol": "JPM", "name": "JPMorgan Chase", "logoUrl": "https://logo.clearbit.com/jpmorganchase.com", "tags": ["Großbank", "Finanzen", "Investment"]},
    {"symbol": "HSBA.L", "name": "HSBC", "logoUrl": "https://logo.clearbit.com/hsbc.com", "tags": ["Banken", "Asien-Fokus", "Vermögen"]},
    {"symbol": "SAN.PA", "name": "Sanofi", "logoUrl": "https://logo.clearbit.com/sanofi.com", "tags": ["Pharma", "Impfstoffe", "Gesundheit"]},
    {"symbol": "BLK", "name": "BlackRock", "logoUrl": "https://logo.clearbit.com/blackrock.com", "tags": ["iShares", "Asset Management", "Finanzen"]},
    {"symbol": "ALV.DE", "name": "Allianz", "logoUrl": "https://logo.clearbit.com/allianz.com", "tags": ["Versicherung", "Vorsorge", "Finanzen"]},
    {"symbol": "MUV2.DE", "name": "Munich Re", "logoUrl": "https://logo.clearbit.com/munichre.com", "tags": ["Rückversicherung", "Risiko", "Finanzen"]},
    {"symbol": "SIE.DE", "name": "Siemens", "logoUrl": "https://logo.clearbit.com/siemens.com", "tags": ["Industrie", "Digitalisierung", "Infrastruktur"]},
    {"symbol": "SU.PA", "name": "Schneider Electric", "logoUrl": "https://logo.clearbit.com/se.com", "tags": ["Energiemanagement", "Automatisierung", "Tech"]},
    {"symbol": "HON", "name": "Honeywell", "logoUrl": "https://logo.clearbit.com/honeywell.com", "tags": ["Mischkonzern", "Luftfahrt", "Industrie"]},
    {"symbol": "CAT", "name": "Caterpillar", "logoUrl": "https://logo.clearbit.com/caterpillar.com", "tags": ["Baumaschinen", "Bergbau", "Schwerindustrie"]},
    {"symbol": "DE", "name": "John Deere", "logoUrl": "https://logo.clearbit.com/deere.com", "tags": ["Agrartechnik", "Forstwirtschaft", "Maschinen"]},
    {"symbol": "ABBN.SW", "name": "ABB", "logoUrl": "https://logo.clearbit.com/abb.com", "tags": ["Robotik", "Automation", "Stromnetz"]},
    {"symbol": "6861.T", "name": "Keyence", "logoUrl": "https://logo.clearbit.com/keyence.com", "tags": ["Sensoren", "Mikroskope", "Automation"]},
    {"symbol": "DG.PA", "name": "Vinci", "logoUrl": "https://logo.clearbit.com/vinci.com", "tags": ["Konzessionen", "Bau", "Infrastruktur"]},
    {"symbol": "PH", "name": "Parker-Hannifin", "logoUrl": "https://logo.clearbit.com/parker.com", "tags": ["Antriebstechnik", "Luftfahrt", "Maschinenbau"]},
    {"symbol": "RIO", "name": "Rio Tinto", "logoUrl": "https://logo.clearbit.com/riotinto.com", "tags": ["Bergbau", "Eisenerz", "Rohstoffe"]},
    {"symbol": "LIN", "name": "Linde", "logoUrl": "https://logo.clearbit.com/linde.com", "tags": ["Gase", "Industrie", "Wasserstoff"]},
    {"symbol": "AI.PA", "name": "Air Liquide", "logoUrl": "https://logo.clearbit.com/airliquide.com", "tags": ["Industriegase", "Medizin", "Tech"]},
    {"symbol": "MC.PA", "name": "LVMH", "logoUrl": "https://logo.clearbit.com/lvmh.com", "tags": ["Luxusgüter", "Mode", "Champagner"]},
    {"symbol": "TTE", "name": "TotalEnergies", "logoUrl": "https://logo.clearbit.com/totalenergies.com", "tags": ["Öl & Gas", "Solar", "Energie"]},
    {"symbol": "NEE", "name": "NextEra Energy", "logoUrl": "https://logo.clearbit.com/nexteraenergy.com", "tags": ["Grüne Energie", "Versorger", "Windkraft"]},
    {"symbol": "ORSTED.CO", "name": "Ørsted", "logoUrl": "https://logo.clearbit.com/orsted.com", "tags": ["Offshore-Wind", "Energie", "Nachhaltig"]},
    {"symbol": "VIE.PA", "name": "Veolia", "logoUrl": "https://logo.clearbit.com/veolia.com", "tags": ["Wasser", "Recycling", "Versorger"]},
    {"symbol": "IBE.MC", "name": "Iberdrola", "logoUrl": "https://logo.clearbit.com/iberdrola.com", "tags": ["Stromversorger", "Erneuerbare", "Netze"]},
    {"symbol": "LLY", "name": "Eli Lilly", "logoUrl": "https://logo.clearbit.com/lilly.com", "tags": ["Pharma", "Adipositas", "Biotech"]},
    {"symbol": "ROG.SW", "name": "Roche", "logoUrl": "https://logo.clearbit.com/roche.com", "tags": ["Pharma", "Diagnostik", "Krebsmedizin"]},
    {"symbol": "NOVN.SW", "name": "Novartis", "logoUrl": "https://logo.clearbit.com/novartis.com", "tags": ["Generika", "Pharma", "Forschung"]},
    {"symbol": "ABBV", "name": "AbbVie", "logoUrl": "https://logo.clearbit.com/abbvie.com", "tags": ["Biopharmaka", "Immunologie", "Pharma"]},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "logoUrl": "https://logo.clearbit.com/jnj.com", "tags": ["Medizintechnik", "Pharma", "Gesundheit"]},
    {"symbol": "AMZN", "name": "Amazon", "logoUrl": "https://logo.clearbit.com/amazon.com", "tags": ["E-Commerce", "AWS-Cloud", "Logistik"]},
    {"symbol": "PG", "name": "Procter & Gamble", "logoUrl": "https://logo.clearbit.com/pg.com", "tags": ["Konsumgüter", "Hygiene", "Marken"]},
    {"symbol": "NESN.SW", "name": "Nestlé", "logoUrl": "https://logo.clearbit.com/nestle.com", "tags": ["Lebensmittel", "Kaffee", "Tiernahrung"]},
    {"symbol": "MDLZ", "name": "Mondelez", "logoUrl": "https://logo.clearbit.com/mondelezinternational.com", "tags": ["Snacks", "Schokolade", "Kekse"]},
    {"symbol": "KO", "name": "Coca-Cola", "logoUrl": "https://logo.clearbit.com/coca-colacompany.com", "tags": ["Erfrischungsgetränke", "Marken", "Global"]},
    {"symbol": "MCD", "name": "McDonald's", "logoUrl": "https://logo.clearbit.com/mcdonalds.com", "tags": ["Fast-Food", "Franchise", "Immobilien"]},
    {"symbol": "WMT", "name": "Walmart", "logoUrl": "https://logo.clearbit.com/walmart.com", "tags": ["Einzelhandel", "Supermärkte", "USA"]},
    {"symbol": "FPE3.DE", "name": "Fuchs SE", "logoUrl": "https://logo.clearbit.com/fuchs.com", "tags": ["Schmierstoffe", "Chemie", "Spezialöle"]},
    {"symbol": "PLD", "name": "Prologis", "logoUrl": "https://logo.clearbit.com/prologis.com", "tags": ["Logistik-Immobilien", "REIT", "Lager"]},
    {"symbol": "KRN.DE", "name": "Krones", "logoUrl": "https://logo.clearbit.com/krones.com", "tags": ["Verpackungsmaschinen", "Abfüllung", "Industrie"]},
    {"symbol": "MMK.VI", "name": "Mayr-Melnhof Karton", "logoUrl": "https://logo.clearbit.com/mm-karton.com", "tags": ["Karton", "Verpackung", "Recycling"]},
    {"symbol": "IBN", "name": "ICICI Bank", "logoUrl": "https://logo.clearbit.com/icicibank.com", "tags": ["Banken", "Indien", "Finanzdienstleistung"]}
]

# Aktuelle Wechselkurse in Euro laden (Alternative Datenstruktur-Verbindung)
print("Lade Wechselkurse für EUR-Umrechnung...")
fx_rates = {"USD": 1.0, "EUR": 1.0, "CHF": 1.0, "GBP": 1.0, "DKK": 1.0, "JPY": 1.0}
for curr in ["USD", "CHF", "GBP", "DKK", "JPY"]:
    try:
        pair = f"EUR{curr}=X" if curr != "GBP" else "GBPEUR=X"
        t = yf.Ticker(pair)
        px = t.history(period="1d")['Close'].iloc[-1]
        if curr == "GBP":
            fx_rates["GBP"] = 1.0 / px # Britische Pence Korrektur erfolgt im Loop
        else:
            fx_rates[curr] = px
    except:
        print(f"Nutze Standardkurs für {curr}")

aktien_daten = []

for aktie in meine_aktien:
    try:
        ticker = yf.Ticker(aktie["symbol"])
        hist_5y = ticker.history(period="5y")
        hist_1m = ticker.history(period="1mo")
        info = ticker.info
        
        if not hist_5y.empty and not hist_1m.empty:
            raw_kurs = hist_5y['Close'].iloc[-1]
            
            # Währungs-Erkennung & automatische Umrechnung in Euro
            sym = aktie["symbol"]
            rate = 1.0
            if ".DE" in sym or ".PA" in sym or ".MC" in sym or ".VI" in sym:
                rate = fx_rates["EUR"]
            elif ".SW" in sym:
                rate = fx_rates["CHF"]
            elif ".L" in sym:
                rate = fx_rates["GBP"] * 100 # GBp sind Pence
            elif ".CO" in sym:
                rate = fx_rates["DKK"]
            elif ".T" in sym:
                rate = fx_rates["JPY"]
            else:
                rate = fx_rates["USD"] # Standard US-Märkte
                
            kurs_eur = raw_kurs / rate
            
            # Performance Berechnungen (Sichere Variante für GitHub)
            kurs_1m = hist_1m['Close'].iloc[0] if len(hist_1m) > 0 else raw_kurs
            
            # Falls weniger als 1 oder 5 Jahre Historie existieren, Failsafe aktivieren
            idx_1y = -252 if len(hist_5y) >= 252 else 0
            idx_5y = 0
            
            kurs_1y = hist_5y['Close'].iloc[idx_1y]
            kurs_5y = hist_5y['Close'].iloc[idx_5y]
            
            perf_m = ((raw_kurs - kurs_1m) / kurs_1m) * 100
            perf_j = ((raw_kurs - kurs_1y) / kurs_1y) * 100
            perf_5j = ((raw_kurs - kurs_5y) / kurs_5y) * 100

            # Robuste Selektion für 1 Jahr / 5 Jahre
            idx_1y = -252 if len(hist_5y) >= 252 else 0
            idx_5y = 0
            
            perf_m = ((raw_kurs - kurs_1m) / kurs_1m) * 100
            perf_j = ((raw_kurs - hist_5y['Close'].iloc[idx_1y]) / hist_5y['Close'].iloc[idx_1y]) * 100
            perf_5j = ((raw_kurs - hist_5y['Close'].iloc[idx_5y]) / hist_5y['Close'].iloc[idx_5y]) * 100
            
            # Dividendenrendite & KGV über Fallback-Struktur ziehen
            div_yield = (info.get("dividendYield", 0) or 0) * 100
            kgv = info.get("trailingPE") or info.get("forwardPE") or 0
            
            aktien_daten.append({
                "name": aktie["name"],
                "logoUrl": aktie["logoUrl"],
                "tags": aktie["tags"],
                "kurs": f"{kurs_eur:.2f} €",
                "perfMonat": perf_m,
                "perfJahr": perf_j,
                "perf5J": perf_5j,
                "yield": div_yield,
                "kgv": kgv
            })
            print(f"Erfolg: {aktie['name']} -> {kurs_eur:.2f} € | KGV: {kgv}")
    except Exception as e:
        print(f"Fehler bei {aktie['name']}: {e}", file=sys.stderr)

with open("daten.json", "w", encoding="utf-8") as f:
    json.dump(aktien_daten, f, ensure_ascii=False, indent=4)
