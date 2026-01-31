import { useState, useEffect, useContext } from 'react';
import { Box, Typography, Paper, Divider, FormControlLabel, Switch, Select, MenuItem, Chip } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { ColorModeContext } from '../App';

export default function SettingsPanel() {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const [darkMode, setDarkMode] = useState(theme.palette.mode === 'dark');
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['Technology', 'Business']);
  const [language, setLanguage] = useState('en');
  const [notifications, setNotifications] = useState(true);
  const categories = ['Technology', 'World', 'Business', 'Science', 'General'];
  const languages = ['en', 'sw', 'fr', 'es'];
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);

  useEffect(() => {
    async function fetchPrefs() {
      try {
        const res = await fetch('/api/v1/auth/me');
        if (res.ok) {
          const data = await res.json();
          if (data.preferences) {
            setSelectedCategories(data.preferences.categories || []);
            setLanguage(data.preferences.languages?.[0] || 'en');
            setNotifications(data.preferences.notifications ?? true);
            setDarkMode(data.preferences.theme === 'dark');
          }
        }
      } catch {}
    }
    fetchPrefs();
  }, []);

  // When darkMode changes, update global theme
  useEffect(() => {
    if ((theme.palette.mode === 'dark') !== darkMode) {
      colorMode.toggleColorMode();
    }
    // eslint-disable-next-line
  }, [darkMode]);

  const handleSave = async () => {
    setSaving(true);
    setSaveStatus(null);
    try {
      const res = await fetch('/api/v1/feed/preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          categories: selectedCategories,
          languages: [language],
          notifications,
          theme: darkMode ? 'dark' : 'light',
        }),
      });
      if (res.ok) {
        setSaveStatus('Preferences saved!');
      } else {
        setSaveStatus('Failed to save preferences');
      }
    } catch {
      setSaveStatus('Network error');
    }
    setSaving(false);
  };

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: 'background.default', fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2, width: '100%' }}>
          <Typography variant="h4" sx={{ color: 'primary.main', fontWeight: 900, letterSpacing: 2, fontSize: 32, flex: 1, borderBottom: '2px solid', borderColor: 'divider', pb: 1, textAlign: 'center' }}>
            SETTINGS
          </Typography>
          <Chip label={darkMode ? 'tmux (dark)' : 'tmux (light)'} sx={{ bgcolor: 'background.paper', color: 'primary.main', fontWeight: 700, fontSize: 18 }} />
        </Box>
        <Divider sx={{ mb: 3, bgcolor: 'divider' }} />
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(auto-fit, minmax(320px, 1fr))' }, gap: { xs: 2, sm: 3 }, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto', alignItems: 'stretch' }}>
        <Paper sx={{ bgcolor: 'background.paper', color: 'text.primary', p: { xs: 2, sm: 3 }, boxShadow: '0 2px 12px #000a', border: '2px solid', borderColor: 'primary.main', borderRadius: 2, minHeight: 180, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
          <Typography variant="h6" sx={{ color: 'primary.main', fontWeight: 900, mb: 2, fontSize: 22, borderBottom: '1px solid', borderColor: 'divider', pb: 1, letterSpacing: 1 }}>
            News Categories
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {categories.map(cat => (
              <Chip
                key={cat}
                label={cat}
                color={selectedCategories.includes(cat) ? 'warning' : 'default'}
                sx={{ fontWeight: 700, fontSize: 16, bgcolor: selectedCategories.includes(cat) ? 'primary.main' : 'background.paper', color: selectedCategories.includes(cat) ? 'background.default' : 'text.primary', mb: 1, border: '1px solid', borderColor: 'divider' }}
                onClick={() => setSelectedCategories(selectedCategories.includes(cat)
                  ? selectedCategories.filter(c => c !== cat)
                  : [...selectedCategories, cat])}
              />
            ))}
          </Box>
        </Paper>
        <Paper sx={{ bgcolor: 'background.paper', color: 'text.primary', p: 3, boxShadow: '0 2px 12px #000a', border: '2px solid', borderColor: 'primary.main', borderRadius: 1, minHeight: 180 }}>
          <Typography variant="h6" sx={{ color: 'primary.main', fontWeight: 900, mb: 2, fontSize: 22, borderBottom: '1px solid', borderColor: 'divider', pb: 1, letterSpacing: 1 }}>
            Language
          </Typography>
          <Select
            value={language}
            onChange={e => setLanguage(e.target.value)}
            sx={{ color: 'text.primary', bgcolor: 'background.paper', fontWeight: 700, fontSize: 18, minWidth: 120, border: '1px solid', borderColor: 'divider' }}
          >
            {languages.map(lang => (
              <MenuItem key={lang} value={lang} sx={{ fontWeight: 700, fontSize: 18 }}>{lang.toUpperCase()}</MenuItem>
            ))}
          </Select>
        </Paper>
        <Paper sx={{ bgcolor: 'background.paper', color: 'text.primary', p: 3, boxShadow: '0 2px 12px #000a', border: '2px solid', borderColor: 'primary.main', borderRadius: 1, minHeight: 180 }}>
          <Typography variant="h6" sx={{ color: 'primary.main', fontWeight: 900, mb: 2, fontSize: 22, borderBottom: '1px solid', borderColor: 'divider', pb: 1, letterSpacing: 1 }}>
            Notifications
          </Typography>
          <FormControlLabel
            control={<Switch checked={notifications} onChange={() => setNotifications(!notifications)} sx={{ color: 'primary.main' }} />}
            label={<span style={{ color: theme.palette.text.primary, fontWeight: 700 }}>Enable Notifications</span>}
          />
        </Paper>
        <Paper sx={{ bgcolor: 'background.paper', color: 'text.primary', p: 3, boxShadow: '0 2px 12px #000a', border: '2px solid', borderColor: 'primary.main', borderRadius: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <Typography variant="h6" sx={{ color: 'primary.main', fontWeight: 900, mb: 2, fontSize: 22, borderBottom: '1px solid', borderColor: 'divider', pb: 1, letterSpacing: 1, textAlign: 'center' }}>
            Theme
          </Typography>
          <FormControlLabel
            control={<Switch checked={darkMode} onChange={() => setDarkMode((prev) => !prev)} sx={{ color: 'primary.main' }} />}
            label={<span style={{ color: theme.palette.text.primary, fontWeight: 700 }}>{darkMode ? 'Dark Mode' : 'Light Mode'}</span>}
          />
        </Paper>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mt: 4, gap: 2 }}>
        <button
          onClick={handleSave}
          disabled={saving}
          style={{
            background: theme.palette.primary.main,
            color: theme.palette.background.default,
            fontWeight: 900,
            fontSize: 18,
            padding: '12px 32px',
            border: 'none',
            borderRadius: '6px',
            boxShadow: '0 2px 8px #000a',
            cursor: saving ? 'not-allowed' : 'pointer',
          }}
        >
          {saving ? 'Saving...' : 'Save Preferences'}
        </button>
        {saveStatus && (
          <Typography variant="body1" sx={{ color: saveStatus === 'Preferences saved!' ? 'primary.main' : '#ff1744', fontWeight: 900, fontSize: 18, ml: 2 }}>
            {saveStatus}
          </Typography>
        )}
      </Box>
    </Box>
  );
}
