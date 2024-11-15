import React from "react";

interface ScoreCircleProps {
  score: number;
  size?: "sm" | "md" | "lg";
}

export const ScoreCircle: React.FC<ScoreCircleProps> = ({
  score,
  size = "md",
}) => {
  // Ensure score is between 0 and 100
  const validScore = Math.min(100, Math.max(0, score));

  // Determine color based on score
  const getColor = (score: number) => {
    if (score >= 80) return "#22c55e"; // green
    if (score >= 50) return "#eab308"; // yellow
    return "#ef4444"; // red
  };

  // Size configurations
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

  const color = getColor(validScore);

  return (
    <div
      className={`relative ${sizeConfig[size].circle} rounded-full flex items-center justify-center`}
      style={{
        background: `conic-gradient(
          ${color} ${validScore}%,
          #e5e7eb ${validScore}%
        )`,
        boxShadow: "0 0 10px rgba(0,0,0,0.1)",
      }}
    >
      <div
        className={`
          absolute
          bg-white
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
          style={{ color }}
        >
          {Math.round(validScore)}
        </span>
      </div>
    </div>
  );
};
