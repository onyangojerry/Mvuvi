import React from 'react';
import { motion } from 'motion/react';
import { ChevronLeft, Clock, ExternalLink } from 'lucide-react';
import { newsData } from '../data/newsData';

interface NewsPanelProps {
  planet: string;
  galaxyId: string;
  solarSystemId: string;
  onBack: () => void;
}

export function NewsPanel({ planet, galaxyId, solarSystemId, onBack }: NewsPanelProps) {
  const galaxy = newsData.find(g => g.id === galaxyId);
  const solarSystem = galaxy?.solarSystems.find(s => s.id === solarSystemId);
  const planetData = solarSystem?.planets.find(p => p.id === planet);

  if (!planetData || !galaxy || !solarSystem) return null;

  return (
    <motion.div
      className="absolute inset-0 flex items-center justify-center p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {/* Background blur effect */}
      <div className="absolute inset-0 backdrop-blur-md bg-black/40" />

      {/* News panel */}
      <motion.div
        className="relative max-w-4xl w-full max-h-[85vh] overflow-y-auto bg-gradient-to-br from-gray-900/95 to-black/95 rounded-2xl border border-white/10 shadow-2xl"
        initial={{ scale: 0.8, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        transition={{ type: 'spring', damping: 20 }}
      >
        {/* Header */}
        <div 
          className="sticky top-0 z-10 px-8 py-6 border-b border-white/10 backdrop-blur-lg"
          style={{
            background: `linear-gradient(135deg, ${planetData.color}20, transparent)`
          }}
        >
          <div className="flex items-start justify-between">
            <div>
              {/* Breadcrumb */}
              <div className="flex items-center gap-2 text-sm text-white/50 mb-3">
                <span>{galaxy.name}</span>
                <span>/</span>
                <span>{solarSystem.name}</span>
                <span>/</span>
                <span className="text-white/80">{planetData.name}</span>
              </div>

              <div className="flex items-center gap-4">
                {/* Planet icon */}
                <div 
                  className="w-16 h-16 rounded-full flex-shrink-0"
                  style={{
                    background: `linear-gradient(135deg, ${planetData.color}, ${planetData.color}99)`,
                    boxShadow: `0 0 30px ${planetData.color}80, inset -5px -5px 10px rgba(0,0,0,0.3)`
                  }}
                />

                <div>
                  <h2 className="text-3xl font-medium text-white">{planetData.name}</h2>
                  <p className="text-white/60 mt-1">
                    {planetData.articles.length} {planetData.articles.length === 1 ? 'article' : 'articles'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Articles */}
        <div className="p-8 space-y-6">
          {planetData.articles.map((article, index) => (
            <motion.article
              key={article.id}
              className="group relative p-6 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all duration-300"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Article accent line */}
              <div 
                className="absolute left-0 top-6 bottom-6 w-1 rounded-full"
                style={{ backgroundColor: planetData.color }}
              />

              <div className="pl-4">
                {/* Metadata */}
                <div className="flex items-center gap-4 text-sm text-white/50 mb-3">
                  <div className="flex items-center gap-1.5">
                    <Clock className="w-4 h-4" />
                    <span>{article.timestamp}</span>
                  </div>
                  <span>•</span>
                  <span>{article.source}</span>
                </div>

                {/* Title */}
                <h3 className="text-xl font-medium text-white mb-3 group-hover:text-cyan-300 transition-colors">
                  {article.title}
                </h3>

                {/* Summary */}
                <p className="text-white/70 leading-relaxed mb-4">
                  {article.summary}
                </p>

                {/* Read more link */}
                <button className="inline-flex items-center gap-2 text-sm text-cyan-400 hover:text-cyan-300 transition-colors">
                  <span>Read full article</span>
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>

              {/* Hover glow effect */}
              <div 
                className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                style={{
                  background: `radial-gradient(circle at center, ${planetData.color}10, transparent)`,
                }}
              />
            </motion.article>
          ))}
        </div>

        {/* Real-time indicator */}
        <motion.div
          className="sticky bottom-0 px-8 py-4 border-t border-white/10 backdrop-blur-lg bg-black/60"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="flex items-center justify-center gap-2">
            <motion.div
              className="w-2 h-2 rounded-full bg-green-400"
              animate={{
                opacity: [1, 0.5, 1],
                scale: [1, 1.2, 1]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut'
              }}
            />
            <span className="text-sm text-white/60">Live news feed • Updates in real-time</span>
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
