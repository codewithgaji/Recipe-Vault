import { Recipe, RecipeCreate, RecipeUpdate } from "@/types/recipe";

const API_BASE_URL = "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  
  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(errorText || `HTTP error ${response.status}`, response.status);
  }
  return response.json();
}

async function fetchWithTimeout(url: string, options: RequestInit = {}, timeout = 5000): Promise<Response> {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(id);
    return response;
  } catch (error) {
    clearTimeout(id);
    if (error instanceof Error && error.name === "AbortError") {
      throw new ApiError("Request timed out - is the backend running?", 0);
    }
    throw error;
  }
}

export const recipeApi = {
  // GET /recipes - List all recipes with optional filters
  async getRecipes(params?: {
    search?: string;
    category?: string;
    difficulty?: string;
  }): Promise<Recipe[]> {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append("search", params.search);
    if (params?.category) searchParams.append("category", params.category);
    if (params?.difficulty) searchParams.append("difficulty", params.difficulty);
    
    const queryString = searchParams.toString();
    const url = `${API_BASE_URL}/recipes${queryString ? `?${queryString}` : ""}`;
    
    const response = await fetchWithTimeout(url);
    return handleResponse<Recipe[]>(response);
  },

  // GET /recipes/:id - Get a single recipe
  async getRecipe(id: number): Promise<Recipe> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/recipes/${id}`);
    return handleResponse<Recipe>(response);
  },

  // POST /recipes - Create a new recipe
  async createRecipe(recipe: RecipeCreate): Promise<Recipe> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/recipes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recipe),
    });
    return handleResponse<Recipe>(response);
  },

  // PUT /recipes/:id - Update a recipe
  async updateRecipe(id: number, recipe: RecipeUpdate): Promise<Recipe> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/recipes/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recipe),
    });
    return handleResponse<Recipe>(response);
  },

  // DELETE /recipes/:id - Delete a recipe
  async deleteRecipe(id: number): Promise<void> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/recipes/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(errorText || `HTTP error ${response.status}`, response.status);
    }
  },
};
