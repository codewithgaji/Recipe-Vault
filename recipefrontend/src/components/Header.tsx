import { ChefHat, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  onAddRecipe: () => void;
}

export function Header({ onAddRecipe }: HeaderProps) {
  return (
    <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <ChefHat className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-display text-2xl font-semibold tracking-tight">
                RecipeVault
              </h1>
              <p className="text-xs text-muted-foreground">
                Your personal recipe collection
              </p>
            </div>
          </div>
          
          <Button onClick={onAddRecipe} className="gap-2">
            <Plus className="w-4 h-4" />
            <span className="hidden sm:inline">Add Recipe</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
