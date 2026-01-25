import React from 'react';
import { motion } from 'motion/react';
import { Rocket } from 'lucide-react';

interface SpaceshipProps {
  position: { x: number; y: number };
  viewMode: string;
}

export function Spaceship({ position, viewMode }: SpaceshipProps) {
  const getScale = () => {
    switch (viewMode) {
      case 'space':
        return 1;
      case 'galaxy':
        return 0.6;
      case 'solar-system':
        return 0.4;
      case 'planet':
        return 0;
      default:
        return 1;
    }
  };

  return (
    <motion.div
      className="fixed pointer-events-none z-50"
      style={{
        left: `${position.x}%`,
        top: `${position.y}%`,
        transform: 'translate(-50%, -50%)'
      }}
      initial={{ scale: 1, opacity: 1 }}
      animate={{ 
        scale: getScale(), 
        opacity: viewMode === 'planet' ? 0 : 1,
        rotate: viewMode === 'space' ? 0 : 360
      }}
      transition={{ 
        duration: 1, 
        ease: 'easeInOut',
        rotate: { duration: 2, ease: 'easeInOut' }
      }}
    >
      <div className="relative">
        {/* Engine glow */}
        <motion.div
          className="absolute -bottom-6 left-1/2 -translate-x-1/2 w-2 h-8 bg-gradient-to-b from-cyan-400 to-transparent rounded-full blur-sm"
          animate={{
            opacity: [0.6, 1, 0.6],
            height: [24, 32, 24]
          }}
          transition={{
            duration: 0.5,
            repeat: Infinity,
            ease: 'easeInOut'
          }}
        />
        
        {/* Spaceship */}
        <div className="relative">
          <Rocket className="w-8 h-8 text-cyan-400 drop-shadow-[0_0_10px_rgba(34,211,238,0.8)]" />
          
          {/* Cockpit glow */}
          <motion.div
            className="absolute top-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-yellow-300 rounded-full blur-[2px]"
            animate={{
              opacity: [0.8, 1, 0.8]
            }}
            transition={{
              duration: 1,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
          />
        </div>
      </div>
    </motion.div>
  );
}
