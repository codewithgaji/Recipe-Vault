from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey


Base = declarative_base()

class Recipe(Base):
  __table_name__ = "recipes"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  instructions = Column(String)
  prep_time = Column(Integer)
  cook_time = Column(Integer)
  servings = Column(Integer)
  difficulty = Column(String) 
  category = Column(String)
  image_url = Column(String)
  rating = Column(Integer)
  created_at =Column(Date)
  updated_at = Column(Date)

  # This creates an "ingredient column in Recipe and then 'back_populates' meaning it takes the connection to the 'recipe' table in db. 

  # It also shows the relationship of "ingredient" column with the "Ingredient" table
  ingredients = relationship(
    "Ingredient", 
    back_populates="recipe",
    cascade="all, delete_orphan" # To delete all fields connected to the Ingredients column
  )




  # In RDBMS we don't use Nested Tables, hence the reason for seperate table. - DATABASE NORMALIZATION

  class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True) # Every ingredient has it's own PK
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE")) # The Link with the "recipes" table, to Link the Id to the recipes.id. CASCADE to delete with all fields
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")