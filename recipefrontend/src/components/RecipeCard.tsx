import { Clock, Users, ChefHat } from "lucide-react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { StarRating } from "@/components/ui/star-rating";
import { DifficultyBadge } from "@/components/ui/difficulty-badge";
import { CategoryBadge } from "@/components/ui/category-badge";
import { Recipe } from "@/types/recipe";

interface RecipeCardProps {
  recipe: Recipe;
  onClick: () => void;
}

export function RecipeCard({ recipe, onClick }: RecipeCardProps) {
  const totalTime = recipe.prep_time + recipe.cook_time;

  return (
    <Card
      className="group cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1 animate-fade-in"
      onClick={onClick}
    >
      <div className="aspect-[4/3] overflow-hidden bg-muted relative">
        {recipe.image_url ? (
          <img
            src={recipe.image_url}
            alt={recipe.title}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/10 to-secondary/10">
            <ChefHat className="w-16 h-16 text-muted-foreground/30" />
          </div>
        )}
        <div className="absolute top-3 left-3 flex gap-2">
          <DifficultyBadge difficulty={recipe.difficulty} />
        </div>
        <div className="absolute top-3 right-3">
          <CategoryBadge category={recipe.category} />
        </div>
      </div>
      
      <CardContent className="p-4">
        <h3 className="font-display text-lg font-semibold text-foreground line-clamp-1 mb-1">
          {recipe.title}
        </h3>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {recipe.description}
        </p>
        <StarRating rating={recipe.rating} size="sm" />
      </CardContent>
      
      <CardFooter className="px-4 pb-4 pt-0">
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" />
            <span>{totalTime} min</span>
          </div>
          <div className="flex items-center gap-1">
            <Users className="w-3.5 h-3.5" />
            <span>{recipe.servings} servings</span>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
