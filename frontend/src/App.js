import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [schedule, setSchedule] = useState([]);
  const [table, setTable] = useState([]);

  const loadData = async () => {
    const [schedRes, tableRes] = await Promise.all([
      fetch('/api/schedule'),
      fetch('/api/table')
    ]);
    setSchedule(await schedRes.json());
    setTable(await tableRes.json());
  };

  useEffect(() => {
    loadData();
  }, []);

  const submitResult = async (idx, hg, ag) => {
    await fetch(`/api/update/${idx}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ home_goals: hg, away_goals: ag })
    });
    loadData();
  };

  return (
    <div className="container">
      <h1>SSHNL Ljestvica</h1>
      <table className="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Momčad</th>
            <th>P</th>
            <th>W</th>
            <th>D</th>
            <th>L</th>
            <th>GF</th>
            <th>GA</th>
            <th>Pts</th>
          </tr>
        </thead>
        <tbody>
          {table.map((row, i) => (
            <tr key={row.team}>
              <td>{i + 1}</td>
              <td>{row.team}</td>
              <td>{row.P}</td>
              <td>{row.W}</td>
              <td>{row.D}</td>
              <td>{row.L}</td>
              <td>{row.GF}</td>
              <td>{row.GA}</td>
              <td>{row.Pts}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Raspored</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Kolo</th>
            <th>Domaćin</th>
            <th>Gost</th>
            <th>Datum</th>
            <th>Rezultat</th>
          </tr>
        </thead>
        <tbody>
          {schedule.map((match, idx) => (
            <tr key={idx}>
              <td>{match.round}</td>
              <td>{match.home}</td>
              <td>{match.away}</td>
              <td>{match.date} {match.time}</td>
              <td>
                <ResultForm score={match.score} onSave={(hg, ag) => submitResult(idx, hg, ag)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ResultForm({ score, onSave }) {
  const [hg, setHg] = useState(score ? score[0] : '');
  const [ag, setAg] = useState(score ? score[1] : '');

  return (
    <form onSubmit={e => { e.preventDefault(); onSave(hg, ag); }}>
      <input style={{width:'40px'}} type="number" min="0" value={hg}
             onChange={e => setHg(e.target.value)} />
      :
      <input style={{width:'40px'}} type="number" min="0" value={ag}
             onChange={e => setAg(e.target.value)} />
      <button type="submit">Spremi</button>
    </form>
  );
}

export default App;
