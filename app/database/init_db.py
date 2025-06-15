import asyncio
import json
from app.database.database import database, metadata, engine
from app.database.recipe_table import recipe_table


async def seed_data():
    metadata.drop_all(engine)
    metadata.create_all(engine)

    with open("app/database/mock_data.json") as f:
        data = json.load(f)

    await database.connect()

    for recipe in data:
        flat_recipe = {
            "id": recipe["id"],
            "name": recipe["name"],
            "portions": recipe["portions"],
            "ingredients": json.dumps(recipe["ingredients"]),
        }
        await database.execute(query=recipe_table.insert(), values=flat_recipe)

    await database.disconnect()
    print("Seeded database with recipes.")


if __name__ == "__main__":
    asyncio.run(seed_data())
