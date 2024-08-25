import React, { useState } from 'react';
import axios from 'axios';
import './Panel.css';

const Panel = ({ playerName, player2Name, selectedTimestamp, filename }) => {
  const [replayResults, setReplayResults] = useState([]); // State to store replay results
  const [isLoading, setIsLoading] = useState(false); // State to track loading

  const formatTime = (index) => {
    const totalSeconds = index * 5;
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const calculateTimestamp = (index) => {
    return index + 1; // Convert index to 5-second intervals (1-based index)
  };

  const convertToSeconds = (index) => {
    return Math.floor(index / 112);
  };

  const handleFindReplaysClick = async () => {
    const timestamp = calculateTimestamp(selectedTimestamp); // Calculate timestamp
    setIsLoading(true); // Start loading indicator

    try {
      const formData = new FormData();
      formData.append('filename', filename);
      formData.append('timestamp', timestamp);

      const response = await axios.post('https://sciiwinrates.hammerhao.net/pca', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const fileNames = response.data.file_names;
      const timestamps = response.data.timestamps;

      if (fileNames && timestamps && fileNames.length === timestamps.length) {
        const results = fileNames.map((fileName, index) => ({
          fileName,
          timestamp: timestamps[index],
        }));
        setReplayResults(results);
      } else {
        console.error("Error: File names and timestamps arrays are not correctly returned or mismatched.");
      }
    } catch (error) {
      console.error("Error finding similar replays:", error);
    } finally {
      setIsLoading(false); // Stop loading indicator
    }
  };

  return (
    <div className="panel">
      <div className="panel-content">
        <div className="panel-details">
          <h2>Game Details</h2>
          <p><strong>Player 1:</strong> {playerName}</p>
          <p><strong>Player 2:</strong> {player2Name}</p>
          <p><strong>Selected Time:</strong> {formatTime(selectedTimestamp)}</p>
        </div>
        <button className="find-replays-button" onClick={handleFindReplaysClick} disabled={isLoading}>
          {isLoading ? 'Finding Replays...' : 'Find Similar Pro Replays to This Timestamp'}
        </button>
        <div className="replay-results">
          {isLoading ? (
            <div className="spinner"></div>  /* Add the spinner here */
          ) : (
            <>
              <h3>Similar Replays</h3>
              {replayResults.length > 0 ? (
                <table>
                  <thead>
                    <tr>
                      <th>File Name</th>
                      <th>In-game Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {replayResults.slice(0, 3).map((replay, index) => ( // Display only the first three rows
                      <tr key={index}>
                        <td>{replay.fileName}</td>
                        <td>{formatTime(convertToSeconds(replay.timestamp))}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p>No similar replays found.</p>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Panel;
