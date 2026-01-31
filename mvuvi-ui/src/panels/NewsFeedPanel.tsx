import { useEffect, useState, useContext } from 'react';
import { Box, Typography, Divider, Paper, Chip, CircularProgress, Alert, useTheme } from '@mui/material';
import { ColorModeContext } from '../App';
import { useNewsStream } from '../hooks/useNewsStream';

type Article = {
  id: string;
  title: string;
  summary?: string;
  content?: string;
  source: string;
  category?: string;
  published_at: string;
  url?: string;
};

export default function NewsFeedPanel() {
  const theme = useTheme();
  // const colorMode = useContext(ColorModeContext);
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/v1/feed?page=1&page_size=20');
        const data = await res.json();
        if (res.ok && data.status === 'success' && Array.isArray(data.data)) {
          setArticles(data.data);
        } else {
          setError('Failed to fetch news feed');
        }
      } catch (err: any) {
        setError('Network error');
      }
      setLoading(false);
    };
    fetchNews();
  }, []);

  // Real-time news updates
  useNewsStream((article: Article) => {
    setArticles((prev) => [article, ...prev]);
  });

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: theme.palette.background.default, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Typography variant="h4" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 3, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 32, textAlign: 'center' }}>
          NEWS FEED
        </Typography>
        <Divider sx={{ mb: 3, bgcolor: theme.palette.background.paper }} />
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: { xs: '1fr' }, gap: { xs: 2, sm: 3 }, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto', alignItems: 'stretch' }}>
        {loading && <CircularProgress sx={{ color: theme.palette.primary.main, mx: 'auto', display: 'block', mt: 4 }} />}
        {error && <Alert severity="error" sx={{ mb: 3, fontWeight: 700 }}>{error}</Alert>}
        {articles.length === 0 && !loading && !error && (
          <Typography variant="body1" sx={{ color: theme.palette.text.secondary, fontWeight: 700, fontSize: 20, textAlign: 'center', mt: 4 }}>
            No news articles found.
          </Typography>
        )}
        {articles.map((news, idx) => (
          <Paper key={news.id || idx} sx={{ bgcolor: theme.palette.background.paper, color: theme.palette.text.primary, p: { xs: 2, sm: 3 }, boxShadow: '0 2px 12px #000a', border: `2px solid ${theme.palette.primary.main}`, borderRadius: 2, width: '100%', fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Typography variant="h5" sx={{ color: theme.palette.primary.main, fontWeight: 900, fontSize: 24, flex: 1, textAlign: 'center' }}>{news.title}</Typography>
              <Chip label={news.source} sx={{ bgcolor: theme.palette.background.default, color: theme.palette.primary.main, fontWeight: 700, fontSize: 16, ml: 2 }} />
            </Box>
            <Typography variant="body2" sx={{ color: theme.palette.text.secondary, fontWeight: 700, fontSize: 16, mb: 2 }}>
              {news.published_at}
            </Typography>
            <Typography variant="body1" sx={{ fontSize: 18, color: theme.palette.text.primary, fontWeight: 700 }}>
              {news.summary || news.content || ''}
            </Typography>
            {news.url && (
              <Typography variant="body2" sx={{ color: theme.palette.primary.main, fontWeight: 700, mt: 1 }}>
                <a href={news.url} target="_blank" rel="noopener noreferrer" style={{ color: theme.palette.primary.main, textDecoration: 'underline', fontWeight: 700 }}>
                  Read more
                </a>
              </Typography>
            )}
          </Paper>
        ))}
      </Box>
    </Box>
  );
}
