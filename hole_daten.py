            # ... [Dein bisheriger oberer Teil von hole_daten.py bleibt gleich] ...

            # Fehlerfreie Absicherung für Performance- und Finanzkennzahlen
            try: perf_m = float(perf_m) if not isNaN(perf_m) else 0.0
            except: perf_m = 0.0
            
            try: perf_j = float(perf_j) if not isNaN(perf_j) else 0.0
            except: perf_j = 0.0
            
            try: perf_5j = float(perf_5j) if not isNaN(perf_5j) else 0.0
            except: perf_5j = 0.0

            try:
                raw_yield = info.get("dividendYield", 0) or 0
                div_yield = float(raw_yield) * 100 if 0 < float(raw_yield) < 1.0 else float(raw_yield)
            except:
                div_yield = 0.0
                
            try: 
                kgv = info.get("trailingPE") or info.get("forwardPE") or 0.0
                kgv = float(kgv)
            except: 
                kgv = 0.0
            
            aktien_daten.append({
                "name": str(aktie["name"]),
                "logoUrl": str(aktie["logoUrl"]) if aktie["logoUrl"] else "",
                "tags": aktie["tags"],
                "watchlist": bool(aktie["watchlist"]),
                "kurs": f"{float(kurs_eur):.2f} €",
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
