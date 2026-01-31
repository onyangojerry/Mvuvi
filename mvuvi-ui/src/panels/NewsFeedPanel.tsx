import { useEffect, useState } from 'react';
import { Box, Typography, Divider, Paper, Chip, CircularProgress, Alert, useTheme } from '@mui/material';

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
  // Categories (can be extended or fetched from backend)
  const categories = ['All', 'Technology', 'World', 'Business', 'Science', 'General'];
  // Persist articles and selected categories in localStorage
  const [articles, setArticles] = useState<Article[]>(() => {
    const stored = localStorage.getItem('news-articles');
    return stored ? JSON.parse(stored) : [];
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(() => {
    const stored = localStorage.getItem('selected-categories');
    return stored ? JSON.parse(stored) : ['All'];
  });

  // Optionally fetch user preferences for default category (not required for this logic)

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/v1/feed?page=1&page_size=50');
        const data = await res.json();
        if (res.ok && data.status === 'success' && Array.isArray(data.data)) {
          setArticles(data.data);
          localStorage.setItem('news-articles', JSON.stringify(data.data));
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

  // Real-time news updates (stream all, filter in render)
  useNewsStream((article: Article) => {
    setArticles((prev) => {
      const updated = [article, ...prev];
      localStorage.setItem('news-articles', JSON.stringify(updated));
      return updated;
    });
  });

  // Filter articles by selected categories
  const showAll = selectedCategories.includes('All');
  const filteredArticles = showAll
    ? articles
    : articles.filter(a => a.category && selectedCategories.includes(a.category));

  return (
    <Box sx={{ p: 0, minHeight: '100vh', height: '100vh', bgcolor: theme.palette.background.default, fontFamily: 'Roboto Mono, monospace', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', px: { xs: 2, sm: 4 }, pt: { xs: 2, sm: 4 } }}>
        <Typography variant="h4" sx={{ color: theme.palette.primary.main, fontWeight: 900, mb: 3, letterSpacing: 2, fontFamily: 'Roboto Mono, monospace', fontSize: 32, textAlign: 'center' }}>
          NEWS FEED
        </Typography>
        <Divider sx={{ mb: 3, bgcolor: theme.palette.background.paper }} />
        {/* Category buttons */}
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', justifyContent: 'center', mb: 2 }}>
          {categories.map(cat => {
            const selected = selectedCategories.includes(cat);
            return (
              <Chip
                key={cat}
                label={cat}
                color={selected ? 'warning' : 'default'}
                sx={{ fontWeight: 700, fontSize: 16, bgcolor: selected ? 'primary.main' : 'background.paper', color: selected ? 'background.default' : 'text.primary', mb: 1, border: '1px solid', borderColor: 'divider', cursor: 'pointer' }}
                onClick={() => {
                  let updated;
                  if (cat === 'All') {
                    // Selecting 'All' deselects others, deselecting 'All' leaves none selected
                    updated = selected ? [] : ['All'];
                  } else {
                    if (selected) {
                      // Remove category
                      updated = selectedCategories.filter(c => c !== cat && c !== 'All');
                      if (updated.length === 0) updated = ['All'];
                    } else {
                      // Add category, remove 'All' if present
                      updated = selectedCategories.filter(c => c !== 'All');
                      updated.push(cat);
                    }
                  }
                  setSelectedCategories(updated);
                  localStorage.setItem('selected-categories', JSON.stringify(updated));
                }}
              />
            );
          })}
        </Box>
      </Box>
      <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: { xs: '1fr' }, gap: { xs: 2, sm: 3 }, px: { xs: 2, sm: 4 }, pb: { xs: 2, sm: 4 }, overflowY: 'auto', alignItems: 'stretch' }}>
        {loading && <CircularProgress sx={{ color: theme.palette.primary.main, mx: 'auto', display: 'block', mt: 4 }} />}
        {error && <Alert severity="error" sx={{ mb: 3, fontWeight: 700 }}>{error}</Alert>}
        {filteredArticles.length === 0 && !loading && !error && (
          <Typography variant="body1" sx={{ color: theme.palette.text.secondary, fontWeight: 700, fontSize: 20, textAlign: 'center', mt: 4 }}>
            No news articles found.
          </Typography>
        )}
        {filteredArticles.map((news, idx) => (
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
