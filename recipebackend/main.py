from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from schemas import Recipe, IngredientItem, Difficulty, Category, RecipeCreate
from datetime import date
from sqlalchemy.orm import Session
import database_models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import cloudinary.uploader




app = FastAPI()

# origins = [
#   "http://localhost:8080"
# ]



app.add_middleware(
  CORSMiddleware,
  allow_origins = ["https://recipe-vault-pearl.vercel.app", "http://localhost:8080"],
  allow_headers = ["*"],
  allow_credentials = True,
  allow_methods = ["*"]
)



RECIPES = [
  Recipe(
    id=1,
    title="Jollof Rice",
    description="Nigerian Jollof, the Best in Africa",
    ingredients=[
      IngredientItem(name="Rice", quantity="2 cups"),
      IngredientItem(name="Tomatoes", quantity="4"),
      IngredientItem(name="Onions", quantity="2"),
      IngredientItem(name="Red Bell Pepper", quantity="2"),
      IngredientItem(name="Tomato Paste", quantity="3 tbsp"),
      IngredientItem(name="Chicken Broth", quantity="4 cups"),
      IngredientItem(name="Butter", quantity="4 tbsp"),
    ],
    instructions=[
      "Heat butter and sauté onions.",
      "Add tomato paste and cook for 2 mins.",
      "Add blended tomatoes and peppers, simmer for 10 mins.",
      "Add rice and broth, bring to boil.",
      "Reduce heat and cook covered for 20 mins until rice is tender and liquid is absorbed."
    ],
    prep_time=15,
    cook_time=30,
    servings=4,
    difficulty=Difficulty.MEDIUM,
    category=Category.LUNCH,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474548/recipe_vault/jzbji0eyw0gribm0mcpk.jpg",
    rating=5,
    created_at=date(2024, 1, 15),
    updated_at=date(2024, 1, 20),
  ),
  Recipe(
    id=2,
    title="Pancakes",
    description="Fluffy breakfast pancakes",
    ingredients=[
      IngredientItem(name="All-Purpose Flour", quantity="2 cups"),
      IngredientItem(name="Eggs", quantity="2"),
      IngredientItem(name="Milk", quantity="1.5 cups"),
      IngredientItem(name="Baking Powder", quantity="2 tsp"),
      IngredientItem(name="Salt", quantity="1/2 tsp"),
      IngredientItem(name="Sugar", quantity="2 tbsp"),
      IngredientItem(name="Butter", quantity="3 tbsp"),
    ],
    instructions=[
      "Mix flour, baking powder, salt, and sugar.",
      "Beat eggs and mix with milk and melted butter.",
      "Combine wet and dry ingredients until just blended.",
      "Pour 1/4 cup batter per pancake onto greased griddle.",
      "Cook 2-3 mins per side until golden."
    ],
    prep_time=10,
    cook_time=15,
    servings=3,
    difficulty=Difficulty.EASY,
    category=Category.BREAKFAST,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474549/recipe_vault/mfijkaw2afjloqkro93i.jpg",
    rating=4,
    created_at=date(2024, 1, 10),
    updated_at=date(2024, 1, 18),
  ),
  Recipe(
    id=3,
    title="Grilled Chicken",
    description="Seasoned grilled chicken breast",
    ingredients=[
      IngredientItem(name="Chicken Breast", quantity="500g"),
      IngredientItem(name="Garlic", quantity="4 cloves"),
      IngredientItem(name="Olive Oil", quantity="3 tbsp"),
      IngredientItem(name="Lemon Juice", quantity="2 tbsp"),
      IngredientItem(name="Salt", quantity="to taste"),
      IngredientItem(name="Black Pepper", quantity="to taste"),
      IngredientItem(name="Thyme", quantity="1 tsp"),
    ],
    instructions=[
      "Mix olive oil, minced garlic, lemon juice, and herbs.",
      "Coat chicken breasts with marinade and let sit 30 mins.",
      "Preheat grill to medium-high.",
      "Grill for 6-7 mins per side until internal temperature reaches 165°F."
    ],
    prep_time=35,
    cook_time=15,
    servings=2,
    difficulty=Difficulty.EASY,
    category=Category.DINNER,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474547/recipe_vault/jh2x413fo4rcjfebwg75.jpg",
    rating=4,
    created_at=date(2024, 1, 12),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=4,
    title="Chocolate Cake",
    description="Rich chocolate dessert",
    ingredients=[
      IngredientItem(name="All-Purpose Flour", quantity="2 cups"),
      IngredientItem(name="Cocoa Powder", quantity="3/4 cup"),
      IngredientItem(name="Sugar", quantity="2 cups"),
      IngredientItem(name="Eggs", quantity="2"),
      IngredientItem(name="Butter", quantity="1/2 cup"),
      IngredientItem(name="Milk", quantity="1 cup"),
      IngredientItem(name="Baking Powder", quantity="1.5 tsp"),
      IngredientItem(name="Vanilla Extract", quantity="1 tsp"),
    ],
    instructions=[
      "Cream butter and sugar.",
      "Add eggs one at a time.",
      "Mix flour, cocoa, and baking powder.",
      "Alternate adding dry ingredients and milk.",
      "Stir in vanilla.",
      "Pour into greased 9-inch pan.",
      "Bake at 350°F for 35-40 minutes until toothpick comes out clean."
    ],
    prep_time=20,
    cook_time=40,
    servings=8,
    difficulty=Difficulty.MEDIUM,
    category=Category.DESERT,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474546/recipe_vault/tyddy7bpmaoy7grzezss.jpg",
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
      IngredientItem(name="Bell Peppers", quantity="2"),
      IngredientItem(name="Carrots", quantity="2"),
      IngredientItem(name="Soy Sauce", quantity="3 tbsp"),
      IngredientItem(name="Garlic", quantity="3 cloves"),
      IngredientItem(name="Ginger", quantity="1 tbsp"),
      IngredientItem(name="Vegetable Oil", quantity="2 tbsp"),
      IngredientItem(name="Sesame Oil", quantity="1 tsp"),
    ],
    instructions=[
      "Heat oil in wok over high heat.",
      "Add garlic and ginger, cook 30 seconds.",
      "Add broccoli and carrots, stir fry 4-5 mins.",
      "Add peppers and soy sauce, cook 3 more minutes until vegetables are tender-crisp.",
      "Drizzle with sesame oil and serve."
    ],
    prep_time=15,
    cook_time=10,
    servings=3,
    difficulty=Difficulty.EASY,
    category=Category.LUNCH,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474552/recipe_vault/aq9nfrgmjev3mt2ecmgp.jpg",
    rating=4,
    created_at=date(2024, 1, 14),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=6,
    title="Smoothie Bowl",
    description="Nutritious breakfast bowl",
    ingredients=[
      IngredientItem(name="Greek Yogurt", quantity="1 cup"),
      IngredientItem(name="Frozen Berries", quantity="1.5 cups"),
      IngredientItem(name="Banana", quantity="1"),
      IngredientItem(name="Honey", quantity="1 tbsp"),
      IngredientItem(name="Granola", quantity="1/2 cup"),
      IngredientItem(name="Coconut Flakes", quantity="2 tbsp"),
      IngredientItem(name="Almond Butter", quantity="1 tbsp"),
    ],
    instructions=[
      "Blend yogurt, frozen berries, banana, and honey until smooth.",
      "Pour into bowl.",
      "Top with granola, coconut flakes, and almond butter.",
      "Serve immediately."
    ],
    prep_time=5,
    cook_time=0,
    servings=1,
    difficulty=Difficulty.EASY,
    category=Category.BREAKFAST,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474551/recipe_vault/jthfpd1zieyvanlqpzbv.jpg",
    rating=4,
    created_at=date(2024, 1, 8),
    updated_at=date(2024, 1, 18),
  ),
  Recipe(
    id=7,
    title="Pasta Carbonara",
    description="Classic Italian pasta",
    ingredients=[
      IngredientItem(name="Spaghetti", quantity="400g"),
      IngredientItem(name="Bacon", quantity="200g"),
      IngredientItem(name="Eggs", quantity="3"),
      IngredientItem(name="Parmesan Cheese", quantity="1 cup"),
      IngredientItem(name="Black Pepper", quantity="1 tsp"),
      IngredientItem(name="Salt", quantity="to taste"),
    ],
    instructions=[
      "Cook pasta in salted boiling water.",
      "Fry bacon until crispy, set aside.",
      "Whisk eggs with grated Parmesan and black pepper.",
      "Drain pasta, reserving 1 cup pasta water.",
      "Toss hot pasta with bacon.",
      "Remove from heat and add egg mixture, stirring quickly.",
      "Add pasta water as needed for creamy sauce.",
      "Serve immediately."
    ],
    prep_time=10,
    cook_time=12,
    servings=4,
    difficulty=Difficulty.MEDIUM,
    category=Category.DINNER,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474545/recipe_vault/kinjrjgo6n87mnrhzr1b.jpg",
    rating=5,
    created_at=date(2024, 1, 11),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=8,
    title="Lemonade",
    description="Refreshing homemade lemonade",
    ingredients=[
      IngredientItem(name="Fresh Lemons", quantity="5"),
      IngredientItem(name="Sugar", quantity="1 cup"),
      IngredientItem(name="Water", quantity="6 cups"),
      IngredientItem(name="Ice", quantity="as needed"),
      IngredientItem(name="Salt", quantity="pinch"),
    ],
    instructions=[
      "Squeeze lemons to get 1 cup juice.",
      "In a pitcher, combine sugar and 1 cup hot water, stir until dissolved.",
      "Add lemon juice, remaining cold water, and a pinch of salt.",
      "Stir well.",
      "Serve over ice with lemon slices."
    ],
    prep_time=10,
    cook_time=0,
    servings=4,
    difficulty=Difficulty.EASY,
    category=Category.BEVERAGE,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474548/recipe_vault/rtw1nrymucu739c1xvma.jpg",
    rating=4,
    created_at=date(2024, 1, 13),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=9,
    title="Brownies",
    description="Fudgy chocolate brownies",
    ingredients=[
      IngredientItem(name="All-Purpose Flour", quantity="1 cup"),
      IngredientItem(name="Cocoa Powder", quantity="3/4 cup"),
      IngredientItem(name="Dark Chocolate", quantity="150g"),
      IngredientItem(name="Butter", quantity="100g"),
      IngredientItem(name="Sugar", quantity="1.5 cups"),
      IngredientItem(name="Eggs", quantity="2"),
      IngredientItem(name="Vanilla Extract", quantity="1 tsp"),
      IngredientItem(name="Baking Powder", quantity="1/2 tsp"),
    ],
    instructions=[
      "Melt chocolate and butter together.",
      "Beat eggs with sugar until creamy.",
      "Stir in melted chocolate and vanilla.",
      "Mix flour, cocoa, and baking powder.",
      "Fold into egg mixture.",
      "Pour into greased 8x8 pan.",
      "Bake at 350°F for 25 minutes.",
      "Cool before cutting into squares."
    ],
    prep_time=15,
    cook_time=25,
    servings=12,
    difficulty=Difficulty.EASY,
    category=Category.DESERT,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474544/recipe_vault/i2rfjfx2gsaixpupjgpq.jpg",
    rating=5,
    created_at=date(2024, 1, 9),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=10,
    title="Caesar Salad",
    description="Crispy lettuce with Caesar dressing",
    ingredients=[
      IngredientItem(name="Romaine Lettuce", quantity="1 head"),
      IngredientItem(name="Parmesan Cheese", quantity="1/2 cup"),
      IngredientItem(name="Croutons", quantity="1 cup"),
      IngredientItem(name="Anchovies", quantity="3 fillets"),
      IngredientItem(name="Garlic", quantity="2 cloves"),
      IngredientItem(name="Lemon Juice", quantity="3 tbsp"),
      IngredientItem(name="Olive Oil", quantity="1/2 cup"),
      IngredientItem(name="Worcestershire Sauce", quantity="1 tsp"),
    ],
    instructions=[
      "Whisk minced garlic, anchovies, lemon juice, and Worcestershire sauce.",
      "Slowly whisk in olive oil.",
      "Tear lettuce into bite-sized pieces.",
      "Toss with dressing, croutons, and shaved Parmesan.",
      "Serve immediately."
    ],
    prep_time=15,
    cook_time=0,
    servings=2,
    difficulty=Difficulty.EASY,
    category=Category.LUNCH,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474545/recipe_vault/tta9d4c6ixagz7tpsnx2.jpg",
    rating=4,
    created_at=date(2024, 1, 16),
    updated_at=date(2024, 1, 19),
  ),
  Recipe(
    id=11,
    title="Puff Puff",
    description="Soft Puffy Delicious Puffs",
    ingredients=[
      IngredientItem(name="All-Purpose Flour", quantity="2 cups"),
      IngredientItem(name="Warm Milk", quantity="3/4 cup"),
      IngredientItem(name="Sugar", quantity="1/4 cup"),
      IngredientItem(name="Instant Yeast", quantity="1.5 tsp"),
      IngredientItem(name="Eggs", quantity="1"),
      IngredientItem(name="Salt", quantity="1/2 tsp"),
      IngredientItem(name="Vanilla Extract", quantity="1/2 tsp"),
      IngredientItem(name="Vegetable Oil", quantity="for frying"),
    ],
    instructions=[
      "Mix yeast with warm milk and 1 tbsp sugar, let sit 5 mins.",
      "Add flour, egg, salt, and vanilla.",
      "Beat until smooth, about 5 mins.",
      "Cover and let rise 30 mins.",
      "Heat oil to 350°F.",
      "Drop spoonfuls of batter into hot oil, fry until golden (2-3 mins per side).",
      "Drain on paper towels.",
      "Dust with sugar and serve warm."
    ],
    prep_time=40,
    cook_time=15,
    servings=8,
    difficulty=Difficulty.EASY,
    category=Category.SNACK,
    image_url="https://res.cloudinary.com/dfzpvawqz/image/upload/v1769474550/recipe_vault/z7bvbfdekfb7ac21ooit.jpg",
    rating=5,
    created_at=date(2024, 1, 23),
    updated_at=date(2024, 1, 24),
  )
]







async def get_db_session():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()


# db: Session = Depends(get_db_session)


import json

@app.on_event("startup")
def init_db():
    # DEV ONLY: wipe tables so you see updates
    # database_models.Base.metadata.drop_all(bind=engine) # This wipes the table
    database_models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(database_models.Recipe).first():
           return # Data already exists
        

        for recipe in RECIPES:
            data = recipe.model_dump()

            # relationship list
            ingredients_data = data.pop("ingredients", [])

            # ---- FIX TYPES FOR DB INSERT ----
            # enums -> string values
            if hasattr(data.get("difficulty"), "value"):
                data["difficulty"] = data["difficulty"].value
            if hasattr(data.get("category"), "value"):
                data["category"] = data["category"].value

            # HttpUrl -> string
            if data.get("image_url") is not None:
                data["image_url"] = str(data["image_url"])

            # instructions must be a real list, not a JSON string
            # If it's accidentally a string like '["step1","step2"]', convert it back.
            if isinstance(data.get("instructions"), str):
                try:
                    data["instructions"] = json.loads(data["instructions"])
                except Exception:
                    # fallback: treat as single step
                    data["instructions"] = [data["instructions"]]

            # create recipe row
            db_recipe = database_models.Recipe(**data)

            # attach ingredient ORM objects
            db_recipe.ingredients = [
                database_models.Ingredient(**ing) for ing in ingredients_data
            ]

            db.add(db_recipe)

        db.commit()
    finally:
        db.close()




@app.get("/")
def welcome():
  return {"Hello": "Welcome to RecipeVault Backend 😁"}




# PYTHON LIST GET ALL ENDPOINT
# @app.get("/recipes")
# async def get_recipes():
#   return RECIPES





 # DATABASE GET RECIPES ENDPOINT

@app.get("/recipes")
async def get_recipes(db: Session = Depends(get_db_session)):
  data_exists = db.query(database_models.Recipe).all()
  if not data_exists:
    raise HTTPException(status_code=404, detail="No Reciptes Found")
  return  data_exists





# PYTHON LIST GET BY ID ENDPOINT
# @app.get("/recipes/{recipe_id}")
# async def get_recipe_by_id(recipe_id: int):
#   recipe = next((b for b in RECIPES if b.id == recipe_id), None)
#   if recipe is None:
#     raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found")
#   return recipe




 # DATABASE GET RECIPES BY ID ENDPOINT

@app.get("/recipes/{recipe_id}")
async def get_recipe_by_id(recipe_id: int, db: Session = Depends(get_db_session)):
  db_recipe = db.query(database_models.Recipe).filter(database_models.Recipe.id == recipe_id).first()
  if not db_recipe:
      raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found")
  return db_recipe




# PYTHON LIST ADD(POST) ENDPOINT

# @app.post("/recipes")
# def add_recipe(recipe: Recipe):
#   exists= any(r.id == recipe.id for r in RECIPES) # This works because now we are checking through the ENTIRE list if something is True/exists

#     # if not RECIPES[b].id == recipe.id: # Don't use this statement, it allows duplicates
#   if exists:
#     raise HTTPException(status_code=400, detail=f"Recipe {recipe.id} Already Exists")
#   RECIPES.append(recipe)
#   return {"message": f"{recipe.title} added successfully", "recipe": recipe}



  # exists = db.query(database_models.Recipe).filter(database_models.Recipe.id == recipe.id).first()
  # if exists:
  #   raise HTTPException(status_code=400, detail=f"Recipe {recipe.id} Already Exists")
  # # new_recipe = database_models.Recipe(**recipe.model_dump())
  # # db.add(new_recipe)
  # # db.commit()
  # # db.refresh(new_recipe)

  # The above won't work because it is actually a Nested Model


 # DATABASE POST RECIPES ENDPOINT

@app.post("/recipes")
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db_session)):
  try:
    data = recipe.model_dump()
    ingredient_data = data.pop("ingredients", [])
    
    # ✅ convert enums to their string values
    if hasattr(data.get("difficulty"), "value"):
        data["difficulty"] = data["difficulty"].value
    if hasattr(data.get("category"), "value"):
        data["category"] = data["category"].value

    # ✅ convert HttpUrl to string
    if data.get("image_url") is not None:
        data["image_url"] = str(data["image_url"])

    new_recipe = database_models.Recipe(**data)
    new_recipe.ingredients = [
      database_models.Ingredient(**ing) for ing in ingredient_data
    ]
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return {"message": f"{new_recipe.title} added successfully", "recipe": new_recipe}
  except Exception as e:
     print("Create Recipe Error:", repr(e))
     raise HTTPException(status_code=500, detail=str(e))

    


# PYTHON LIST UPDATE ENDPOINT


# @app.put("/recipes/{recipe_id}")
# def update_recipe(recipe_id: int, recipe: Recipe):
#   for i in range(len(RECIPES)):
#     if RECIPES[i].id == recipe_id:
#       RECIPES[i] = recipe
#       recipe.id = recipe_id # Keep ID consistent
#       return {"Message": f"Recipe {RECIPES[i].id} Updated Successfully!"}
#   raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found, Update Failed!")


# 



 # DATABASE UPDATE RECIPES - ENDPOINT

@app.put("/recipes/{recipe_id}")
def updated_recipes(recipe_id: int, recipe:Recipe, db: Session = Depends(get_db_session)):
  db_recipe_exists = db.query(database_models.Recipe).filter(database_models.Recipe.id == recipe_id).first()
  if not db_recipe_exists: # Treating None value pairs first
    raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found, Update Failed!")
  data = recipe.model_dump() # First dump the recipe in an object for easier manipulation
  ingredients_data = data.pop("ingredients", []) # Pop out the ORM Table value that is related(connected) to the Pydantic Model we dumped --> Recipe

  for key, value in data.items():
    setattr(db_recipe_exists, key, value) # Update the values of the parameter(recipe) assigned to "db_recipe_exists)"

  db_recipe_exists.ingredients = [
    database_models.Ingredient(**b) for b in ingredients_data # And then take the table value of "ingredients_data" and assign it to it's actual table
  ]

  db.commit()
  db.refresh(db_recipe_exists)
  return {"message": f"{db_recipe_exists.title} Updated Successfully"}



# PYTHON LIST DELETE ENDPOINT

# @app.delete("/recipes/{recipe_id}")
# def delete_recipe(recipe_id: int):
#   for i in range(len(RECIPES)):
#     if RECIPES[i].id == recipe_id:
#       del RECIPES[i]
#       return {"Message": f"Recipe {recipe_id} Has Been Deleted Successfully"}
#   raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found")




 # DATABASE DELETE RECIPES - ENDPOINTS

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db_session)):
  recipe_exists = db.query(database_models.Recipe).filter(database_models.Recipe.id == recipe_id).first()
  if not recipe_exists:
    raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} Not Found, Delete Failed!")
  db.delete(recipe_exists)
  db.commit()
  return {"message": f"{recipe_exists.title} Deleted Successfully"}






# CLOUDINARY IMAGE ENDPOINT
@app.post("/recipes/{recipe_id}/image")
def upload_recipe_image(
    recipe_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session)
):
  
  db_recipe = db.query(database_models.Recipe).filter(database_models.Recipe.id == recipe_id).first()

  if not db_recipe:
    raise HTTPException(status_code=404, detail="Recipe not found")
  result = cloudinary.uploader.upload(file.file, folder="recipe_vault")
  db_recipe.image_url = result["secure_url"]

  db.commit()
  db.refresh(db_recipe)
  return {"image_url": db_recipe.image_url}