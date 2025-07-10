import json
from collections import defaultdict
from flask import Flask, render_template, request, redirect

DATA_FILE = 'data/schedule.json'

app = Flask(__name__)


def load_schedule():
    with open(DATA_FILE, encoding='utf-8') as f:
        return json.load(f)

def save_schedule(schedule):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)

def compute_table(schedule):
    table = defaultdict(lambda: {'P':0, 'W':0, 'D':0, 'L':0, 'GF':0, 'GA':0, 'Pts':0})
    for match in schedule:
        if match['score'] is None:
            continue
        hg, ag = match['score']
        home = match['home']
        away = match['away']
        table[home]['P'] += 1
        table[away]['P'] += 1
        table[home]['GF'] += hg
        table[home]['GA'] += ag
        table[away]['GF'] += ag
        table[away]['GA'] += hg
        if hg > ag:
            table[home]['W'] += 1
            table[home]['Pts'] += 3
            table[away]['L'] += 1
        elif hg < ag:
            table[away]['W'] += 1
            table[away]['Pts'] += 3
            table[home]['L'] += 1
        else:
            table[home]['D'] += 1
            table[away]['D'] += 1
            table[home]['Pts'] += 1
            table[away]['Pts'] += 1
    sorted_table = sorted(table.items(), key=lambda i: (i[1]['Pts'], i[1]['GF']-i[1]['GA'], i[1]['GF']), reverse=True)
    return sorted_table


@app.route('/')
def index():
    schedule = load_schedule()
    table = compute_table(schedule)
    return render_template('index.html', schedule=schedule, table=table)


@app.route('/update/<int:match_id>', methods=['POST'])
def update_match(match_id: int):
    schedule = load_schedule()
    try:
        hg = int(request.form['home_goals'])
        ag = int(request.form['away_goals'])
    except (KeyError, ValueError):
        return redirect('/')
    if 0 <= match_id < len(schedule):
        schedule[match_id]['score'] = [hg, ag]
        save_schedule(schedule)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
