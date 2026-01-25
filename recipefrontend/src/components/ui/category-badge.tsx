import { cn } from "@/lib/utils";
import { Category } from "@/types/recipe";

interface CategoryBadgeProps {
  category: Category;
  className?: string;
}

export function CategoryBadge({ category, className }: CategoryBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
        "bg-secondary/20 text-secondary border border-secondary/30",
        className
      )}
    >
      {category}
    </span>
  );
}
