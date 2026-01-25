import { Clock, Users, ChefHat, Edit, Trash2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StarRating } from "@/components/ui/star-rating";
import { DifficultyBadge } from "@/components/ui/difficulty-badge";
import { CategoryBadge } from "@/components/ui/category-badge";
import { Separator } from "@/components/ui/separator";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Recipe } from "@/types/recipe";

interface RecipeDetailProps {
  recipe: Recipe | null;
  open: boolean;
  onClose: () => void;
  onEdit: (recipe: Recipe) => void;
  onDelete: (id: number) => void;
}

export function RecipeDetail({
  recipe,
  open,
  onClose,
  onEdit,
  onDelete,
}: RecipeDetailProps) {
  if (!recipe) return null;

  const totalTime = recipe.prep_time + recipe.cook_time;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto p-0">
        {/* Hero Image */}
        <div className="aspect-[16/9] bg-muted relative">
          {recipe.image_url ? (
            <img
              src={recipe.image_url}
              alt={recipe.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/10 to-secondary/10">
              <ChefHat className="w-24 h-24 text-muted-foreground/30" />
            </div>
          )}
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-4 right-4 bg-background/80 backdrop-blur-sm hover:bg-background"
            onClick={onClose}
          >
            <X className="w-5 h-5" />
          </Button>
        </div>

        <div className="p-6 space-y-6">
          {/* Header */}
          <div className="space-y-3">
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <DifficultyBadge difficulty={recipe.difficulty} />
                  <CategoryBadge category={recipe.category} />
                </div>
                <h2 className="font-display text-3xl font-semibold">
                  {recipe.title}
                </h2>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onEdit(recipe)}
                >
                  <Edit className="w-4 h-4 mr-1" /> Edit
                </Button>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="destructive" size="sm">
                      <Trash2 className="w-4 h-4 mr-1" /> Delete
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Delete Recipe?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This will permanently delete "{recipe.title}". This action cannot be undone.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction
                        onClick={() => {
                          onDelete(recipe.id);
                          onClose();
                        }}
                        className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                      >
                        Delete
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>

            <p className="text-muted-foreground">{recipe.description}</p>

            <div className="flex items-center gap-6">
              <StarRating rating={recipe.rating} size="md" />
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4" />
                  <span>{totalTime} min total</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Users className="w-4 h-4" />
                  <span>{recipe.servings} servings</span>
                </div>
              </div>
            </div>

            {/* Time breakdown */}
            <div className="flex gap-4 text-sm">
              <div className="bg-muted rounded-lg px-4 py-2">
                <span className="text-muted-foreground">Prep:</span>{" "}
                <span className="font-medium">{recipe.prep_time} min</span>
              </div>
              <div className="bg-muted rounded-lg px-4 py-2">
                <span className="text-muted-foreground">Cook:</span>{" "}
                <span className="font-medium">{recipe.cook_time} min</span>
              </div>
            </div>
          </div>

          <Separator />

          {/* Ingredients */}
          <div>
            <h3 className="font-display text-xl font-semibold mb-4">Ingredients</h3>
            <ul className="space-y-2">
              {recipe.ingredients.map((ingredient, index) => (
                <li
                  key={index}
                  className="flex items-baseline gap-3 py-1.5 border-b border-border/50 last:border-0"
                >
                  <span className="font-medium text-primary min-w-[100px]">
                    {ingredient.quantity}
                  </span>
                  <span>{ingredient.name}</span>
                </li>
              ))}
            </ul>
          </div>

          <Separator />

          {/* Instructions */}
          <div>
            <h3 className="font-display text-xl font-semibold mb-4">Instructions</h3>
            <ol className="space-y-4">
              {recipe.instructions.map((instruction, index) => (
                <li key={index} className="flex gap-4">
                  <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-semibold">
                    {index + 1}
                  </span>
                  <p className="pt-1">{instruction}</p>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
