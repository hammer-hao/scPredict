import React, { useState } from 'react';
import UploadForm from './UploadForm';
import LineChart from './LineChart';
import './App.css';

const App = () => {
  const [winRates, setWinRates] = useState([]);
  const [playerName, setPlayerName] = useState('');

  return (
    <div className="App">
      <h1>SC2 Replay Visualizer</h1>
      <UploadForm setWinRates={setWinRates} setPlayerName={setPlayerName}/>
      {winRates.length > 0 && <LineChart winRates={winRates} playerName={playerName} />}
    </div>
  );
};

export default App;
