import React from 'react';
import { motion } from 'motion/react';
import { ChevronLeft, Home, Compass } from 'lucide-react';

interface NavigationProps {
  viewMode: string;
  selectedGalaxy: string | null;
  selectedSolarSystem: string | null;
  selectedPlanet: string | null;
  onBackToSpace: () => void;
  onBackToGalaxy: () => void;
  onBackToSolarSystem: () => void;
}

export function Navigation({
  viewMode,
  selectedGalaxy,
  selectedSolarSystem,
  selectedPlanet,
  onBackToSpace,
  onBackToGalaxy,
  onBackToSolarSystem
}: NavigationProps) {
  return (
    <div className="absolute top-8 left-8 z-50">
      <motion.div
        className="flex flex-col gap-3"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.3 }}
      >
        {/* Back to Space button */}
        {viewMode !== 'space' && (
          <motion.button
            onClick={onBackToSpace}
            className="flex items-center gap-2 px-4 py-2.5 bg-black/60 backdrop-blur-md rounded-lg border border-cyan-400/30 hover:bg-cyan-400/20 hover:border-cyan-400/50 transition-all group"
            whileHover={{ scale: 1.05, x: -5 }}
            whileTap={{ scale: 0.95 }}
          >
            <Home className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-medium text-cyan-300">Back to Space</span>
          </motion.button>
        )}

        {/* Back to Galaxy button */}
        {(viewMode === 'solar-system' || viewMode === 'planet') && selectedSolarSystem && (
          <motion.button
            onClick={onBackToGalaxy}
            className="flex items-center gap-2 px-4 py-2.5 bg-black/60 backdrop-blur-md rounded-lg border border-white/20 hover:bg-white/10 hover:border-white/30 transition-all group"
            whileHover={{ scale: 1.05, x: -5 }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <ChevronLeft className="w-4 h-4 text-white/80 group-hover:text-white" />
            <span className="text-sm font-medium text-white/80 group-hover:text-white">
              Back to Galaxy
            </span>
          </motion.button>
        )}

        {/* Back to Solar System button */}
        {viewMode === 'planet' && selectedPlanet && (
          <motion.button
            onClick={onBackToSolarSystem}
            className="flex items-center gap-2 px-4 py-2.5 bg-black/60 backdrop-blur-md rounded-lg border border-white/20 hover:bg-white/10 hover:border-white/30 transition-all group"
            whileHover={{ scale: 1.05, x: -5 }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <ChevronLeft className="w-4 h-4 text-white/80 group-hover:text-white" />
            <span className="text-sm font-medium text-white/80 group-hover:text-white">
              Back to Solar System
            </span>
          </motion.button>
        )}

        {/* View indicator */}
        {viewMode === 'space' && (
          <motion.div
            className="flex items-center gap-2 px-4 py-2.5 bg-black/40 backdrop-blur-md rounded-lg border border-white/10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <Compass className="w-4 h-4 text-cyan-400" />
            <span className="text-sm text-white/70">Galaxy Map View</span>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
