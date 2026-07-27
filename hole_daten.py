import time
import yfinance as yf

# Liste der Tickersymbole aus Ihrem Workflow
tickers = ["MSFT", "TSM", "SAP.DE", "ORCL", "AVGO"]

def fetch_data():
    for ticker in tickers:
        try:
            print(f"Rufe Daten ab für {ticker}...")
            
            # Das Herunterladen der Daten für 1 Jahr
            data = yf.download(ticker, period="1y", progress=False)
            
            if data.empty:
                print(f"Warnung: Keine Preisdaten für {ticker} gefunden (möglicherweise delisted oder blockiert).")
            else:
                print(f"Erfolgreich: Daten für {ticker} geladen. Zeilen: {len(data)}")
                # Fügen Sie hier Ihre weitere Datenverarbeitung ein (z.B. Speichern als CSV)
                # data.to_csv(f"{ticker}.csv")

            # Wichtig: Eine kurze Pause einbauen, um Rate-Limits / IP-Blocks in CI/CD zu verhindern
            time.sleep(3)
            
        except Exception as e:
            print(f"Fehler beim Abrufen von Ticker '{ticker}' Grund: {e}")

if __name__ == "__main__":
    fetch_data()
