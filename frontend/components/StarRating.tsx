"use client";

interface StarRatingProps {
  stars: number; // 0-3
  size?: "sm" | "md" | "lg";
  animate?: boolean;
}

const SIZES = {
  sm: "text-sm",
  md: "text-xl",
  lg: "text-3xl",
};

export default function StarRating({ stars, size = "md", animate = false }: StarRatingProps) {
  return (
    <div className={`flex gap-0.5 ${SIZES[size]}`}>
      {[1, 2, 3].map((i) => (
        <span
          key={i}
          className={`transition-all duration-300 ${
            animate ? "animate-star-pop" : ""
          } ${i <= stars ? "text-star" : "text-border"}`}
          style={animate ? { animationDelay: `${(i - 1) * 100}ms` } : {}}
        >
          ★
        </span>
      ))}
    </div>
  );
}
