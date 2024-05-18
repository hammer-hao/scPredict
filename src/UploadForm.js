import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = ({ setWinRates }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://129.153.228.72/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setWinRates(response.data.winrates);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleFileChange} accept=".sc2replay" />
      <button type="submit">Upload Replay</button>
    </form>
  );
};

export default UploadForm;