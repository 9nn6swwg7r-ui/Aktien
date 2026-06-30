import yfinance as yf
import json
import sys
import math
from datetime import datetime

def isNaN(num):
    return isinstance(num, float) and math.isnan(num)

# Komplett bereinigte Liste aller Aktien
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
    {"symbol": "ROG.SW", "name": "Roche", "logoUrl": "
