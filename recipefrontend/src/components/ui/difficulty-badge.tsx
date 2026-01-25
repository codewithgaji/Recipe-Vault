import { cn } from "@/lib/utils";
import { Difficulty } from "@/types/recipe";

interface DifficultyBadgeProps {
  difficulty: Difficulty;
  className?: string;
}

const difficultyConfig: Record<Difficulty, { label: string; className: string }> = {
  easy: {
    label: "Easy",
    className: "bg-difficulty-easy/15 text-difficulty-easy border-difficulty-easy/30",
  },
  medium: {
    label: "Medium",
    className: "bg-difficulty-medium/15 text-difficulty-medium border-difficulty-medium/30",
  },
  hard: {
    label: "Hard",
    className: "bg-difficulty-hard/15 text-difficulty-hard border-difficulty-hard/30",
  },
};

export function DifficultyBadge({ difficulty, className }: DifficultyBadgeProps) {
  const config = difficultyConfig[difficulty];
  
  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border",
        config.className,
        className
      )}
    >
      {config.label}
    </span>
  );
}
