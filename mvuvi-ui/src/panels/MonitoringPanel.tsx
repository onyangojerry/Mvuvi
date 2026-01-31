import { Box, Typography, Divider, Paper, CircularProgress, Alert } from '@mui/material';
import { useEffect, useState } from 'react';

export default function MonitoringPanel() {
  const [metrics, setMetrics] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMetrics() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/metrics');
        const data = await res.text();
        if (res.ok) {
          setMetrics(data);
        } else {
          setError('Failed to fetch metrics');
        }
      } catch (e: any) {
        setError('Could not fetch metrics');
      }
      setLoading(false);
    }
    fetchMetrics();
  }, []);

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: '#181c24', fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Typography variant="h4" sx={{ color: '#ffb300', fontWeight: 900, mb: 3, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 32, textAlign: 'center' }}>
          SYSTEM MONITORING
        </Typography>
        <Divider sx={{ mb: 3, bgcolor: '#23272f', borderBottom: '2px solid #ffb300' }} />
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto' }}>
        {loading && <CircularProgress sx={{ color: '#ffb300', mx: 'auto', my: 4, display: 'block' }} />}
        {error && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}
        {!loading && !error && (
          <Paper sx={{ bgcolor: '#181c24', color: '#f8f8f8', p: 2, border: '2px solid #ffb300', borderRadius: 2, fontFamily: 'Roboto Mono, monospace', whiteSpace: 'pre-wrap', fontSize: 14, overflowX: 'auto' }}>
            {metrics}
          </Paper>
        )}
      </Box>
    </Box>
  );
}
