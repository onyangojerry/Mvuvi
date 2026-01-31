import { useState } from 'react';
import { Box, Typography, Button, Select, MenuItem, InputLabel, FormControl, Paper, CircularProgress, useTheme } from '@mui/material';



export default function OCRPanel() {
  const theme = useTheme();
  // const colorMode = useContext(ColorModeContext);
  // Persist state in localStorage
  const [file, setFile] = useState<File | null>(null);
  const [engine, setEngine] = useState(() => localStorage.getItem('ocr-engine') || 'tesseract');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(() => {
    const stored = localStorage.getItem('ocr-result');
    return stored ? JSON.parse(stored) : null;
  });
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // Restore file name (cannot restore File object, but can show name)
  const [fileName, setFileName] = useState(() => localStorage.getItem('ocr-file-name') || '');

  const ENGINES = [
    { label: 'Tesseract', value: 'tesseract' },
    { label: 'EasyOCR', value: 'easyocr' },
    { label: 'PaddleOCR', value: 'paddleocr' },
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setFileName(e.target.files[0].name);
      setResult(null);
      setError(null);
      localStorage.setItem('ocr-file-name', e.target.files[0].name);
    }
  };

  const handleEngineChange = (e: any) => {
    setEngine(e.target.value);
    localStorage.setItem('ocr-engine', e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('image', file);
      formData.append('engine', engine);
      formData.append('language', 'eng');
      formData.append('preprocess', 'false');
      const res = await fetch('/api/v1/ocr/extract', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.status === 200 && data.data) {
        setResult(data.data);
        localStorage.setItem('ocr-result', JSON.stringify(data.data));
      } else {
        // Handle FastAPI error format: detail can be string or object
        let errorMsg = 'OCR failed';
        if (typeof data.detail === 'string') {
          errorMsg = data.detail;
        } else if (typeof data.detail === 'object' && data.detail !== null) {
          // Try to extract message or error
          errorMsg = data.detail.message || data.detail.error || JSON.stringify(data.detail);
        } else if (data.error) {
          errorMsg = data.error;
        }
        setError(errorMsg);
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };


  // Upload to News Feed (full pipeline)
  const handleUploadToNewsFeed = async () => {
    if (!file) return;
    setUploading(true);
    setUploadStatus(null);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('image', file);
      formData.append('language', 'en');
      // Optionally add source, user_id, etc.
      const res = await fetch('/api/v1/ingest/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.status === 202 && data.status === 'accepted') {
        setUploadStatus('Uploaded! Article will appear in the news feed shortly.');
        setFile(null);
        setFileName('');
        localStorage.removeItem('ocr-file-name');
      } else {
        setError(data.detail?.message || data.error || 'Upload failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setUploading(false);
  };

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: theme.palette.background.default, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Typography variant="h4" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 3, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 32, textAlign: 'center' }}>
          OCR EXTRACTION
        </Typography>
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: { xs: '1fr' }, gap: { xs: 2, sm: 4 }, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto', alignItems: 'stretch' }}>
        <Paper sx={{ bgcolor: theme.palette.background.paper, color: theme.palette.text.primary, p: { xs: 2, sm: 3 }, boxShadow: '0 2px 12px #000a', border: `2px solid ${theme.palette.primary.main}`, borderRadius: 2, minHeight: 180, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
          <form onSubmit={handleSubmit}>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 3, alignItems: 'center', mb: 3 }}>
              <FormControl fullWidth sx={{ maxWidth: 200 }}>
                <InputLabel id="engine-label" sx={{ color: theme.palette.primary.main, fontWeight: 700, fontSize: 18 }}>Engine</InputLabel>
                <Select
                  labelId="engine-label"
                  value={engine}
                  label="Engine"
                  onChange={handleEngineChange}
                  sx={{ color: theme.palette.text.primary, bgcolor: theme.palette.background.default, fontWeight: 700, fontSize: 18 }}
                >
                  {ENGINES.map((eng) => (
                    <MenuItem key={eng.value} value={eng.value} sx={{ fontWeight: 700, fontSize: 18 }}>{eng.label}</MenuItem>
                  ))}
                </Select>
              </FormControl>
              <Button variant="contained" component="label" sx={{ bgcolor: theme.palette.primary.main, color: theme.palette.background.default, fontWeight: 900, fontSize: 18, px: 3, py: 1, boxShadow: '0 2px 8px #000a' }}>
                Upload Image
                <input type="file" accept="image/*" hidden onChange={handleFileChange} />
              </Button>
              {(fileName || file) && <Typography variant="body1" sx={{ color: theme.palette.primary.main, fontWeight: 700, fontSize: 18, ml: 2 }}>{file?.name || fileName}</Typography>}
              <Button type="submit" variant="contained" sx={{ bgcolor: theme.palette.background.default, color: theme.palette.primary.main, fontWeight: 900, fontSize: 18, px: 3, py: 1, boxShadow: '0 2px 8px #000a' }} disabled={!file || loading}>
                {loading ? <CircularProgress size={28} sx={{ color: theme.palette.primary.main }} /> : 'Extract Text'}
              </Button>
              {/* Upload to News Feed button, enabled after extraction */}
              <Button
                variant="contained"
                sx={{ bgcolor: theme.palette.primary.main, color: theme.palette.background.default, fontWeight: 900, fontSize: 18, px: 3, py: 1, boxShadow: '0 2px 8px #000a' }}
                disabled={!file || uploading}
                onClick={handleUploadToNewsFeed}
              >
                {uploading ? <CircularProgress size={28} sx={{ color: theme.palette.background.default }} /> : 'Upload to News Feed'}
              </Button>
            </Box>
          </form>
          {result && (
            <Box sx={{ mt: 4, p: 3, bgcolor: theme.palette.background.default, borderRadius: 2, border: `1px solid ${theme.palette.primary.main}`, boxShadow: '0 2px 8px #000a' }}>
              <Typography variant="h5" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 24, textAlign: 'center' }}>RESULT</Typography>
              <Typography variant="body1" sx={{ mb: 2, fontSize: 20, color: theme.palette.text.primary, textAlign: 'center' }}><b>Text:</b> <span style={{ color: theme.palette.primary.main, fontWeight: 700 }}>{result.text}</span></Typography>
              <Typography variant="body1" sx={{ fontSize: 18, color: theme.palette.text.primary, textAlign: 'center' }}><b>Confidence:</b> <span style={{ color: theme.palette.primary.main, fontWeight: 700 }}>{result.confidence}</span></Typography>
              <Typography variant="body1" sx={{ fontSize: 18, color: theme.palette.text.primary, textAlign: 'center' }}><b>Word Count:</b> <span style={{ color: theme.palette.primary.main, fontWeight: 700 }}>{result.word_count}</span></Typography>
            </Box>
          )}
          {uploadStatus && (
            <Typography variant="body1" sx={{ color: theme.palette.success.main, mt: 3, fontWeight: 900, fontSize: 18, textAlign: 'center' }}>{uploadStatus}</Typography>
          )}
          {error && (
            <Typography variant="body1" sx={{ color: '#ff1744', mt: 3, fontWeight: 900, fontSize: 18, textAlign: 'center' }}>{typeof error === 'string' ? error : JSON.stringify(error)}</Typography>
          )}
        </Paper>
      </Box>
    </Box>
  );
}
