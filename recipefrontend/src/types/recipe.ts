export interface IngredientItem {
  name: string;
  quantity: string;
}

export type Difficulty = "easy" | "medium" | "hard";

export type Category = "Breakfast" | "Lunch" | "Dinner" | "Dessert" | "Snack" | "Beverage";

export interface Recipe {
  id: number;
  title: string;
  description: string;
  ingredients: IngredientItem[];
  instructions: string[];
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: Difficulty;
  category: Category;
  image_url?: string;
  rating: number;
  created_at: string;
  updated_at: string;
}

export interface RecipeCreate {
  title: string;
  description: string;
  ingredients: IngredientItem[];
  instructions: string[];
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: Difficulty;
  category: Category;
  image_url?: string;
  rating: number;
}

export interface RecipeUpdate {
  title?: string;
  description?: string;
  ingredients?: IngredientItem[];
  instructions?: string[];
  prep_time?: number;
  cook_time?: number;
  servings?: number;
  difficulty?: Difficulty;
  category?: Category;
  image_url?: string;
  rating?: number;
}

export const CATEGORIES: Category[] = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Beverage"];
export const DIFFICULTIES: Difficulty[] = ["easy", "medium", "hard"];
