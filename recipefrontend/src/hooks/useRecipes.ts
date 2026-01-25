import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { recipeApi } from "@/services/api";
import { RecipeCreate, RecipeUpdate } from "@/types/recipe";
import { useToast } from "@/hooks/use-toast";

export function useRecipes(filters?: {
  search?: string;
  category?: string;
  difficulty?: string;
}) {
  return useQuery({
    queryKey: ["recipes", filters],
    queryFn: () => recipeApi.getRecipes(filters),
    retry: false,
  });
}

export function useRecipe(id: number) {
  return useQuery({
    queryKey: ["recipe", id],
    queryFn: () => recipeApi.getRecipe(id),
    enabled: id > 0,
    retry: false,
  });
}

export function useCreateRecipe() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (recipe: RecipeCreate) => recipeApi.createRecipe(recipe),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["recipes"] });
      toast({
        title: "Recipe created!",
        description: "Your new recipe has been saved.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create recipe",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

export function useUpdateRecipe() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, recipe }: { id: number; recipe: RecipeUpdate }) =>
      recipeApi.updateRecipe(id, recipe),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["recipes"] });
      toast({
        title: "Recipe updated!",
        description: "Your changes have been saved.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update recipe",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

export function useDeleteRecipe() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: number) => recipeApi.deleteRecipe(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["recipes"] });
      toast({
        title: "Recipe deleted",
        description: "The recipe has been removed.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to delete recipe",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}
