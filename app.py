import json
from collections import defaultdict

from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
import os

DATA_FILE = 'data/schedule.json'

app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
CORS(app)

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



@app.route('/api/schedule')
def get_schedule():
    schedule = load_schedule()
    return jsonify(schedule)


@app.route('/api/table')
def get_table():
    schedule = load_schedule()
    table = [dict(team=t, **stats) for t, stats in compute_table(schedule)]
    return jsonify(table)


@app.route('/api/update/<int:match_id>', methods=['POST'])
def update_match(match_id: int):
    schedule = load_schedule()
    data = request.get_json(force=True)
    try:
        hg = int(data.get('home_goals'))
        ag = int(data.get('away_goals'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid data'}), 400
    if 0 <= match_id < len(schedule):
        schedule[match_id]['score'] = [hg, ag]
        save_schedule(schedule)
    return jsonify({'success': True})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    root = app.static_folder
    if path != "" and os.path.exists(os.path.join(root, path)):
        return send_from_directory(root, path)
    return send_from_directory(root, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
