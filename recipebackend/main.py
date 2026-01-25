from fastapi import FastAPI, Depends, HTTPException
from schemas import Recipe, IngredientItem, Difficulty, Category
from datetime import date



app = FastAPI()

RECIPES = [
  Recipe(
    id=1,
    title="Jollof Rice",
    description="Nigerian Jollof, the Best in Africa",
    ingredients=[
      IngredientItem(name="Rice", quantity="2 cups"),
      IngredientItem(name="Tomatoes", quantity="4"),
      IngredientItem(name="Onions", quantity="2"),
    ],
    instructions="Cook rice with tomato sauce and spices until tender",
    prep_time=15,
    cook_time=25,
    servings=4,
    difficulty=Difficulty.MEDIUM,
    category=Category.LUNCH,
    image_url="jollof.png",
    rating=5,
    created_at=date(2024, 1, 15),
    updated_at=date(2024, 1, 20),
  ),
  Recipe(
    id=2,
    title="Pancakes",
    description="Fluffy breakfast pancakes",
    ingredients=[
      IngredientItem(name="Flour", quantity="2 cups"),
      IngredientItem(name="Eggs", quantity="3"),
    ],
    instructions="Mix and cook on griddle",
    prep_time=10,
    cook_time=10,
    servings=3,
    difficulty=Difficulty.EASY,
    category=Category.BREAKFAST,
    image_url="pancakes.png",
    rating=4,
    created_at=date(2024, 1, 10),
    updated_at=date(2024, 1, 18),
  ),
  Recipe(
    id=3,
    title="Grilled Chicken",
    description="Seasoned grilled chicken breast",
    ingredients=[
      IngredientItem(name="Chicken", quantity="500g"),
      IngredientItem(name="Garlic", quantity="3 cloves"),
    ],
    instructions="Grill until cooked through",
    prep_time=20,
    cook_time=15,
    servings=2,
    difficulty=Difficulty.EASY,
    category=Category.DINNER,
    image_url="chicken.png",
    rating=4,
    created_at=date(2024, 1, 12),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=4,
    title="Chocolate Cake",
    description="Rich chocolate dessert",
    ingredients=[
      IngredientItem(name="Chocolate", quantity="200g"),
      IngredientItem(name="Flour", quantity="1.5 cups"),
    ],
    instructions="Bake at 350F for 35 minutes",
    prep_time=15,
    cook_time=35,
    servings=8,
    difficulty=Difficulty.MEDIUM,
    category=Category.DESERT,
    image_url="cake.png",
    rating=5,
    created_at=date(2024, 1, 5),
    updated_at=date(2024, 1, 17),
  ),
  Recipe(
    id=5,
    title="Vegetable Stir Fry",
    description="Quick Asian-inspired vegetables",
    ingredients=[
      IngredientItem(name="Broccoli", quantity="2 cups"),
      IngredientItem(name="Soy Sauce", quantity="3 tbsp"),
    ],
    instructions="Stir fry on high heat",
    prep_time=10,
    cook_time=8,
    servings=3,
    difficulty=Difficulty.EASY,
    category=Category.LUNCH,
    image_url="stirfry.png",
    rating=4,
    created_at=date(2024, 1, 14),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=6,
    title="Smoothie Bowl",
    description="Nutritious breakfast bowl",
    ingredients=[
      IngredientItem(name="Yogurt", quantity="1 cup"),
      IngredientItem(name="Berries", quantity="1 cup"),
    ],
    instructions="Blend and top with granola",
    prep_time=5,
    cook_time=0,
    servings=1,
    difficulty=Difficulty.EASY,
    category=Category.BREAKFAST,
    image_url="smoothie.png",
    rating=4,
    created_at=date(2024, 1, 8),
    updated_at=date(2024, 1, 18),
  ),
  Recipe(
    id=7,
    title="Pasta Carbonara",
    description="Classic Italian pasta",
    ingredients=[
      IngredientItem(name="Pasta", quantity="400g"),
      IngredientItem(name="Eggs", quantity="3"),
      IngredientItem(name="Bacon", quantity="200g"),
    ],
    instructions="Toss hot pasta with sauce",
    prep_time=10,
    cook_time=12,
    servings=4,
    difficulty=Difficulty.MEDIUM,
    category=Category.DINNER,
    image_url="carbonara.png",
    rating=5,
    created_at=date(2024, 1, 11),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=8,
    title="Lemonade",
    description="Refreshing homemade lemonade",
    ingredients=[
      IngredientItem(name="Lemon", quantity="5"),
      IngredientItem(name="Sugar", quantity="1 cup"),
    ],
    instructions="Squeeze lemons and mix with water",
    prep_time=5,
    cook_time=0,
    servings=4,
    difficulty=Difficulty.EASY,
    category=Category.BEVERAGE,
    image_url="lemonade.png",
    rating=4,
    created_at=date(2024, 1, 13),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=9,
    title="Brownies",
    description="Fudgy chocolate brownies",
    ingredients=[
      IngredientItem(name="Chocolate", quantity="150g"),
      IngredientItem(name="Butter", quantity="100g"),
    ],
    instructions="Bake at 350F for 25 minutes",
    prep_time=15,
    cook_time=25,
    servings=12,
    difficulty=Difficulty.EASY,
    category=Category.DESERT,
    image_url="brownies.png",
    rating=5,
    created_at=date(2024, 1, 9),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=10,
    title="Caesar Salad",
    description="Crispy lettuce with Caesar dressing",
    ingredients=[
      IngredientItem(name="Lettuce", quantity="1 head"),
      IngredientItem(name="Croutons", quantity="1 cup"),
    ],
    instructions="Toss with dressing",
    prep_time=10,
    cook_time=0,
    servings=2,
    difficulty=Difficulty.EASY,
    category=Category.LUNCH,
    image_url="salad.png",
    rating=4,
    created_at=date(2024, 1, 16),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id = 11,
    title = "Puff Puff",
    description="Soft Puffy Delicious Puffs",
    ingredients=[
      IngredientItem(name="Flour", quantity="1 Cup"),
      IngredientItem(name="Milk", quantity="1/2 Cup"),
      IngredientItem(name="Sugar", quantity="1/4 Cup"),
      IngredientItem(name="Yeast", quantity="1 tsp"),
    ],
    instructions="Mix the ingredients for 3 mins",
    prep_time=10,
    cook_time=10,
    servings=8,
    difficulty=Difficulty.EASY,
    category=Category.SNACK,
    image_url="Puff-Puff.png",
    rating=5,
    created_at=date(2026, 1, 23),
    updated_at=date(2026, 1, 24)
  )
]

@app.get("/")
def welcome():
  return {"Hello": "Welcome to RecipeVault Backend 😁"}


@app.get("/recipes")
async def get_recipes():
  return RECIPES


@app.get("/recipes/{recipe_id}")
async def get_recipe_by_id(recipe_id: int):
  recipe = next((b for b in RECIPES if b.id == recipe_id), None)
  if recipe is None:
    raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found")
  return recipe


@app.post("/recipes")
def add_recipe(recipe: Recipe):
  exists= any(r.id == recipe.id for r in RECIPES) # This works because now we are checking through the ENTIRE list if something is True/exists

    # if not RECIPES[b].id == recipe.id: # Don't use this statement, it allows duplicates
  if exists:
    raise HTTPException(status_code=400, detail=f"Recipe {recipe.id} Already Exists")
  RECIPES.append(recipe)
  return {"message": f"{recipe.title} added successfully", "recipe": recipe}


@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, recipe: Recipe):
  for i in range(len(RECIPES)):
    if RECIPES[i].id == recipe_id:
      RECIPES[i] = recipe
      recipe.id = recipe_id # Keep ID consistent
      return {"Message": f"Recipe {RECIPES[i].id} Updated Successfully!"}
  raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found, Update Failed!")
  


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
  for i in range(len(RECIPES)):
    if RECIPES[i].id == recipe_id:
      del RECIPES[i]
      return {"Message": f"Recipe {recipe_id} Has Been Deleted Successfully"}
  raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found")