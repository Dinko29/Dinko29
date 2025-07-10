# SSHNL raspored i ljestvica

Ovaj projekt sadrži malu Flask aplikaciju koja prikazuje ljestvicu i raspored SuperSport HNL lige. Rezultate je moguće unositi ručno, a tablica se nakon svakog unosa automatski ažurira.

## Postavljanje

1. Instalirajte ovisnosti:
   ```bash
   pip install -r requirements.txt
   ```

2. Preuzmite raspored sa službene stranice HNL-a pokretanjem skripte:
   ```bash
   python scrape_schedule.py
   ```
   Skripta koristi knjižnice `requests` i `BeautifulSoup` za dohvat podataka s [hnl.hr](https://hnl.hr/). Ako se struktura stranice promijeni, možda ćete morati prilagoditi CSS selektore unutar `scrape_schedule.py`.

3. Pokrenite aplikaciju:
   ```bash
   python app.py
   ```
   Aplikacija će biti dostupna na `http://localhost:5000`.

## Korištenje

Na početnoj stranici prikazuje se ljestvica i ispod nje raspored svih kola. Uz svaki par nalazi se forma za unos rezultata. Nakon što unesete rezultat i kliknete **Spremi**, stranica će se ponovno učitati s ažuriranim podacima.

Svi podaci se spremaju u datoteku `data/schedule.json`.
