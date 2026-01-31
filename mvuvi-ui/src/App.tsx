import React, { useMemo, useState, useEffect } from 'react';
import { CssBaseline, Box } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import DashboardPanel from './panels/DashboardPanel';
import OCRPanel from './panels/OCRPanel';
import NewsFeedPanel from './panels/NewsFeedPanel';
import SettingsPanel from './panels/SettingsPanel';

export const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

function TerminalHeader() {
  const location = useLocation();
  let title = 'MVUVI TERMINAL';
  if (location.pathname === '/ocr') title = 'OCR ENGINE';
  if (location.pathname === '/feed') title = 'NEWS FEED';
  if (location.pathname === '/settings') title = 'SETTINGS';
  return (
    <Box sx={{ bgcolor: 'background.paper', color: 'primary.main', px: 3, py: 2, display: 'flex', alignItems: 'center', borderBottom: '2px solid', borderColor: 'primary.main', fontWeight: 900, fontSize: 28, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', boxShadow: '0 2px 12px #000a' }}>
      {title}
      <Box sx={{ ml: 'auto', fontSize: 16, color: 'text.primary', fontWeight: 700, letterSpacing: 1 }}>
        {new Date().toLocaleTimeString()}
      </Box>
    </Box>
  );
}

export default function App() {
  // Persist theme in localStorage
  const [darkMode, setDarkMode] = useState(() => {
    const stored = localStorage.getItem('mvuvi-theme');
    return stored ? stored === 'dark' : true;
  });
  useEffect(() => {
    localStorage.setItem('mvuvi-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  const colorMode = useMemo(() => ({
    toggleColorMode: () => setDarkMode((prev) => !prev),
  }), []);

  const theme = useMemo(() => createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      background: {
        default: darkMode ? '#181c24' : '#f8f8f8',
        paper: darkMode ? '#181c24' : '#fff',
      },
      primary: { main: '#ffb300' },
      text: {
        primary: darkMode ? '#f8f8f8' : '#181c24',
        secondary: darkMode ? '#888' : '#23272f',
      },
    },
    typography: {
      fontFamily: 'Roboto Mono, monospace',
    },
  }), [darkMode]);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Box sx={{ bgcolor: 'background.default', minHeight: '100vh', height: '100vh', fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0 }}>
              <TerminalHeader />
              <Box sx={{ display: 'flex', flex: 1, minHeight: 0, overflow: 'hidden' }}>
                <Box sx={{ bgcolor: 'background.paper', width: 80, display: 'flex', flexDirection: 'column', alignItems: 'center', pt: 4, borderRight: '2px solid', borderColor: 'primary.main', gap: 3, boxShadow: '2px 0 12px #000a' }}>
                  {/* Sidebar icons */}
                  <a href="/" style={{ color: theme.palette.primary.main, textDecoration: 'none', fontWeight: 900, fontSize: 22, fontFamily: 'Roboto Mono, monospace', padding: '8px 0' }}>⌂</a>
                  <a href="/ocr" style={{ color: theme.palette.primary.main, textDecoration: 'none', fontWeight: 900, fontSize: 22, fontFamily: 'Roboto Mono, monospace', padding: '8px 0' }}>OCR</a>
                  <a href="/feed" style={{ color: theme.palette.primary.main, textDecoration: 'none', fontWeight: 900, fontSize: 22, fontFamily: 'Roboto Mono, monospace', padding: '8px 0' }}>NEWS</a>
                  <a href="/settings" style={{ color: theme.palette.primary.main, textDecoration: 'none', fontWeight: 900, fontSize: 22, fontFamily: 'Roboto Mono, monospace', padding: '8px 0' }}>⚙</a>
                </Box>
                <Box sx={{ flex: 1, p: 0, display: 'grid', gridTemplateRows: '1fr', gridTemplateColumns: '1fr', bgcolor: 'background.default', overflow: 'auto', borderRadius: 0, minHeight: 0 }}>
                  <Routes>
                    <Route path="/" element={<DashboardPanel />} />
                    <Route path="/ocr" element={<OCRPanel />} />
                    <Route path="/feed" element={<NewsFeedPanel />} />
                    <Route path="/settings" element={<SettingsPanel />} />
                  </Routes>
                </Box>
              </Box>
            </Box>
          </Box>
        </Router>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}
