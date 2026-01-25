import { useState, useMemo } from "react";
import { Header } from "@/components/Header";
import { RecipeFilters } from "@/components/RecipeFilters";
import { RecipeCard } from "@/components/RecipeCard";
import { RecipeForm } from "@/components/RecipeForm";
import { RecipeDetail } from "@/components/RecipeDetail";
import { BackendError } from "@/components/BackendError";
import { EmptyState } from "@/components/EmptyState";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import {
  useRecipes,
  useCreateRecipe,
  useUpdateRecipe,
  useDeleteRecipe,
} from "@/hooks/useRecipes";
import { Recipe, RecipeCreate } from "@/types/recipe";

const Index = () => {
  // Filters
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");

  // Debounced search for API
  const [debouncedSearch, setDebouncedSearch] = useState("");

  // Update debounced search after typing stops
  useState(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(timer);
  });

  // Modal states
  const [formOpen, setFormOpen] = useState(false);
  const [detailOpen, setDetailOpen] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [editingRecipe, setEditingRecipe] = useState<Recipe | null>(null);

  // API hooks
  const { data: recipes, isLoading, error, refetch } = useRecipes({
    search: debouncedSearch || undefined,
    category: category && category !== "all" ? category : undefined,
    difficulty: difficulty && difficulty !== "all" ? difficulty : undefined,
  });

  const createRecipe = useCreateRecipe();
  const updateRecipe = useUpdateRecipe();
  const deleteRecipe = useDeleteRecipe();

  const hasFilters = Boolean(search || (category && category !== "all") || (difficulty && difficulty !== "all"));

  const clearFilters = () => {
    setSearch("");
    setCategory("");
    setDifficulty("");
    setDebouncedSearch("");
  };

  const handleAddRecipe = () => {
    setEditingRecipe(null);
    setFormOpen(true);
  };

  const handleEditRecipe = (recipe: Recipe) => {
    setEditingRecipe(recipe);
    setDetailOpen(false);
    setFormOpen(true);
  };

  const handleViewRecipe = (recipe: Recipe) => {
    setSelectedRecipe(recipe);
    setDetailOpen(true);
  };

  const handleFormSubmit = (data: RecipeCreate) => {
    if (editingRecipe) {
      updateRecipe.mutate(
        { id: editingRecipe.id, recipe: data },
        {
          onSuccess: () => setFormOpen(false),
        }
      );
    } else {
      createRecipe.mutate(data, {
        onSuccess: () => setFormOpen(false),
      });
    }
  };

  const handleDeleteRecipe = (id: number) => {
    deleteRecipe.mutate(id);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header onAddRecipe={handleAddRecipe} />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <RecipeFilters
            search={search}
            onSearchChange={setSearch}
            category={category}
            onCategoryChange={setCategory}
            difficulty={difficulty}
            onDifficultyChange={setDifficulty}
            onClearFilters={clearFilters}
          />
        </div>

        {/* Error State */}
        {error && (
          <BackendError error={error} onRetry={() => refetch()} />
        )}

        {/* Loading State */}
        {isLoading && !error && <LoadingSkeleton />}

        {/* Empty State */}
        {!isLoading && !error && recipes?.length === 0 && (
          <EmptyState
            hasFilters={hasFilters}
            onAddRecipe={handleAddRecipe}
            onClearFilters={clearFilters}
          />
        )}

        {/* Recipe Grid */}
        {!isLoading && !error && recipes && recipes.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {recipes.map((recipe) => (
              <RecipeCard
                key={recipe.id}
                recipe={recipe}
                onClick={() => handleViewRecipe(recipe)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Recipe Form Modal */}
      <RecipeForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSubmit={handleFormSubmit}
        recipe={editingRecipe}
        isLoading={createRecipe.isPending || updateRecipe.isPending}
      />

      {/* Recipe Detail Modal */}
      <RecipeDetail
        recipe={selectedRecipe}
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
        onEdit={handleEditRecipe}
        onDelete={handleDeleteRecipe}
      />
    </div>
  );
};

export default Index;
