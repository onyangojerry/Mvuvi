import React, { useState } from 'react';
import { motion } from 'motion/react';
import { Galaxy } from '../data/newsData';
import { Sparkles } from 'lucide-react';

interface GalaxyViewProps {
  galaxies: Galaxy[];
  onSelectGalaxy: (galaxyId: string) => void;
  spaceshipPosition: { x: number; y: number };
}

export function GalaxyView({ galaxies, onSelectGalaxy, spaceshipPosition }: GalaxyViewProps) {
  const [hoveredGalaxy, setHoveredGalaxy] = useState<string | null>(null);

  const galaxyPositions = [
    { x: 25, y: 30 },
    { x: 70, y: 25 },
    { x: 50, y: 55 },
    { x: 20, y: 70 },
    { x: 75, y: 65 },
    { x: 45, y: 85 }
  ];

  return (
    <div className="absolute inset-0 flex items-center justify-center">
      {galaxies.map((galaxy, index) => {
        const position = galaxyPositions[index] || { x: 50, y: 50 };
        const isHovered = hoveredGalaxy === galaxy.id;

        return (
          <motion.div
            key={galaxy.id}
            className="absolute cursor-pointer"
            style={{
              left: `${position.x}%`,
              top: `${position.y}%`,
              transform: 'translate(-50%, -50%)'
            }}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: 1, 
              opacity: 1,
              rotate: isHovered ? 0 : 360
            }}
            transition={{ 
              delay: index * 0.2,
              scale: { duration: 0.6 },
              opacity: { duration: 0.6 },
              rotate: { duration: 20, repeat: Infinity, ease: 'linear' }
            }}
            whileHover={{ scale: 1.2 }}
            onClick={() => onSelectGalaxy(galaxy.id)}
            onHoverStart={() => setHoveredGalaxy(galaxy.id)}
            onHoverEnd={() => setHoveredGalaxy(null)}
          >
            {/* Galaxy core */}
            <div className="relative w-32 h-32">
              {/* Outer glow */}
              <motion.div
                className="absolute inset-0 rounded-full blur-xl"
                style={{
                  background: `radial-gradient(circle, ${galaxy.gradient[0]}80, ${galaxy.gradient[1]}40, transparent)`
                }}
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.6, 0.8, 0.6]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: 'easeInOut'
                }}
              />

              {/* Core glow */}
              <div 
                className="absolute inset-4 rounded-full blur-md"
                style={{
                  background: `radial-gradient(circle, ${galaxy.color}, transparent)`
                }}
              />

              {/* Stars in galaxy */}
              {Array.from({ length: 30 }).map((_, i) => {
                const angle = (i / 30) * Math.PI * 2;
                const radius = 20 + Math.random() * 35;
                const x = Math.cos(angle) * radius;
                const y = Math.sin(angle) * radius;

                return (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 rounded-full"
                    style={{
                      left: `calc(50% + ${x}px)`,
                      top: `calc(50% + ${y}px)`,
                      backgroundColor: galaxy.color,
                      boxShadow: `0 0 4px ${galaxy.color}`
                    }}
                    animate={{
                      opacity: [0.3, 0.8, 0.3],
                      scale: [0.8, 1.2, 0.8]
                    }}
                    transition={{
                      duration: 2 + Math.random() * 2,
                      repeat: Infinity,
                      delay: Math.random() * 2
                    }}
                  />
                );
              })}

              {/* Center icon */}
              <div className="absolute inset-0 flex items-center justify-center">
                <Sparkles 
                  className="w-8 h-8" 
                  style={{ color: galaxy.color }}
                />
              </div>
            </div>

            {/* Galaxy label */}
            <motion.div
              className="absolute top-full mt-4 left-1/2 -translate-x-1/2 whitespace-nowrap"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: isHovered ? 1 : 0.7, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="px-4 py-2 bg-black/60 backdrop-blur-sm rounded-lg border border-white/20">
                <p className="text-sm font-medium text-white">{galaxy.name}</p>
                <p className="text-xs text-white/60 mt-1">
                  {galaxy.solarSystems.length} Solar Systems
                </p>
              </div>
            </motion.div>

            {/* Particle trail effect when hovered */}
            {isHovered && (
              <motion.div
                className="absolute inset-0 rounded-full"
                style={{
                  border: `2px solid ${galaxy.color}40`
                }}
                initial={{ scale: 1, opacity: 0 }}
                animate={{ scale: 2, opacity: 0 }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: 'easeOut'
                }}
              />
            )}
          </motion.div>
        );
      })}

      {/* Instruction text */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.5 }}
      >
        <div className="px-6 py-3 bg-black/40 backdrop-blur-md rounded-full border border-cyan-400/30">
          <p className="text-cyan-300 text-sm">Click a galaxy to explore news categories</p>
        </div>
      </motion.div>
    </div>
  );
}
