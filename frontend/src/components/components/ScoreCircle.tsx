import React, { useEffect, useState, useRef } from "react";

interface ScoreCircleProps {
  score: number;
  size?: "sm" | "md" | "lg";
}

export const ScoreCircle: React.FC<ScoreCircleProps> = ({
  score,
  size = "md",
}) => {
  const [displayScore, setDisplayScore] = useState(score);
  const animationRef = useRef<number>();
  const previousScore = useRef(score);

  useEffect(() => {
    // Cancel any existing animation
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    const startTime = performance.now();
    const duration = 600; // Animation duration in milliseconds
    const startValue = previousScore.current;
    const endValue = Math.min(100, Math.max(0, score));
    const changeInValue = endValue - startValue;

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function (ease-out cubic)
      const eased = 1 - Math.pow(1 - progress, 3);

      const currentValue = startValue + changeInValue * eased;
      setDisplayScore(currentValue);

      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate);
      }
    };

    animationRef.current = requestAnimationFrame(animate);
    previousScore.current = endValue;

    // Cleanup
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [score]);

  // Determine color based on score
  const getColor = (score: number) => {
    if (score >= 80) return "su";
    if (score >= 50) return "wa";
    return "er";
  };

  const sizeConfig = {
    sm: {
      circle: "w-24 h-24",
      text: "text-2xl",
    },
    md: {
      circle: "w-32 h-32",
      text: "text-3xl",
    },
    lg: {
      circle: "w-40 h-40",
      text: "text-4xl",
    },
  };

  const color = getColor(displayScore);

  return (
    <div
      className={`relative ${sizeConfig[size].circle} rounded-full flex items-center justify-center`}
      style={{
        background: `conic-gradient(
          oklch(var(--${color})) ${displayScore}%,
          oklch(var(--b3)) ${displayScore}%
        )`,
        boxShadow: "0 0 10px rgba(0,0,0,0.1)",
      }}
    >
      <div
        className={`
          absolute
          bg-base-100
          rounded-full
          flex
          items-center
          justify-center
          ${sizeConfig[size].circle}
          transform
          scale-[0.85]
        `}
      >
        <span
          className={`
            font-bold
            ${sizeConfig[size].text}
          `}
          style={{ color: `oklch(var(--${color}))` }}
        >
          {Math.round(displayScore)}
        </span>
      </div>
    </div>
  );
};
