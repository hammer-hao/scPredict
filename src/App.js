import React, { useState } from 'react';
import UploadForm from './UploadForm';
import LineChart from './LineChart';

const App = () => {
  const [winRates, setWinRates] = useState([]);

  return (
    <div className="App">
      <h1>SC2 Replay Visualizer</h1>
      <UploadForm setWinRates={setWinRates} />
      {winRates.length > 0 && <LineChart winRates={winRates} />}
    </div>
  );
};

export default App;
