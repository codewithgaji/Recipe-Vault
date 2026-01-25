import { Search, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { CATEGORIES, DIFFICULTIES, Category, Difficulty } from "@/types/recipe";

interface RecipeFiltersProps {
  search: string;
  onSearchChange: (value: string) => void;
  category: string;
  onCategoryChange: (value: string) => void;
  difficulty: string;
  onDifficultyChange: (value: string) => void;
  onClearFilters: () => void;
}

export function RecipeFilters({
  search,
  onSearchChange,
  category,
  onCategoryChange,
  difficulty,
  onDifficultyChange,
  onClearFilters,
}: RecipeFiltersProps) {
  const hasFilters = search || category || difficulty;

  return (
    <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
      <div className="relative flex-1 max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          placeholder="Search recipes..."
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-10"
        />
      </div>
      
      <Select value={category} onValueChange={onCategoryChange}>
        <SelectTrigger className="w-full sm:w-[160px]">
          <SelectValue placeholder="Category" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Categories</SelectItem>
          {CATEGORIES.map((cat) => (
            <SelectItem key={cat} value={cat}>
              {cat}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      
      <Select value={difficulty} onValueChange={onDifficultyChange}>
        <SelectTrigger className="w-full sm:w-[140px]">
          <SelectValue placeholder="Difficulty" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Levels</SelectItem>
          {DIFFICULTIES.map((diff) => (
            <SelectItem key={diff} value={diff} className="capitalize">
              {diff.charAt(0).toUpperCase() + diff.slice(1)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      
      {hasFilters && (
        <Button
          variant="ghost"
          size="sm"
          onClick={onClearFilters}
          className="gap-1"
        >
          <X className="w-4 h-4" />
          Clear
        </Button>
      )}
    </div>
  );
}
