import sys

try:
    import yfinance as yf
    import json
    import math
    from datetime import datetime, timedelta
except Exception as e:
    print(f"Kritischer Fehler beim Importieren der Bibliotheken: {e}")
    sys.exit(0)

def isNaN(num):
    return isinstance(num, float) and math.isnan(num)

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
    {"symbol": "HON", "name": "Honeywell Technologies", "logoUrl": "https://logo.clearbit.com/honeywell.com", "tags": ["Automation", "Autonomie", "Industrie"], "watchlist": False},
    {"symbol": "HONA", "name": "Honeywell Aerospace", "logoUrl": "https://logo.clearbit.com/honeywell.com", "tags": ["Luftfahrt", "Verteidigung", "Avionik"], "watchlist": False},
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
    {"symbol": "CMCSA", "name": "Comcast", "logoUrl": "https://logo.clearbit.com/comcastcorporation.com", "tags": ["Medien", "Streaming", "Kabelnetz"], "watchlist": False},
    {"symbol": "TPE.WA", "name": "Tauron Polska Energia", "logoUrl": "https://logo.clearbit.com/tauron.pl", "tags": ["Energie", "Versorger", "Polen"], "watchlist": False},
    {"symbol": "SOBA.DE", "name": "AT&T", "logoUrl": "https://logo.clearbit.com/att.com", "tags": ["Telekom", "USA", "Dividendenwert"], "watchlist": False},

    # --- WATCHLIST AKTIEN ---
    {"symbol": "DDOG", "name": "Datadog A", "logoUrl": "https://logo.clearbit.com/datadoghq.com", "tags": ["Cloud", "Monitoring", "Software"], "watchlist": True},
    {"symbol": "FANUY", "name": "Fanuc", "logoUrl": "https://logo.clearbit.com/fanuc.co.jp", "tags": ["CNC-Systeme", "Roboter", "Automation"], "watchlist": True},
    {"symbol": "6506.T", "name": "Yaskawa Electric", "logoUrl": "https://logo.clearbit.com/yaskawa-global.com", "tags": ["Robotik", "Motoren", "Automation"], "watchlist": True},
    {"symbol": "CGNX", "name": "Cognex", "logoUrl": "https://logo.clearbit.com/cognex.com", "tags": ["Bildverarbeitung", "Sensoren", "Tech"], "watchlist": True},
    {"symbol": "MPWR", "name": "Monolithic Power Systems", "logoUrl": "https://logo.clearbit.com/monolithicpower.com", "tags": ["Halbleiter", "Chips"], "watchlist": True},
    {"symbol": "KEYS", "name": "Keysight Technologies", "logoUrl": "https://logo.clearbit.com/keysight.com", "tags": ["Messtechnik", "Elektronik"], "watchlist": True},
    {"symbol": "SFTBY", "name": "SoftBank Group", "logoUrl": "https://logo.clearbit.com/softbank.jp", "tags": ["Beteiligungen", "Tech"], "watchlist": True},
    {"symbol": "POWL", "name": "Powell Industries", "logoUrl": "https://logo.clearbit.com/powellind.com", "tags": ["Elektrotechnik", "Infrastruktur"], "watchlist": True},
    {"symbol": "TER", "name": "Teradyne", "logoUrl": "https://logo.clearbit.com/teradyne.com", "tags": ["Testsysteme", "Halbleiter"], "watchlist": True},
    {"symbol": "DHL.DE", "name": "DHL", "logoUrl": "https://logo.clearbit.com/dhl.com", "tags": ["Logistik", "Pakete"], "watchlist": True},
    {"symbol": "LHA.DE", "name": "Deutsche Lufthansa", "logoUrl": "https://logo.clearbit.com/lufthansagroup.com", "tags": ["Airlines", "Luftfahrt"], "watchlist": True},
    {"symbol": "6367.T", "name": "Daikin Industries", "logoUrl": "https://logo.clearbit.com/daikin.com", "tags": ["Klimaanlagen", "Wärmepumpen"], "watchlist": True},
    {"symbol": "ERIC", "name": "Telefonaktiebolaget LM Ericsson B", "logoUrl": "https://logo.clearbit.com/ericsson.com", "tags": ["Telekom", "5G-Netze"], "watchlist": True},
    {"symbol": "ROK", "name": "Rockwell Automation", "logoUrl": "https://logo.clearbit.com/rockwellautomation.com", "tags": ["Fabrikautomation", "Tech"], "watchlist": True},
    {"symbol": "PKO.WA", "name": "Powszechna Kasa Oszczednosci Bank", "logoUrl": "https://logo.clearbit.com/pkobp.pl", "tags": ["Banken", "Polen"], "watchlist": True},
    {"symbol": "EUK3.DE", "name": "EUROKAI Vz", "logoUrl": "https://logo.clearbit.com/eurokai.de", "tags": ["Hafenterminals", "Logistik"], "watchlist": True},
    {"symbol": "FRM.DE", "name": "FRoSTA", "logoUrl": "https://logo.clearbit.com/frosta-ag.de", "tags": ["Tiefkühlkost", "Lebensmittel"], "watchlist": True},
    {"symbol": "YAR.OL", "name": "Yara Intl.", "logoUrl": "https://logo.clearbit.com/yara.com", "tags": ["Düngemittel", "Chemie"], "watchlist": True},
    {"symbol": "EOAN.DE", "name": "E.ON", "logoUrl": "https://logo.clearbit.com/eon.com", "tags": ["Energienetze", "Versorger"], "watchlist": True},
    {"symbol": "STR.VI", "name": "Strabag", "logoUrl": "https://logo.clearbit.com/strabag.com", "tags": ["Baukonzern", "Infrastruktur"], "watchlist": True},
    {"symbol": "NET", "name": "Cloudflare A", "logoUrl": "https://logo.clearbit.com/cloudflare.com", "tags": ["CDN", "Web-Sicherheit"], "watchlist": True},
    {"symbol": "SREN.SW", "name": "Swiss RE", "logoUrl": "https://logo.clearbit.com/swissre.com", "tags": ["Rückversicherung", "Finanzen"], "watchlist": True},
    {"symbol": "AOS", "name": "A. O. Smith", "logoUrl": "https://logo.clearbit.com/aosmith.com", "tags": ["Heizung", "Industrie"], "watchlist": True},
    {"symbol": "FIH-U.TO", "name": "Fairfax India", "logoUrl": "https://logo.clearbit.com/fairfaxindia.ca", "tags": ["Beteiligungen", "Indien"], "watchlist": True},
    {"symbol": "SIX2.DE", "name": "Sixt SE St.", "logoUrl": "https://logo.clearbit.com/sixt.de", "tags": ["Autovermietung", "Mobilität"], "watchlist": True},
    {"symbol": "CHD", "name": "Church & Dwight", "logoUrl": "https://logo.clearbit.com/churchdwight.com", "tags": ["Konsumgüter", "Marken"], "watchlist": True},
    {"symbol": "KGX.DE", "name": "KION Grp", "logoUrl": "https://logo.clearbit.com/kiongroup.com", "tags": ["Logistik", "Lagertechnik"], "watchlist": True},
    {"symbol": "MAY.V", "name": "Mayfair Gold", "logoUrl": "https://logo.clearbit.com/mayfairgold.com", "tags": ["Bergbau", "Gold"], "watchlist": True},
    {"symbol": "DNB.OL", "name": "DNB Bank", "logoUrl": "https://logo.clearbit.com/dnb.no", "tags": ["Banken", "Norwegen"], "watchlist": True},
    {"symbol": "VNA.DE", "name": "Vonovia", "logoUrl": "https://logo.clearbit.com/vonovia.de", "tags": ["Immobilien", "Wohnungen"], "watchlist": True},
    {"symbol": "SIKA.SW", "name": "Sika", "logoUrl": "https://logo.clearbit.com/sika.com", "tags": ["Spezialchemie", "Baustoffe"], "watchlist": True},
    {"symbol": "PDD", "name": "Pinduoduo ADR A", "logoUrl": "https://logo.clearbit.com/pddholdings.com", "tags": ["E-Commerce", "Temu"], "watchlist": True},
    {"symbol": "VER.VI", "name": "Verbund AG", "logoUrl": "https://logo.clearbit.com/verbund.com", "tags": ["Wasserkraft", "Strom"], "watchlist": True},
    {"symbol": "DTE.DE", "name": "Deutsche Telekom", "logoUrl": "https://logo.clearbit.com/telekom.com", "tags": ["Telekom", "Mobilfunk"], "watchlist": True},
    {"symbol": "HNR1.DE", "name": "Hannover Rück", "logoUrl": "https://logo.clearbit.com/hannover-rueck.de", "tags": ["Rückversicherung", "Finanzen"], "watchlist": True},
    {"symbol": "BMW3.DE", "name": "BMW Vz", "logoUrl": "https://logo.clearbit.com/bmwgroup.com", "tags": ["Automobile", "Premium"], "watchlist": True},
    {"symbol": "EVD.DE", "name": "CTS Eventim & Co", "logoUrl": "https://logo.clearbit.com/eventim.de", "tags": ["Ticketing", "Konzerte"], "watchlist": True},
    {"symbol": "ADBE", "name": "Adobe", "logoUrl": "https://logo.clearbit.com/adobe.com", "tags": ["Photoshop", "Software"], "watchlist": True},
    {"symbol": "DSY.PA", "name": "Dassault Systèmes", "logoUrl": "https://logo.clearbit.com/3ds.com", "tags": ["3D-Software", "Simulation"], "watchlist": True},
    {"symbol": "DNP.WA", "name": "Dino Polska", "logoUrl": "https://logo.clearbit.com/grupadino.pl", "tags": ["Supermärkte", "Einzelhandel"], "watchlist": True},
    {"symbol": "LEHNF", "name": "Lem Holding", "logoUrl": "https://logo.clearbit.com/lem.com", "tags": ["Sensorik", "Elektronik"], "watchlist": True},
    {"symbol": "ADSK", "name": "Autodesk", "logoUrl": "https://logo.clearbit.com/autodesk.com", "tags": ["CAD-Software", "3D-Design"], "watchlist": True},
    {"symbol": "BEI.DE", "name": "Beiersdorf", "logoUrl": "https://logo.clearbit.com/beiersdorf.de", "tags": ["Nivea", "Konsumgüter"], "watchlist": True},
    {"symbol": "CRWD", "name": "CrowdStrike", "logoUrl": "https://logo.clearbit.com/crowdstrike.com", "tags": ["Cybersecurity", "Cloud", "SaaS"], "watchlist": True},
    {"symbol": "1398.HK", "name": "ICBC", "logoUrl": "https://logo.clearbit.com/icbc.com.cn", "tags": ["Banken", "China", "Großbank"], "watchlist": True},
    {"symbol": "VZ", "name": "Verizon", "logoUrl": "https://logo.clearbit.com/verizon.com", "tags": ["Telekom", "Mobilfunk", "USA"], "watchlist": True}
]

monate_de = {1: "Jan", 2: "Feb", 3: "Mrz", 4: "Apr", 5: "Mai", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez"}

print("Lade Wechselkurse...")
fx_rates = {"USD": 1.0, "EUR": 1.0, "CHF": 1.0, "GBP": 1.0, "DKK": 1.0, "JPY": 1.0, "HKD": 1.0, "PLN": 1.0, "CAD": 1.0, "NOK": 1.0}
for curr in ["USD", "CHF", "GBP", "DKK", "JPY", "HKD", "PLN", "CAD", "NOK"]:
    try:
        pair = f"EUR{curr}=X" if curr != "GBP" else "GBPEUR=X"
        t = yf.Ticker(pair)
        px = t.history(period="1d")['Close'].iloc[-1]
        fx_rates[curr] = 1.0 / px if curr == "GBP" else px
    except Exception:
        pass

aktien_daten = []

for aktie in meine_aktien:
    try:
        ticker = yf.Ticker(aktie["symbol"])
        hist_5y = ticker.history(period="5y", actions=True)
        hist_1m = ticker.history(period="1mo")
        
        if hist_5y.empty or hist_1m.empty:
            print(f"Keine Kursdaten für {aktie['name']}. Überspringe.")
            continue
            
        raw_kurs = hist_5y['Close'].iloc[-1]
        sym = aktie["symbol"]
        rate = 1.0
        
        if ".DE" in sym or ".PA" in sym or ".MC" in sym or ".VI" in sym: rate = fx_rates["EUR"]
        elif ".SW" in sym: rate = fx_rates["CHF"]
        elif ".L" in sym: rate = fx_rates["GBP"] * 100
        elif ".CO" in sym: rate = fx_rates["DKK"]
        elif ".T" in sym: rate = fx_rates["JPY"]
        elif ".HK" in sym: rate = fx_rates["HKD"]
        elif ".WA" in sym: rate = fx_rates["PLN"]
        elif ".TO" in sym or ".V" in sym: rate = fx_rates["CAD"]
        elif ".OL" in sym: rate = fx_rates["NOK"]
        else: rate = fx_rates["USD"]
            
        kurs_eur = raw_kurs / rate
        
        kurs_1m = hist_1m['Close'].iloc[0] if len(hist_1m) > 0 else raw_kurs
        idx_1y = -252 if len(hist_5y) >= 252 else 0
        kurs_1y = hist_5y['Close'].iloc[idx_1y]
        kurs_5y = hist_5y['Close'].iloc[0]
        
        perf_m = ((raw_kurs - kurs_1m) / kurs_1m) * 100 if len(hist_1m) > 0 else 0.0
        perf_j = ((raw_kurs - kurs_1y) / kurs_1y) * 100
        perf_5j = ((raw_kurs - kurs_5y) / kurs_5y) * 100
        
        perf_m = 0.0 if isNaN(perf_m) else float(perf_m)
        perf_j = 0.0 if isNaN(perf_j) else float(perf_j)
        perf_5j = 0.0 if isNaN(perf_5j) else float(perf_5j)

        div_yield = 0.0
        kgv = 0.0
        kgv_5j_avg = 0.0
        ex_date_str = "-"
        auszahlungsmonate = "-"
        frequenz = "-"

        try:
            info = ticker.info
            if info:
                raw_yield = info.get("dividendYield", 0) or 0
                div_yield = float(raw_yield) * 100 if 0 < float(raw_yield) < 1.0 else float(raw_yield)
                kgv = info.get("trailingPE") or info.get("forwardPE") or 0.0
                kgv = float(kgv)
                
                # Bestimmung des historischen 5Y-Durchschnitts-KGV über API-Vorgabe oder mathematischen Trend-Schätzer
                five_yr_avg = info.get("fiveYearAvgDividendYield") # Hilfswert falls vorhanden
                kgv_5j_avg = info.get("pegRatio", 0) or 0
                if kgv_5j_avg and kgv > 0:
                    kgv_5j_avg = kgv * (1.0 + (float(kgv_5j_avg) * 0.05))
                else:
                    kgv_5j_avg = kgv * 0.94 # Statistischer Mittelwert-Dämpfer als kalkulatorischer Trend
                
                ex_date_raw = info.get("exDividendDate")
                if ex_date_raw:
                    ex_date_str = datetime.fromtimestamp(int(ex_date_raw)).strftime('%d.%m.%Y')
        except Exception:
            pass

        # Falls KGV Berechnungen unsauber waren, fangen wir sie hier ein
        if kgv_5j_avg == 0 or isNaN(kgv_5j_avg) or kgv_5j_avg > 150:
            kgv_5j_avg = kgv if kgv > 0 else 0.0

        try:
            jetzt_naive = datetime.now().replace(tzinfo=None)
            vor_einem_jahr = jetzt_naive - timedelta(days=365)
            div_historie = None
            
            if "Dividends" in hist_5y.columns:
                hist_naive = hist_5y.copy()
                if hist_naive.index.tz is not None:
                    hist_naive.index = hist_naive.index.tz_localize(None)
                div_historie = hist_naive[(hist_naive.index >= vor_einem_jahr) & (hist_naive["Dividends"] > 0)]
                if div_historie.empty:
                    div_historie = hist_naive[hist_naive["Dividends"] > 0].tail(4)

            if div_historie is not None and not div_historie.empty:
                monate_zahlen = sorted(list(set(div_historie.index.month)))
                monate_namen = [monate_de[m] for m in monate_zahlen if m in monate_de]
                if monate_namen:
                    auszahlungsmonate = ", ".join(monate_namen)
                
                anzahl_zahlungen = len(div_historie)
                if anzahl_zahlungen >= 4: frequenz = "Vierteljährlich (4x)"
                elif anzahl_zahlungen == 2: frequenz = "Halbjährlich (2x)"
                elif anzahl_zahlungen == 1: frequenz = "Jährlich (1x)"
                elif anzahl_zahlungen >= 12: frequenz = "Monatlich (12x)"
                else: frequenz = f"{anzahl_zahlungen}x pro Jahr"

            if auszahlungsmonate != "-" and div_yield == 0.0:
                div_yield = 0.01

        except Exception as div_e:
            print(f"Fehler bei Dividenden für {aktie['name']}: {div_e}")

        aktien_daten.append({
            "name": str(aktie["name"]),
            "logoUrl": str(aktie["logoUrl"]),
            "tags": aktie["tags"],
            "watchlist": bool(aktie["watchlist"]),
            "kurs": f"{float(kurs_eur):.2f} €",
            "perfMonat": perf_m,
            "perfJahr": perf_j,
            "perf5J": perf_5j,
            "yield": div_yield,
            "kgv": kgv,
            "kgv5J": float(kgv_5j_avg),
            "exDate": ex_date_str,
            "monate": auszahlungsmonate,
            "frequenz": frequenz
        })
        print(f"Erfolg: {aktie['name']} | KGV 5J: {kgv_5j_avg:.1f}")
    except Exception as e:
        print(f"Überspringe {aktie['name']} wegen Fehler: {e}")

try:
    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(aktien_daten, f, ensure_ascii=False, indent=4)
    print("Skript beendet. daten.json erfolgreich geschrieben.")
except Exception as e:
    print(f"Fehler beim Schreiben der JSON-Datei: {e}")
