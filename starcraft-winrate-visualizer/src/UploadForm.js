import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Box, Typography, Paper, CircularProgress } from '@mui/material';
import { styled } from '@mui/system';

const FormContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  marginTop: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
}));

const UploadForm = ({ setWinRates, setPlayerName }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Start loading
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('https://ociscwinrates.hammerhao.net/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setWinRates(response.data.winrates);
      setPlayerName(response.data.player_1_name);
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false); // End loading
    }
  };

  return (
    <FormContainer elevation={3}>
      <Typography variant="h5" component="h1" gutterBottom>
        Upload Starcraft 2 Replay
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <TextField
          type="file"
          onChange={handleFileChange}
          accept=".sc2replay"
          InputLabelProps={{ shrink: true }}
          sx={{ mb: 2 }}
        />
        <Button variant="contained" color="primary" type="submit" disabled={loading}>
          Upload Replay
        </Button>
        {loading && (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 2 }}>
            <CircularProgress />
            <Typography variant="body1" sx={{ mt: 1 }}>
              Processing your replay, please wait...
            </Typography>
          </Box>
        )}
      </Box>
    </FormContainer>
  );
};

export default UploadForm;