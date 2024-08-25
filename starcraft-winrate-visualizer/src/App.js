import React, { useState } from 'react';
import UploadForm from './UploadForm';
import LineChart from './LineChart';
import Panel from './Panel';
import './App.css';

const App = () => {
  const [winRates, setWinRates] = useState([]);
  const [playerName, setPlayerName] = useState('');
  const [player2Name, setPlayer2Name] = useState('');
  const [filename, setFilename] = useState('');  // Add this state to store the filename
  const [panelVisible, setPanelVisible] = useState(false);
  const [selectedPoint, setSelectedPoint] = useState(null);

  const handlePointClick = (index) => {
    setSelectedPoint(index);
    setPanelVisible(true);
  };

  return (
    <div className="App">
      <h1>SC2 Replay Visualizer</h1>
      <UploadForm 
        setWinRates={setWinRates} 
        setPlayerName={setPlayerName} 
        setPlayer2Name={setPlayer2Name} 
        setFilename={setFilename}  // Pass the setFilename function
      />
      {winRates.length > 0 && (
        <div className="chart-panel-container">
          <LineChart
            winRates={winRates}
            playerName={playerName}
            onPointClick={handlePointClick}
          />
          {panelVisible && (
            <Panel
              playerName={playerName}
              player2Name={player2Name}
              selectedTimestamp={selectedPoint}
              filename={filename}  // Pass the filename to the Panel
            />
          )}
        </div>
      )}
    </div>
  );
};

export default App;