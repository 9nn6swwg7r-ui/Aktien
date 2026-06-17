import yfinance as yf
import json
import sys

# Radikal gekürzte Liste: Nur noch deine 33 Wunsch-Aktien
meine_aktien = [
    {"symbol": "1398.HK", "name": "Industrial & Commercial Bank of China", "logoUrl": "https://logo.clearbit.com/icbc.com.cn", "tags": ["Banken", "China", "Staatskonzern"]},
    {"symbol": "TPE.WA", "name": "Tauron Polska Energia", "logoUrl": "https://logo.clearbit.com/tauron.pl", "tags": ["Energie", "Versorger", "Polen"]},
    {"symbol": "DNP.WA", "name": "Dino Polska", "logoUrl": "https://logo.clearbit.com/grupadino.pl", "tags": ["Supermärkte", "Einzelhandel", "Polen"]},
    {"symbol": "LHA.DE", "name": "Deutsche Lufthansa", "logoUrl": "https://logo.clearbit.com/lufthansagroup.com", "tags": ["Airlines", "Luftfahrt", "Logistik"]},
    {"symbol": "FIH-U.TO", "name": "Fairfax India", "logoUrl": "https://logo.clearbit.com/fairfaxindia.ca", "tags": ["Beteiligungen", "Indien", "Investment"]},
    {"symbol": "EOAN.DE", "name": "E.ON", "logoUrl": "https://logo.clearbit.com/eon.com", "tags": ["Energienetze", "Infrastruktur", "Versorger"]},
    {"symbol": "CMCSA", "name": "Comcast A", "logoUrl": "https://logo.clearbit.com/comcastcorporation.com", "tags": ["Medien", "Kabelnetz", "Streaming"]},
    {"symbol": "KHC", "name": "Kraft Heinz", "logoUrl": "https://logo.clearbit.com/kraftheinzcompany.com", "tags": ["Lebensmittel", "Ketchup", "Marken"]},
    {"symbol": "VNA.DE", "name": "Vonovia", "logoUrl": "https://logo.clearbit.com/vonovia.de", "tags": ["Immobilien", "Wohnungen", "Vermieter"]},
    {"symbol": "PKO.WA", "name": "Powszechna Kasa Oszczednosci Bank", "logoUrl": "https://logo.clearbit.com/pkobp.pl", "tags": ["Banken", "Polen", "Finanzen"]},
    {"symbol": "DNB.OL", "name": "DNB Bank", "logoUrl": "https://logo.clearbit.com/dnb.no", "tags": ["Banken", "Norwegen", "Finanzservice"]},
    {"symbol": "6506.T", "name": "Yaskawa Electric", "logoUrl": "https://logo.clearbit.com/yaskawa-global.com", "tags": ["Robotik", "Motoren", "Automation"]},
    {"symbol": "6954.T", "name": "Fanuc", "logoUrl": "https://logo.clearbit.com/fanuc.co.jp", "tags": ["CNC-Systeme", "Roboter", "Fabrikautomation"]},
    {"symbol": "YAR.OL", "name": "Yara Intl.", "logoUrl": "https://logo.clearbit.com/yara.com", "tags": ["Düngemittel", "Agrar-Chemie", "Ernte"]},
    {"symbol": "VZ", "name": "Verizon", "logoUrl": "https://logo.clearbit.com/verizon.com", "tags": ["Telekom", "Mobilfunk", "5G"]},
    {"symbol": "DHL.DE", "name": "DHL", "logoUrl": "https://logo.clearbit.com/dhl.com", "tags": ["Logistik", "Pakete", "Post"]},
    {"symbol": "EVD.DE", "name": "CTS Eventim", "logoUrl": "https://logo.clearbit.com/eventim.de", "tags": ["Ticketing", "Konzerte", "Live-Events"]},
    {"symbol": "VER.VI", "name": "Verbund AG", "logoUrl": "https://logo.clearbit.com/verbund.com", "tags": ["Wasserkraft", "Strom", "Österreich"]},
    {"symbol": "CGNX", "name": "Cognex", "logoUrl": "https://logo.clearbit.com/cognex.com", "tags": ["Bildverarbeitung", "Sensoren", "Tech"]},
    {"symbol": "EUK3.DE", "name": "EUROKAI Vz.", "logoUrl": "https://logo.clearbit.com/eurokai.de", "tags": ["Hafenterminals", "Logistik", "Schifffahrt"]},
    {"symbol": "BMW3.DE", "name": "BMW Vz.", "logoUrl": "https://logo.clearbit.com/bmwgroup.com", "tags": ["Automobile", "Premium", "Motorrad"]},
    {"symbol": "PDD", "name": "Pinduoduo ADR", "logoUrl": "https://logo.clearbit.com/pddholdings.com", "tags": ["E-Commerce", "Temu", "China"]},
    {"symbol": "BEI.DE", "name": "Beiersdorf", "logoUrl": "https://logo.clearbit.com/beiersdorf.de", "tags": ["Nivea", "Hautpflege", "Konsumgüter"]},
    {"symbol": "SIX2.DE", "name": "Sixt St.", "logoUrl": "https://logo.clearbit.com/sixt.de", "tags": ["Autovermietung", "Mobilität", "Leasing"]},
    {"symbol": "ABBN.SW", "name": "ABB", "logoUrl": "https://logo.clearbit.com/abb.com", "tags": ["Elektrotechnik", "Automation", "Tech"]},
    {"symbol": "STR.VI", "name": "Strabag", "logoUrl": "https://logo.clearbit.com/strabag.com", "tags": ["Baukonzern", "Infrastruktur", "Tiefbau"]},
    {"symbol": "FRM.DE", "name": "FRoSTA", "logoUrl": "https://logo.clearbit.com/frosta-ag.de", "tags": ["Tiefkühlkost", "Ernährung", "Lebensmittel"]},
    {"symbol": "6367.T", "name": "Daikin Industries", "logoUrl": "https://logo.clearbit.com/daikin.com", "tags": ["Klimaanlagen", "Wärmepumpen", "Heizung"]},
    {"symbol": "ADSK", "name": "Autodesk", "logoUrl": "https://logo.clearbit.com/autodesk.com", "tags": ["CAD-Software", "3D-Design", "Architektur"]},
    {"symbol": "ADBE", "name": "Adobe", "logoUrl": "https://logo.clearbit.com/adobe.com", "tags": ["Photoshop", "Kreativ-Cloud", "Software"]},
    {"symbol": "SIKA.SW", "name": "Sika", "logoUrl": "https://logo.clearbit.com/sika.com", "tags": ["Spezialchemie", "Baustoffe", "Klebstoffe"]},
    {"symbol": "TER", "name": "Teradyne", "logoUrl": "https://logo.clearbit.com/teradyne.com", "tags": ["Testsysteme", "Halbleiter", "Automatisierung"]},
    {"symbol": "ROK", "name": "Rockwell Automation", "logoUrl": "https://logo.clearbit.com/rockwellautomation.com", "tags": ["Fabrikautomation", "Industriesoftware", "Tech"]}
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
