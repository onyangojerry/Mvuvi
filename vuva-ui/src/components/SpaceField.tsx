import React, { useEffect, useRef } from 'react';

interface Star {
  x: number;
  y: number;
  size: number;
  opacity: number;
  speed: number;
}

export function SpaceField() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const starsRef = useRef<Star[]>([]);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize stars
    const starCount = 200;
    starsRef.current = Array.from({ length: starCount }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.5 + 0.3,
      speed: Math.random() * 0.3 + 0.1
    }));

    // Animation loop
    const animate = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      starsRef.current.forEach(star => {
        // Twinkle effect
        star.opacity += (Math.random() - 0.5) * 0.02;
        star.opacity = Math.max(0.2, Math.min(0.8, star.opacity));

        // Draw star
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
        ctx.fill();

        // Gentle drift
        star.x += Math.sin(Date.now() * 0.0001 + star.y) * star.speed * 0.2;
        star.y += star.speed * 0.1;

        // Wrap around
        if (star.y > canvas.height) {
          star.y = 0;
          star.x = Math.random() * canvas.width;
        }
        if (star.x > canvas.width) star.x = 0;
        if (star.x < 0) star.x = canvas.width;
      });

      // Add nebula effect
      const gradient = ctx.createRadialGradient(
        canvas.width * 0.3,
        canvas.height * 0.3,
        0,
        canvas.width * 0.3,
        canvas.height * 0.3,
        canvas.width * 0.5
      );
      gradient.addColorStop(0, 'rgba(79, 70, 229, 0.03)');
      gradient.addColorStop(0.5, 'rgba(124, 58, 237, 0.02)');
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full"
      style={{ background: 'radial-gradient(ellipse at center, #0a0a1a 0%, #000000 100%)' }}
    />
  );
}
