import { Box, Typography, Divider, Paper, CircularProgress, Alert, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { useEffect, useState } from 'react';

export default function IngestionPanel() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHistory() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/v1/ingest/history');
        const data = await res.json();
        if (res.ok && data.data) {
          setHistory(data.data);
        } else {
          setError('Failed to fetch ingestion history');
        }
      } catch (e: any) {
        setError('Could not fetch ingestion history');
      }
      setLoading(false);
    }
    fetchHistory();
  }, []);

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: '#181c24', fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Typography variant="h4" sx={{ color: '#ffb300', fontWeight: 900, mb: 3, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 32, textAlign: 'center' }}>
          INGESTION HISTORY
        </Typography>
        <Divider sx={{ mb: 3, bgcolor: '#23272f', borderBottom: '2px solid #ffb300' }} />
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto' }}>
        {loading && <CircularProgress sx={{ color: '#ffb300', mx: 'auto', my: 4, display: 'block' }} />}
        {error && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}
        {!loading && !error && (
          <TableContainer component={Paper} sx={{ bgcolor: '#181c24', color: '#f8f8f8', border: '2px solid #ffb300', borderRadius: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ color: '#ffb300', fontWeight: 900 }}>ID</TableCell>
                  <TableCell sx={{ color: '#ffb300', fontWeight: 900 }}>File</TableCell>
                  <TableCell sx={{ color: '#ffb300', fontWeight: 900 }}>Status</TableCell>
                  <TableCell sx={{ color: '#ffb300', fontWeight: 900 }}>Uploaded</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {history.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell sx={{ color: '#f8f8f8' }}>{row.id}</TableCell>
                    <TableCell sx={{ color: '#f8f8f8' }}>{row.filename}</TableCell>
                    <TableCell sx={{ color: row.status === 'completed' ? '#00e676' : '#ffb300', fontWeight: 700 }}>{row.status}</TableCell>
                    <TableCell sx={{ color: '#f8f8f8' }}>{row.uploaded_at}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Box>
    </Box>
  );
}
