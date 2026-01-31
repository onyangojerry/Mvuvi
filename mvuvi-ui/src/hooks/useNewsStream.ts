import { useEffect } from 'react';

export function useNewsStream(onNewArticle: (article: any) => void) {
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001/api/v1/feed/stream');

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'new_article') {
          onNewArticle(message.article);
        }
      } catch (e) {
        // Ignore malformed messages
      }
    };

    ws.onerror = (error) => {
      // Optionally handle errors
      // console.error('WebSocket error:', error);
    };

    return () => ws.close();
  }, [onNewArticle]);
}
