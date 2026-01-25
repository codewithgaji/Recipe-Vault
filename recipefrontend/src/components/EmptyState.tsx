import { ChefHat, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  hasFilters: boolean;
  onAddRecipe: () => void;
  onClearFilters: () => void;
}

export function EmptyState({ hasFilters, onAddRecipe, onClearFilters }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center animate-fade-in">
      <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mb-6">
        <ChefHat className="w-10 h-10 text-muted-foreground" />
      </div>
      
      <h2 className="font-display text-2xl font-semibold mb-2">
        {hasFilters ? "No recipes found" : "No recipes yet"}
      </h2>
      
      <p className="text-muted-foreground max-w-md mb-6">
        {hasFilters
          ? "Try adjusting your filters or search terms"
          : "Start building your recipe collection by adding your first recipe!"}
      </p>

      {hasFilters ? (
        <Button variant="outline" onClick={onClearFilters}>
          Clear Filters
        </Button>
      ) : (
        <Button onClick={onAddRecipe} className="gap-2">
          <Plus className="w-4 h-4" />
          Add Your First Recipe
        </Button>
      )}
    </div>
  );
}
