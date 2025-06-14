from sqlalchemy import Table, Column, String, Float
from app.database.database import metadata

recipe_table = Table(
    "recipes",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("portions", Float, nullable=False),
    Column("ingredients", String, nullable=False),
)
