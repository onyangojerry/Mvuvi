import { Box, Typography, Divider, Paper, CircularProgress, Alert, useTheme } from '@mui/material';
import { useEffect, useState, useContext } from 'react';
import { ColorModeContext } from '../App';

export default function DashboardPanel() {
  const theme = useTheme();
  // const colorMode = useContext(ColorModeContext);
  const [status, setStatus] = useState<'loading'|'healthy'|'unhealthy'|'error'>('loading');
  const [components, setComponents] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHealth() {
      setStatus('loading');
      setError(null);
      try {
        const res = await fetch('/api/v1/health');
        const data = await res.json();
        if (res.ok && data.status === 'healthy') {
          setStatus('healthy');
          setComponents(data.components || null);
        } else {
          setStatus('unhealthy');
          setComponents(data.components || null);
        }
      } catch (e: any) {
        setStatus('error');
        setError('Could not fetch system status');
      }
    }
    fetchHealth();
  }, []);

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: theme.palette.background.default, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Typography variant="h4" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 3, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 32, textAlign: 'center' }}>
          DASHBOARD
        </Typography>
        <Divider sx={{ mb: 3, bgcolor: theme.palette.background.paper, borderBottom: `2px solid ${theme.palette.primary.main}` }} />
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(auto-fit, minmax(320px, 1fr))' }, gap: { xs: 2, sm: 4 }, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto', alignItems: 'stretch' }}>
        <Paper sx={{ bgcolor: theme.palette.background.paper, color: theme.palette.text.primary, p: { xs: 2, sm: 3 }, boxShadow: '0 2px 12px #000a', border: `2px solid ${theme.palette.primary.main}`, borderRadius: 2, minHeight: 180, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
          <Typography variant="h6" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 2, fontSize: 22, borderBottom: `1px solid ${theme.palette.background.paper}`, pb: 1, letterSpacing: 1, fontFamily: 'Roboto Mono, monospace', textAlign: 'center' }}>
            System Status
          </Typography>
          {status === 'loading' && <CircularProgress sx={{ color: theme.palette.primary.main, mx: 'auto', my: 2 }} />}
          {status === 'error' && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}
          {status !== 'loading' && status !== 'error' && (
            <Typography variant="body1" sx={{ fontFamily: 'Roboto Mono, monospace', fontWeight: 700, color: status === 'healthy' ? '#00e676' : '#ff1744', fontSize: 18, textAlign: 'center' }}>
              ● {status === 'healthy' ? 'All systems operational' : 'Some systems unhealthy'}
            </Typography>
          )}
          {components && (
            <Box sx={{ mt: 2 }}>
              {Object.entries(components).map(([key, value]) => (
                <Typography key={key} variant="body2" sx={{ color: value === 'healthy' ? '#00e676' : '#ff1744', fontWeight: 700, textAlign: 'center', fontFamily: 'Roboto Mono, monospace' }}>
                  {key}: {String(value)}
                </Typography>
              ))}
            </Box>
          )}
        </Paper>
        <Paper sx={{ bgcolor: theme.palette.background.paper, color: theme.palette.text.primary, p: { xs: 2, sm: 3 }, boxShadow: '0 2px 12px #000a', border: `2px solid ${theme.palette.primary.main}`, borderRadius: 2, minHeight: 180, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
          <Typography variant="h6" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 2, fontSize: 22, borderBottom: `1px solid ${theme.palette.background.paper}`, pb: 1, letterSpacing: 1, fontFamily: 'Roboto Mono, monospace', textAlign: 'center' }}>
            Recent Activity
          </Typography>
          <Typography variant="body1" sx={{ fontFamily: 'Roboto Mono, monospace', fontWeight: 700, color: theme.palette.text.primary, fontSize: 18, textAlign: 'center' }}>
            No recent alerts
          </Typography>
        </Paper>
        <Paper sx={{ bgcolor: theme.palette.background.paper, color: theme.palette.text.primary, p: { xs: 2, sm: 3 }, boxShadow: '0 2px 12px #000a', border: `2px solid ${theme.palette.primary.main}`, borderRadius: 2, minHeight: 180, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
          <Typography variant="h6" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 2, fontSize: 22, borderBottom: `1px solid ${theme.palette.background.paper}`, pb: 1, letterSpacing: 1, fontFamily: 'Roboto Mono, monospace', textAlign: 'center' }}>
            Quick Actions
          </Typography>
          <Typography variant="body1" sx={{ fontFamily: 'Roboto Mono, monospace', fontWeight: 700, color: theme.palette.primary.main, fontSize: 18, textAlign: 'center' }}>
            Use sidebar to access OCR, News, Settings
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
}
