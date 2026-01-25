import React, { useState } from 'react';
import { motion } from 'motion/react';
import { Galaxy, SolarSystem } from '../data/newsData';
import { ChevronLeft, Circle } from 'lucide-react';

interface SolarSystemViewProps {
  galaxy: Galaxy;
  selectedSystem?: string;
  onSelectSolarSystem?: (systemId: string) => void;
  onSelectPlanet?: (planetId: string) => void;
  onBack: () => void;
}

export function SolarSystemView({ 
  galaxy, 
  selectedSystem, 
  onSelectSolarSystem, 
  onSelectPlanet,
  onBack 
}: SolarSystemViewProps) {
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);

  // If a solar system is selected, show its planets
  if (selectedSystem) {
    const solarSystem = galaxy.solarSystems.find(s => s.id === selectedSystem);
    if (!solarSystem) return null;

    return (
      <div className="absolute inset-0 flex items-center justify-center">
        {/* Central star (sun) */}
        <motion.div
          className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.8, type: 'spring' }}
        >
          <div className="relative w-24 h-24">
            {/* Sun glow */}
            <motion.div
              className="absolute inset-0 rounded-full blur-2xl"
              style={{
                background: `radial-gradient(circle, ${solarSystem.color}, transparent)`
              }}
              animate={{
                scale: [1, 1.3, 1],
                opacity: [0.8, 1, 0.8]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut'
              }}
            />
            <div 
              className="absolute inset-2 rounded-full"
              style={{ backgroundColor: solarSystem.color }}
            />
          </div>
        </motion.div>

        {/* Planets orbiting */}
        {solarSystem.planets.map((planet, index) => {
          const orbitRadius = 150 + index * 100;
          const isHovered = hoveredItem === planet.id;

          return (
            <motion.div
              key={planet.id}
              className="absolute left-1/2 top-1/2"
              style={{
                width: orbitRadius * 2,
                height: orbitRadius * 2,
                marginLeft: -orbitRadius,
                marginTop: -orbitRadius
              }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: index * 0.2 }}
            >
              {/* Orbit path */}
              <div 
                className="absolute inset-0 rounded-full border border-white/10"
                style={{
                  borderStyle: 'dashed'
                }}
              />

              {/* Planet */}
              <motion.div
                className="absolute cursor-pointer"
                style={{
                  left: '50%',
                  top: 0,
                  marginLeft: -planet.size / 2,
                  marginTop: -planet.size / 2
                }}
                animate={{
                  rotate: 360
                }}
                transition={{
                  duration: 10 + index * 5,
                  repeat: Infinity,
                  ease: 'linear'
                }}
                whileHover={{ scale: 1.3 }}
                onClick={() => onSelectPlanet?.(planet.id)}
                onHoverStart={() => setHoveredItem(planet.id)}
                onHoverEnd={() => setHoveredItem(null)}
              >
                <div className="relative">
                  {/* Planet glow */}
                  <motion.div
                    className="absolute inset-0 rounded-full blur-md"
                    style={{
                      backgroundColor: planet.color,
                      width: planet.size,
                      height: planet.size
                    }}
                    animate={{
                      opacity: isHovered ? 1 : 0.6
                    }}
                  />
                  
                  {/* Planet surface */}
                  <div
                    className="relative rounded-full"
                    style={{
                      width: planet.size,
                      height: planet.size,
                      background: `linear-gradient(135deg, ${planet.color}, ${planet.color}99)`,
                      boxShadow: `inset -5px -5px 10px rgba(0,0,0,0.3), 0 0 20px ${planet.color}80`
                    }}
                  >
                    {/* Surface details */}
                    <div 
                      className="absolute inset-0 rounded-full opacity-30"
                      style={{
                        background: 'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), transparent)'
                      }}
                    />
                  </div>

                  {/* Planet label */}
                  {isHovered && (
                    <motion.div
                      className="absolute top-full mt-2 left-1/2 -translate-x-1/2 whitespace-nowrap z-10"
                      initial={{ opacity: 0, y: -5 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <div className="px-3 py-2 bg-black/80 backdrop-blur-sm rounded-lg border border-white/30">
                        <p className="text-xs font-medium text-white">{planet.name}</p>
                        <p className="text-[10px] text-white/60 mt-0.5">
                          {planet.articles.length} articles
                        </p>
                      </div>
                    </motion.div>
                  )}

                  {/* Ring effect for some planets */}
                  {index % 3 === 0 && (
                    <div
                      className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 border-2 rounded-full opacity-30"
                      style={{
                        width: planet.size * 1.8,
                        height: planet.size * 0.4,
                        borderColor: planet.color,
                        transform: 'translateX(-50%) translateY(-50%) rotateX(75deg)'
                      }}
                    />
                  )}
                </div>
              </motion.div>
            </motion.div>
          );
        })}

        {/* System name */}
        <motion.div
          className="absolute top-8 left-1/2 -translate-x-1/2"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="px-6 py-3 bg-black/60 backdrop-blur-sm rounded-lg border border-white/20">
            <p className="text-xl font-medium text-white">{solarSystem.name}</p>
            <p className="text-sm text-white/60 mt-1">
              {solarSystem.planets.length} Planets
            </p>
          </div>
        </motion.div>

        {/* Instructions */}
        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="px-6 py-3 bg-black/40 backdrop-blur-md rounded-full border border-cyan-400/30">
            <p className="text-cyan-300 text-sm">Click a planet to view news articles</p>
          </div>
        </motion.div>
      </div>
    );
  }

  // Show solar systems for selection
  return (
    <div className="absolute inset-0 flex items-center justify-center">
      {/* Central galaxy representation */}
      <motion.div
        className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
        initial={{ scale: 0 }}
        animate={{ scale: 1, rotate: 360 }}
        transition={{ 
          scale: { duration: 0.8 },
          rotate: { duration: 30, repeat: Infinity, ease: 'linear' }
        }}
      >
        <div 
          className="w-32 h-32 rounded-full blur-xl"
          style={{
            background: `radial-gradient(circle, ${galaxy.gradient[0]}, ${galaxy.gradient[1]}, transparent)`
          }}
        />
      </motion.div>

      {/* Solar systems */}
      {galaxy.solarSystems.map((system, index) => {
        const orbitRadius = 200 + index * 120;
        const isHovered = hoveredItem === system.id;
        
        return (
          <motion.div
            key={system.id}
            className="absolute left-1/2 top-1/2"
            style={{
              width: orbitRadius * 2,
              height: orbitRadius * 2,
              marginLeft: -orbitRadius,
              marginTop: -orbitRadius
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.15 }}
          >
            {/* Orbit line */}
            <div className="absolute inset-0 rounded-full border border-white/5" />

            {/* Solar system node */}
            <motion.div
              className="absolute cursor-pointer"
              style={{
                left: '50%',
                top: 0,
                marginLeft: -30,
                marginTop: -30
              }}
              animate={{
                rotate: 360
              }}
              transition={{
                duration: 15 + index * 5,
                repeat: Infinity,
                ease: 'linear'
              }}
              whileHover={{ scale: 1.2 }}
              onClick={() => onSelectSolarSystem?.(system.id)}
              onHoverStart={() => setHoveredItem(system.id)}
              onHoverEnd={() => setHoveredItem(null)}
            >
              <div className="relative w-16 h-16">
                {/* Glow */}
                <motion.div
                  className="absolute inset-0 rounded-full blur-lg"
                  style={{ backgroundColor: system.color }}
                  animate={{
                    opacity: isHovered ? 1 : 0.6,
                    scale: isHovered ? 1.2 : 1
                  }}
                />
                
                {/* Core */}
                <div 
                  className="absolute inset-2 rounded-full"
                  style={{ backgroundColor: system.color }}
                />

                {/* Mini planets orbiting */}
                {Array.from({ length: 3 }).map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-2 h-2 rounded-full bg-white/60"
                    style={{
                      left: '50%',
                      top: '50%',
                      marginLeft: -4,
                      marginTop: -4
                    }}
                    animate={{
                      x: Math.cos((i / 3) * Math.PI * 2) * 25,
                      y: Math.sin((i / 3) * Math.PI * 2) * 25,
                      rotate: 360
                    }}
                    transition={{
                      duration: 2 + i,
                      repeat: Infinity,
                      ease: 'linear'
                    }}
                  />
                ))}

                {/* Label */}
                {isHovered && (
                  <motion.div
                    className="absolute top-full mt-3 left-1/2 -translate-x-1/2 whitespace-nowrap z-10"
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    <div className="px-3 py-2 bg-black/80 backdrop-blur-sm rounded-lg border border-white/30">
                      <p className="text-sm font-medium text-white">{system.name}</p>
                      <p className="text-xs text-white/60 mt-1">
                        {system.planets.length} planets
                      </p>
                    </div>
                  </motion.div>
                )}
              </div>
            </motion.div>
          </motion.div>
        );
      })}

      {/* Galaxy name */}
      <motion.div
        className="absolute top-8 left-1/2 -translate-x-1/2"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="px-6 py-3 bg-black/60 backdrop-blur-sm rounded-lg border border-white/20">
          <p className="text-2xl font-medium text-white">{galaxy.name}</p>
          <p className="text-sm text-white/60 mt-1 text-center">
            {galaxy.solarSystems.length} Solar Systems
          </p>
        </div>
      </motion.div>

      {/* Instructions */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="px-6 py-3 bg-black/40 backdrop-blur-md rounded-full border border-cyan-400/30">
          <p className="text-cyan-300 text-sm">Select a solar system to explore subtopics</p>
        </div>
      </motion.div>
    </div>
  );
}
