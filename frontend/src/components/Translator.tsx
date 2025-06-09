import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  Box,
  Paper,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Typography,
  CircularProgress,
  Stack,
} from '@mui/material';
import {
  VolumeUp as VolumeUpIcon,
  Translate as TranslateIcon,
  RecordVoiceOver as RecordVoiceOverIcon,
} from '@mui/icons-material';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const languages = [
  { id: 'tamil', name: 'Tamil' },
  { id: 'telugu', name: 'Telugu' },
  { id: 'hindi', name: 'Hindi' },
];

const Translator: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('tamil');
  const [translatedText, setTranslatedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const handleTranslate = async () => {
    if (!inputText.trim()) {
      toast.error('Please enter some text to translate');
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/translate`, {
        text: inputText,
        target_language: targetLanguage,
      });
      setTranslatedText(response.data.translated_text);
      toast.success('Translation completed!');
    } catch (error) {
      if (axios.isAxiosError(error)) {
        toast.error(error.response?.data?.detail || 'Translation failed. Please try again.');
      } else {
        toast.error('Translation failed. Please try again.');
      }
      console.error('Translation error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextToSpeech = async () => {
    if (!translatedText.trim()) {
      toast.error('Please translate text first');
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/text-to-speech`,
        {
          text: translatedText,
          language: targetLanguage,
        },
        { responseType: 'blob' }
      );
      const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl);
      toast.success('Audio generated!');
    } catch (error) {
      if (axios.isAxiosError(error)) {
        toast.error(error.response?.data?.detail || 'Failed to generate audio. Please try again.');
      } else {
        toast.error('Failed to generate audio. Please try again.');
      }
      console.error('TTS error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslateAndSpeak = async () => {
    if (!inputText.trim()) {
      toast.error('Please enter some text to translate');
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/translate-and-speak`,
        {
          text: inputText,
          target_language: targetLanguage,
        }
      );
      
      setTranslatedText(response.data.translated_text);
      
      // Convert base64 to blob
      const audioData = atob(response.data.audio_data);
      const audioArray = new Uint8Array(audioData.length);
      for (let i = 0; i < audioData.length; i++) {
        audioArray[i] = audioData.charCodeAt(i);
      }
      const audioBlob = new Blob([audioArray], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl);
      
      toast.success('Translation and audio generation completed!');
    } catch (error) {
      if (axios.isAxiosError(error)) {
        toast.error(error.response?.data?.detail || 'Operation failed. Please try again.');
      } else {
        toast.error('Operation failed. Please try again.');
      }
      console.error('Combined operation error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Cleanup audio URL when component unmounts
  React.useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Stack spacing={3}>
        <FormControl fullWidth>
          <InputLabel id="language-label">Target Language</InputLabel>
          <Select
            labelId="language-label"
            value={targetLanguage}
            label="Target Language"
            onChange={(e) => setTargetLanguage(e.target.value)}
          >
            {languages.map((lang) => (
              <MenuItem key={lang.id} value={lang.id}>
                {lang.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="Input Text (English)"
          multiline
          rows={4}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text to translate..."
          fullWidth
        />

        <Stack direction="row" spacing={2}>
          <Button
            variant="contained"
            onClick={handleTranslate}
            disabled={isLoading}
            startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <TranslateIcon />}
          >
            Translate
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleTranslateAndSpeak}
            disabled={isLoading}
            startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <RecordVoiceOverIcon />}
          >
            Translate & Speak
          </Button>
        </Stack>

        {translatedText && (
          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Translated Text
            </Typography>
            <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
              <Typography>{translatedText}</Typography>
            </Paper>
            <Button
              variant="contained"
              color="primary"
              onClick={handleTextToSpeech}
              disabled={isLoading || !translatedText}
              startIcon={<VolumeUpIcon />}
              sx={{ mt: 2 }}
            >
              Speak
            </Button>
          </Box>
        )}

        {audioUrl && (
          <Box sx={{ mt: 2 }}>
            <audio controls style={{ width: '100%' }}>
              <source src={audioUrl} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          </Box>
        )}
      </Stack>
    </Paper>
  );
};

export default Translator; 