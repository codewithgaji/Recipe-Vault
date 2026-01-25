import { useState, useEffect } from "react";
import { Plus, Trash2, GripVertical } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { StarRating } from "@/components/ui/star-rating";
import {
  Recipe,
  RecipeCreate,
  IngredientItem,
  CATEGORIES,
  DIFFICULTIES,
  Difficulty,
  Category,
} from "@/types/recipe";

interface RecipeFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (recipe: RecipeCreate) => void;
  recipe?: Recipe | null;
  isLoading?: boolean;
}

const defaultFormData: RecipeCreate = {
  title: "",
  description: "",
  ingredients: [{ name: "", quantity: "" }],
  instructions: [""],
  prep_time: 15,
  cook_time: 30,
  servings: 4,
  difficulty: "medium",
  category: "Dinner",
  image_url: "",
  rating: 3,
};

export function RecipeForm({
  open,
  onClose,
  onSubmit,
  recipe,
  isLoading,
}: RecipeFormProps) {
  const [formData, setFormData] = useState<RecipeCreate>(defaultFormData);

  useEffect(() => {
    if (recipe) {
      setFormData({
        title: recipe.title,
        description: recipe.description,
        ingredients: recipe.ingredients.length > 0 ? recipe.ingredients : [{ name: "", quantity: "" }],
        instructions: recipe.instructions.length > 0 ? recipe.instructions : [""],
        prep_time: recipe.prep_time,
        cook_time: recipe.cook_time,
        servings: recipe.servings,
        difficulty: recipe.difficulty,
        category: recipe.category,
        image_url: recipe.image_url || "",
        rating: recipe.rating,
      });
    } else {
      setFormData(defaultFormData);
    }
  }, [recipe, open]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const cleanedData = {
      ...formData,
      ingredients: formData.ingredients.filter((i) => i.name.trim() !== ""),
      instructions: formData.instructions.filter((i) => i.trim() !== ""),
    };
    onSubmit(cleanedData);
  };

  const addIngredient = () => {
    setFormData({
      ...formData,
      ingredients: [...formData.ingredients, { name: "", quantity: "" }],
    });
  };

  const removeIngredient = (index: number) => {
    setFormData({
      ...formData,
      ingredients: formData.ingredients.filter((_, i) => i !== index),
    });
  };

  const updateIngredient = (
    index: number,
    field: keyof IngredientItem,
    value: string
  ) => {
    const updated = [...formData.ingredients];
    updated[index] = { ...updated[index], [field]: value };
    setFormData({ ...formData, ingredients: updated });
  };

  const addInstruction = () => {
    setFormData({
      ...formData,
      instructions: [...formData.instructions, ""],
    });
  };

  const removeInstruction = (index: number) => {
    setFormData({
      ...formData,
      instructions: formData.instructions.filter((_, i) => i !== index),
    });
  };

  const updateInstruction = (index: number, value: string) => {
    const updated = [...formData.instructions];
    updated[index] = value;
    setFormData({ ...formData, instructions: updated });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="font-display text-2xl">
            {recipe ? "Edit Recipe" : "Add New Recipe"}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="space-y-4">
            <div>
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
                placeholder="e.g., Grandma's Apple Pie"
                required
              />
            </div>

            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                placeholder="A brief description of this recipe..."
                rows={2}
                required
              />
            </div>

            <div>
              <Label htmlFor="image_url">Image URL (optional)</Label>
              <Input
                id="image_url"
                type="url"
                value={formData.image_url}
                onChange={(e) =>
                  setFormData({ ...formData, image_url: e.target.value })
                }
                placeholder="https://example.com/image.jpg"
              />
            </div>
          </div>

          {/* Details Row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <Label htmlFor="prep_time">Prep (min)</Label>
              <Input
                id="prep_time"
                type="number"
                min="0"
                value={formData.prep_time}
                onChange={(e) =>
                  setFormData({ ...formData, prep_time: parseInt(e.target.value) || 0 })
                }
                required
              />
            </div>
            <div>
              <Label htmlFor="cook_time">Cook (min)</Label>
              <Input
                id="cook_time"
                type="number"
                min="0"
                value={formData.cook_time}
                onChange={(e) =>
                  setFormData({ ...formData, cook_time: parseInt(e.target.value) || 0 })
                }
                required
              />
            </div>
            <div>
              <Label htmlFor="servings">Servings</Label>
              <Input
                id="servings"
                type="number"
                min="1"
                value={formData.servings}
                onChange={(e) =>
                  setFormData({ ...formData, servings: parseInt(e.target.value) || 1 })
                }
                required
              />
            </div>
            <div>
              <Label>Rating</Label>
              <div className="pt-2">
                <StarRating
                  rating={formData.rating}
                  size="md"
                  interactive
                  onRatingChange={(rating) =>
                    setFormData({ ...formData, rating })
                  }
                />
              </div>
            </div>
          </div>

          {/* Category & Difficulty */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Category</Label>
              <Select
                value={formData.category}
                onValueChange={(value: Category) =>
                  setFormData({ ...formData, category: value })
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORIES.map((cat) => (
                    <SelectItem key={cat} value={cat}>
                      {cat}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Difficulty</Label>
              <Select
                value={formData.difficulty}
                onValueChange={(value: Difficulty) =>
                  setFormData({ ...formData, difficulty: value })
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {DIFFICULTIES.map((diff) => (
                    <SelectItem key={diff} value={diff} className="capitalize">
                      {diff.charAt(0).toUpperCase() + diff.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Ingredients */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <Label>Ingredients</Label>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addIngredient}
              >
                <Plus className="w-4 h-4 mr-1" /> Add
              </Button>
            </div>
            <div className="space-y-2">
              {formData.ingredients.map((ingredient, index) => (
                <div key={index} className="flex gap-2 items-center">
                  <GripVertical className="w-4 h-4 text-muted-foreground/50 flex-shrink-0" />
                  <Input
                    placeholder="Quantity (e.g., 2 cups)"
                    value={ingredient.quantity}
                    onChange={(e) =>
                      updateIngredient(index, "quantity", e.target.value)
                    }
                    className="w-32 flex-shrink-0"
                  />
                  <Input
                    placeholder="Ingredient name"
                    value={ingredient.name}
                    onChange={(e) =>
                      updateIngredient(index, "name", e.target.value)
                    }
                    className="flex-1"
                  />
                  {formData.ingredients.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => removeIngredient(index)}
                      className="text-destructive hover:text-destructive"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Instructions */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <Label>Instructions</Label>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addInstruction}
              >
                <Plus className="w-4 h-4 mr-1" /> Add Step
              </Button>
            </div>
            <div className="space-y-2">
              {formData.instructions.map((instruction, index) => (
                <div key={index} className="flex gap-2 items-start">
                  <span className="w-6 h-9 flex items-center justify-center text-sm font-medium text-muted-foreground bg-muted rounded flex-shrink-0">
                    {index + 1}
                  </span>
                  <Textarea
                    placeholder={`Step ${index + 1}...`}
                    value={instruction}
                    onChange={(e) => updateInstruction(index, e.target.value)}
                    rows={2}
                    className="flex-1"
                  />
                  {formData.instructions.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => removeInstruction(index)}
                      className="text-destructive hover:text-destructive mt-1"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Saving..." : recipe ? "Save Changes" : "Create Recipe"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
