import yfinance as yf
import json
import sys

# Vollständige Liste: 51 Depot-Aktien (watchlist: False) + 33 Watchlist-Aktien (watchlist: True)
meine_aktien = [
    # --- DEPOT AKTIEN ---
    {"symbol": "MSFT", "name": "Microsoft", "logoUrl": "https://logo.clearbit.com/microsoft.com", "tags": ["Software", "Cloud", "KI"], "watchlist": False},
    {"symbol": "TSM", "name": "TSMC", "logoUrl": "https://logo.clearbit.com/tsmc.com", "tags": ["Halbleiter", "Chips", "Tech"], "watchlist": False},
    {"symbol": "SAP.DE", "name": "SAP", "logoUrl": "https://logo.clearbit.com/sap.com", "tags": ["ERP-Software", "Cloud", "B2B"], "watchlist": False},
    {"symbol": "ORCL", "name": "Oracle", "logoUrl": "https://logo.clearbit.com/oracle.com", "tags": ["Datenbanken", "Cloud", "Infrastruktur"], "watchlist": False},
    {"symbol": "AVGO", "name": "Broadcom", "logoUrl": "https://logo.clearbit.com/broadcom.com", "tags": ["Chips", "Netzwerk", "Software"], "watchlist": False},
    {"symbol": "ASML", "name": "ASML", "logoUrl": "https://logo.clearbit.com/asml.com", "tags": ["Lithographie", "Tech", "Halbleiter"], "watchlist": False},
    {"symbol": "GOOGL", "name": "Alphabet", "logoUrl": "https://logo.clearbit.com/google.com", "tags": ["Suche", "Werbung", "KI"], "watchlist": False},
    {"symbol": "QCOM", "name": "Qualcomm", "logoUrl": "https://logo.clearbit.com/qualcomm.com", "tags": ["Mobilfunk", "Prozessoren", "5G"], "watchlist": False},
    {"symbol": "NOW", "name": "ServiceNow", "logoUrl": "https://logo.clearbit.com/servicenow.com", "tags": ["Workflow", "Cloud", "SaaS"], "watchlist": False},
    {"symbol": "INTU", "name": "Intuit", "logoUrl": "https://logo.clearbit.com/intuit.com", "tags": ["Finanzsoftware", "Steuern", "KMU"], "watchlist": False},
    {"symbol": "JPM", "name": "JPMorgan Chase", "logoUrl": "https://logo.clearbit.com/jpmorganchase.com", "tags": ["Großbank", "Finanzen", "Investment"], "watchlist": False},
    {"symbol": "HSBA.L", "name": "HSBC", "logoUrl": "https://logo.clearbit.com/hsbc.com", "tags": ["Banken", "Asien-Fokus", "Vermögen"], "watchlist": False},
    {"symbol": "SAN.PA", "name": "Sanofi", "logoUrl": "https://logo.clearbit.com/sanofi.com", "tags": ["Pharma", "Impfstoffe", "Gesundheit"], "watchlist": False},
    {"symbol": "BLK", "name": "BlackRock", "logoUrl": "https://logo.clearbit.com/blackrock.com", "tags": ["iShares", "Asset Management", "Finanzen"], "watchlist": False},
    {"symbol": "ALV.DE", "name": "Allianz", "logoUrl": "https://logo.clearbit.com/allianz.com", "tags": ["Versicherung", "Vorsorge", "Finanzen"], "watchlist": False},
    {"symbol": "MUV2.DE", "name": "Munich Re", "logoUrl": "https://logo.clearbit.com/munichre.com", "tags": ["Rückversicherung", "Risiko", "Finanzen"], "watchlist": False},
    {"symbol": "SIE.DE", "name": "Siemens", "logoUrl": "https://logo.clearbit.com/siemens.com", "tags": ["Industrie", "Digitalisierung", "Infrastruktur"], "watchlist": False},
    {"symbol": "SU.PA", "name": "Schneider Electric", "logoUrl": "https://logo.clearbit.com/se.com", "tags": ["Energiemanagement", "Automatisierung", "Tech"], "watchlist": False},
    {"symbol": "HON", "name": "Honeywell", "logoUrl": "https://logo.clearbit.com/honeywell.com", "tags": ["Mischkonzern", "Luftfahrt", "Industrie"], "watchlist": False},
    {"symbol": "CAT", "name": "Caterpillar", "logoUrl": "https://logo.clearbit.com/caterpillar.com", "tags": ["Baumaschinen", "Bergbau", "Schwerindustrie"], "watchlist": False},
    {"symbol": "DE", "name": "John Deere", "logoUrl": "https://logo.clearbit.com/deere.com", "tags": ["Agrartechnik", "Forstwirtschaft", "Maschinen"], "watchlist": False},
    {"symbol": "ABBN.SW", "name": "ABB", "logoUrl": "https://logo.clearbit.com/abb.com", "tags": ["Robotik", "Automation", "Stromnetz"], "watchlist": False},
    {"symbol": "6861.T", "name": "Keyence", "logoUrl": "https://logo.clearbit.com/keyence.com", "tags": ["Sensoren", "Mikroskope", "Automation"], "watchlist": False},
    {"symbol": "DG.PA", "name": "Vinci", "logoUrl": "https://logo.clearbit.com/vinci.com", "tags": ["Konzessionen", "Bau", "Infrastruktur"], "watchlist": False},
    {"symbol": "PH", "name": "Parker-Hannifin", "logoUrl": "https://logo.clearbit.com/parker.com", "tags": ["Antriebstechnik", "Luftfahrt", "Maschinenbau"], "watchlist": False},
    {"symbol": "RIO", "name": "Rio Tinto", "logoUrl": "https://logo.clearbit.com/riotinto.com", "tags": ["Bergbau", "Eisenerz", "Rohstoffe"], "watchlist": False},
    {"symbol": "LIN", "name": "Linde", "logoUrl": "https://logo.clearbit.com/linde.com", "tags": ["Gase", "Industrie", "Wasserstoff"], "watchlist": False},
    {"symbol": "AI.PA", "name": "Air Liquide", "logoUrl": "https://logo.clearbit.com/airliquide.com", "tags": ["Industriegase", "Medizin", "Tech"], "watchlist": False},
    {"symbol": "MC.PA", "name": "LVMH", "logoUrl": "https://logo.clearbit.com/lvmh.com", "tags": ["Luxusgüter", "Mode", "Champagner"], "watchlist": False},
    {"symbol": "TTE", "name": "TotalEnergies", "logoUrl": "https://logo.clearbit.com/totalenergies.com", "tags": ["Öl & Gas", "Solar", "Energie"], "watchlist": False},
    {"symbol": "NEE", "name": "NextEra Energy", "logoUrl": "https://logo.clearbit.com/nexteraenergy.com", "tags": ["Grüne Energie", "Versorger", "Windkraft"], "watchlist": False},
    {"symbol": "ORSTED.CO", "name": "Ørsted", "logoUrl": "https://logo.clearbit.com/orsted.com", "tags": ["Offshore-Wind", "Energie", "Nachhaltig"], "watchlist": False},
    {"symbol": "VIE.PA", "name": "Veolia", "logoUrl": "https://logo.clearbit.com/veolia.com", "tags": ["Wasser", "Recycling", "Versorger"], "watchlist": False},
    {"symbol": "IBE.MC", "name": "Iberdrola", "logoUrl": "https://logo.clearbit.com/iberdrola.com", "tags": ["Stromversorger", "Erneuerbare", "Netze"], "watchlist": False},
    {"symbol": "LLY", "name": "Eli Lilly", "logoUrl": "https://logo.clearbit.com/lilly.com", "tags": ["Pharma", "Adipositas", "Biotech"], "watchlist": False},
    {"symbol": "ROG.SW", "name": "Roche", "logoUrl": "https://logo.clearbit.com/roche.com", "tags": ["Pharma", "Diagnostik", "Krebsmedizin"], "watchlist": False},
    {"symbol": "NOVN.SW", "name": "Novartis", "logoUrl": "https://logo.clearbit.com/novartis.com", "tags": ["Generika", "Pharma", "Forschung"], "watchlist": False},
    {"symbol": "ABBV", "name": "AbbVie", "logoUrl": "https://logo.clearbit.com/abbvie.com", "tags": ["Biopharmaka", "Immunologie", "Pharma"], "watchlist": False},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "logoUrl": "https://logo.clearbit.com/jnj.com", "tags": ["Medizintechnik", "Pharma", "Gesundheit"], "watchlist": False},
    {"symbol": "AMZN", "name": "Amazon", "logoUrl": "https://logo.clearbit.com/amazon.com", "tags": ["E-Commerce", "AWS-Cloud", "Logistik"], "watchlist": False},
    {"symbol": "PG", "name": "Procter & Gamble", "logoUrl": "https://logo.clearbit.com/pg.com", "tags": ["Konsumgüter", "Hygiene", "Marken"], "watchlist": False},
    {"symbol": "NESN.SW", "name": "Nestlé", "logoUrl": "https://logo.clearbit.com/nestle.com", "tags": ["Lebensmittel", "Kaffee", "Tiernahrung"], "watchlist": False},
    {"symbol": "MDLZ", "name": "Mondelez", "logoUrl": "https://logo.clearbit.com/mondelezinternational.com", "tags": ["Snacks", "Schokolade", "Kekse"], "watchlist": False},
    {"symbol": "KO", "name": "Coca-Cola", "logoUrl": "https://logo.clearbit.com/coca-colacompany.com", "tags": ["Erfrischungsgetränke", "Marken", "Global"], "watchlist": False},
    {"symbol": "MCD", "name": "McDonald's", "logoUrl": "https://logo.clearbit.com/mcdonalds.com", "tags": ["Fast-Food", "Franchise", "Immobilien"], "watchlist": False},
    {"symbol": "WMT", "name": "Walmart", "logoUrl": "https://logo.clearbit.com/walmart.com", "tags": ["Einzelhandel", "Supermärkte", "USA"], "watchlist": False},
    {"symbol": "FPE3.DE", "name": "Fuchs SE", "logoUrl": "https://logo.clearbit.com/fuchs.com", "tags": ["Schmierstoffe", "Chemie", "Spezialöle"], "watchlist": False},
    {"symbol": "PLD", "name": "Prologis", "logoUrl": "https://logo.clearbit.com/prologis.com", "tags": ["Logistik-Immobilien", "REIT", "Lager"], "watchlist": False},
    {"symbol": "KRN.DE", "name": "Krones", "logoUrl": "https://logo.clearbit.com/krones.com", "tags": ["Verpackungsmaschinen", "Abfüllung", "Industrie"], "watchlist": False},
    {"symbol": "MMK.VI", "name": "Mayr-Melnhof Karton", "logoUrl": "https://logo.clearbit.com/mm-karton.com", "tags": ["Karton", "Verpackung", "Recycling"], "watchlist": False},
    {"symbol": "IBN", "name": "ICICI Bank", "logoUrl": "https://logo.clearbit.com/icicibank.com", "tags": ["Banken", "Indien", "Finanzdienstleistung"], "watchlist": False},

    # --- WATCHLIST AKTIEN ---
    {"symbol": "1398.HK", "name": "Industrial & Commercial Bank of China", "logoUrl": "https://logo.clearbit.com/icbc.com.cn", "tags": ["Banken", "China", "Staatskonzern"], "watchlist": True},
    {"symbol": "TPE.WA", "name": "Tauron Polska Energia", "logoUrl": "https://logo.clearbit.com/tauron.pl", "tags": ["Energie", "Versorger", "Polen"], "watchlist": True},
    {"symbol": "DNP.WA", "name": "Dino Polska", "logoUrl": "https://logo.clearbit.com/grupadino.pl", "tags": ["Supermärkte", "Einzelhandel", "Polen"], "watchlist": True},
    {"symbol": "LHA.DE", "name": "Deutsche Lufthansa", "logoUrl": "https://logo.clearbit.com/lufthansagroup.com", "tags": ["Airlines", "Luftfahrt", "Logistik"], "watchlist": True},
    {"symbol": "FIH-U.TO", "name": "Fairfax India", "logoUrl": "https://logo.clearbit.com/fairfaxindia.ca", "tags": ["Beteiligungen", "Indien", "Investment"], "watchlist": True},
    {"symbol": "EOAN.DE", "name": "E.ON", "logoUrl": "https://logo.clearbit.com/eon.com", "tags": ["Energienetze", "Infrastruktur", "Versorger"], "watchlist": True},
    {"symbol": "CMCSA", "name": "Comcast A", "logoUrl": "https://logo.clearbit.com/comcastcorporation.com", "tags": ["Medien", "Kabelnetz", "Streaming"], "watchlist": True},
    {"symbol": "KHC", "name": "Kraft Heinz", "logoUrl": "https://logo.clearbit.com/kraftheinzcompany.com", "tags": ["Lebensmittel", "Ketchup", "Marken"], "watchlist": True},
    {"symbol": "VNA.DE", "name": "Vonovia", "logoUrl": "https://logo.clearbit.com/vonovia.de", "tags": ["Immobilien", "Wohnungen", "Vermieter"], "watchlist": True},
    {"symbol": "PKO.WA", "name": "Powszechna Kasa Oszczednosci Bank", "logoUrl": "https://logo.clearbit.com/pkobp.pl", "tags": ["Banken", "Polen", "Finanzen"], "watchlist": True},
    {"symbol": "DNB.OL", "name": "DNB Bank", "logoUrl": "https://logo.clearbit.com/dnb.no", "tags": ["Banken", "Norwegen", "Finanzservice"], "watchlist": True},
    {"symbol": "6506.T", "name": "Yaskawa Electric", "logoUrl": "https://logo.clearbit.com/yaskawa-global.com", "tags": ["Robotik", "Motoren", "Automation"], "watchlist": True},
    {"symbol": "6954.T", "name": "Fanuc", "logoUrl": "https://logo.clearbit.com/fanuc.co.jp", "tags": ["CNC-Systeme", "Roboter", "Fabrikautomation"], "watchlist": True},
    {"symbol": "YAR.OL", "name": "Yara Intl.", "logoUrl": "https://logo.clearbit.com/yara.com", "tags": ["Düngemittel", "Agrar-Chemie", "Ernte"], "watchlist": True},
    {"symbol": "VZ", "name": "Verizon", "logoUrl": "https://logo.clearbit.com/verizon.com", "tags": ["Telekom", "Mobilfunk", "5G"], "watchlist": True},
    {"symbol": "DHL.DE", "name": "DHL", "logoUrl": "https://logo.clearbit.com/dhl.com", "tags": ["Logistik", "Pakete", "Post"], "watchlist": True},
    {"symbol": "EVD.DE", "name": "CTS Eventim", "logoUrl": "https://logo.clearbit.com/eventim.de", "tags": ["Ticketing", "Konzerte", "Live-Events"], "watchlist": True},
    {"symbol": "VER.VI", "name": "Verbund AG", "logoUrl": "https://logo.clearbit.com/verbund.com", "tags": ["Wasserkraft", "Strom", "Österreich"], "watchlist": True},
    {"symbol": "CGNX", "name": "Cognex", "logoUrl": "https://logo.clearbit.com/cognex.com", "tags": ["Bildverarbeitung", "Sensoren", "Tech"], "watchlist": True},
    {"symbol": "EUK3.DE", "name": "EUROKAI Vz.", "logoUrl": "https://logo.clearbit.com/eurokai.de", "tags": ["Hafenterminals", "Logistik", "Schifffahrt"], "watchlist": True},
    {"symbol": "BMW3.DE", "name": "BMW Vz.", "logoUrl": "https://logo.clearbit.com/bmwgroup.com", "tags": ["Automobile", "Premium", "Motorrad"], "watchlist": True},
    {"symbol": "PDD", "name": "Pinduoduo ADR", "logoUrl": "https://logo.clearbit.com/pddholdings.com", "tags": ["E-Commerce", "Temu", "China"], "watchlist": True},
    {"symbol": "BEI.DE", "name": "Beiersdorf", "logoUrl": "https://logo.clearbit.com/beiersdorf.de", "tags": ["Nivea", "Hautpflege", "Konsumgüter"], "watchlist": True},
    {"symbol": "SIX2.DE", "name": "Sixt St.", "logoUrl": "https://logo.clearbit.com/sixt.de", "tags": ["Autovermietung", "Mobilität", "Leasing"], "watchlist": True},
    {"symbol": "ABBN.SW", "name": "ABB (Watchlist)", "logoUrl": "https://logo.clearbit.com/abb.com", "tags": ["Elektrotechnik", "Automation", "Tech"], "watchlist": True},
    {"symbol": "STR.VI", "name": "Strabag", "logoUrl": "https://logo.clearbit.com/strabag.com", "tags": ["Baukonzern", "Infrastruktur", "Tiefbau"], "watchlist": True},
    {"symbol": "FRM.DE", "name": "FRoSTA", "logoUrl": "https://logo.clearbit.com/frosta-ag.de", "tags": ["Tiefkühlkost", "Ernährung", "Lebensmittel"], "watchlist": True},
    {"symbol": "6367.T", "name": "Daikin Industries", "logoUrl": "https://logo.clearbit.com/daikin.com", "tags": ["Klimaanlagen", "Wärmepumpen", "Heizung"], "watchlist": True},
    {"symbol": "ADSK", "name": "Autodesk", "logoUrl": "https://logo.clearbit.com/autodesk.com", "tags": ["CAD-Software", "3D-Design", "Architektur"], "watchlist": True},
    {"symbol": "ADBE", "name": "Adobe", "logoUrl": "https://logo.clearbit.com/adobe.com", "tags": ["Photoshop", "Kreativ-Cloud", "Software"], "watchlist": True},
    {"symbol": "SIKA.SW", "name": "Sika", "logoUrl": "https://logo.clearbit.com/sika.com", "tags": ["Spezialchemie", "Baustoffe", "Klebstoffe"], "watchlist": True},
    {"symbol": "TER", "name": "Teradyne", "logoUrl": "https://logo.clearbit.com/teradyne.com", "tags": ["Testsysteme", "Halbleiter", "Automatisierung"], "watchlist": True},
    {"symbol": "ROK", "name": "Rockwell Automation", "logoUrl": "https://logo.clearbit.com/rockwellautomation.com", "tags": ["Fabrikautomation", "Industriesoftware", "Tech"], "watchlist": True}
]

print("Lade Wechselkurse für weltweite EUR-Umrechnung...")
fx_rates = {"USD": 1.0, "EUR": 1.0, "CHF": 1.0, "GBP": 1.0, "DKK": 1.0, "JPY": 1.0, "HKD": 1.0, "PLN": 1.0, "CAD": 1.0, "NOK": 1.0}
for curr in ["USD", "CHF", "GBP", "DKK", "JPY", "HKD", "PLN", "CAD", "NOK"]:
    try:
        pair = f"EUR{curr}=X" if curr != "GBP" else "GBPEUR=X"
        t = yf.Ticker(pair)
        px = t.history(period="1d")['Close'].iloc[-1]
        if curr == "GBP":
            fx_rates["GBP"] = 1.0 / px
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
            
            sym = aktie["symbol"]
            rate = 1.0
            if ".DE" in sym or ".PA" in sym or ".MC" in sym or ".VI" in sym:
                rate = fx_rates["EUR"]
            elif ".SW" in sym:
                rate = fx_rates["CHF"]
            elif ".L" in sym:
                rate = fx_rates["GBP"] * 100
            elif ".CO" in sym:
                rate = fx_rates["DKK"]
            elif ".T" in sym:
                rate = fx_rates["JPY"]
            elif ".HK" in sym:
                rate = fx_rates["HKD"]
            elif ".WA" in sym:
                rate = fx_rates["PLN"]
            elif ".TO" in sym:
                rate = fx_rates["CAD"]
            elif ".OL" in sym:
                rate = fx_rates["NOK"]
            else:
                rate = fx_rates["USD"]
                
            kurs_eur = raw_kurs / rate
            
            kurs_1m = hist_1m['Close'].iloc[0] if len(hist_1m) > 0 else raw_kurs
            idx_1y = -252 if len(hist_5y) >= 252 else 0
            idx_5y = 0
            
            kurs_1y = hist_5y['Close'].iloc[idx_1y]
            kurs_5y = hist_5y['Close'].iloc[idx_5y]
            
            perf_m = ((raw_kurs - kurs_1m) / kurs_1m) * 100
            perf_j = ((raw_kurs - kurs_1y) / kurs_1y) * 100
            perf_5j = ((raw_kurs - kurs_5y) / kurs_5y) * 100
            
            raw_yield = info.get("dividendYield", 0) or 0
            div_yield = raw_yield * 100 if 0 < raw_yield < 1.0 else raw_yield
                
            kgv = info.get("trailingPE") or info.get("forwardPE") or 0
            
            aktien_daten.append({
                "name": aktie["name"],
                "logoUrl": aktie["logoUrl"],
                "tags": aktie["tags"],
                "watchlist": aktie["watchlist"],
                "kurs": f"{kurs_eur:.2f} €",
                "perfMonat": perf_m,
                "perfJahr": perf_j,
                "perf5J": perf_5j,
                "yield": div_yield,
                "kgv": kgv
            })
            print(f"Erfolg: {aktie['name']} -> {kurs_eur:.2f} €")
    except Exception as e:
        print(f"Fehler bei {aktie['name']}: {e}", file=sys.stderr)

with open("daten.json", "w", encoding="utf-8") as f:
    json.dump(aktien_daten, f, ensure_ascii=False, indent=4)
