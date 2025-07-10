import json
import requests
from bs4 import BeautifulSoup

URL = "https://hnl.hr/supersport-hnl/raspored-i-rezultati/"


def fetch_schedule():
    """Fetch schedule data from hnl.hr and return a list of matches."""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    schedule = []
    # The CSS selectors below are a best guess. Inspect the page and adjust them
    # if necessary to match the real HTML structure.
    rounds = soup.select("div.round")
    for r_idx, r in enumerate(rounds, start=1):
        matches = r.select("div.match")
        for m in matches:
            home = m.select_one(".home").get_text(strip=True)
            away = m.select_one(".away").get_text(strip=True)
            date = m.select_one(".date").get_text(strip=True)
            time = m.select_one(".time").get_text(strip=True)
            schedule.append({
                "round": r_idx,
                "home": home,
                "away": away,
                "date": date,
                "time": time,
                "score": None
            })
    return schedule


def main():
    schedule = fetch_schedule()
    with open("data/schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(schedule)} matches to data/schedule.json")


if __name__ == "__main__":
    main()
