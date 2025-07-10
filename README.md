# SSHNL raspored i ljestvica

Ovaj projekt sadrži Flask API i React korisničko sučelje za prikaz ljestvice i rasporeda SuperSport HNL lige. Rezultate je moguće unositi ručno, a tablica se nakon svakog unosa automatski ažurira.

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

3. Instalirajte Node ovisnosti za React klijent:
   ```bash
   cd frontend
   npm install
   ```

4. Pokrenite razvojne servere u dvije odvojene konzole:
   ```bash
   # pokreni Flask API
   python app.py
   ```
   i
   ```bash
   # pokreni React klijent
   cd frontend && npm start
   ```
   React će se otvoriti na `http://localhost:3000` i prosljeđivati zahtjeve prema API-ju na portu 5000.

## Korištenje

Nakon pokretanja razvojnih servera, React aplikacija prikazuje ljestvicu i raspored svih kola. Uz svaki par nalazi se forma za unos rezultata. Nakon što unesete rezultat i kliknete **Spremi**, tablica i raspored automatski se osvježavaju.

Svi podaci se spremaju u datoteku `data/schedule.json` na strani poslužitelja.
