from sqlalchemy import Table, Column, String, Float
from app.database.database import metadata

# File containing the schema for a recipe_table
#   -> id: Unique identifier for the recipe (string)
#   -> name: The name of the recipe (string)
#   -> portions: The name of the recipe (string). Can be a float (see assumptions.txt)
#   -> ingredients: A JSON stringified array consisting of type Ingredient


recipe_table = Table(
    "recipes",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("portions", Float, nullable=False),
    Column("ingredients", String, nullable=False),
)
