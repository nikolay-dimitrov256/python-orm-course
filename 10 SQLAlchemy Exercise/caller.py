from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Recipe, Chef
from helpers import session_handler

CONNECTION_STRING = 'postgresql+psycopg2://postgres:admin@localhost/sqlalchemy_exercise'
engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)

session = Session()


@session_handler(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
    session.add(recipe)


@session_handler(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str) -> int:
    # bulk update in one query
    records_changed: int = (
        session.query(Recipe)
        .filter_by(name=name)
        .update({
            Recipe.name: new_name,
            Recipe.ingredients: new_ingredients,
            Recipe.instructions: new_instructions
        })
    )

    return records_changed


@session_handler(session)
def delete_recipe_by_name(name: str) -> int:
    # DELETE FROM recipes WHERE name = <name>
    deleted_records: int = session.query(Recipe).filter_by(name=name).delete()

    return deleted_records


@session_handler(session, autoclose=False)
def get_recipes_by_ingredient(ingredient_name: str) -> list:
    found_recipes = session.query(Recipe).filter(Recipe.ingredients.ilike(f'%{ingredient_name}%')).all()

    return found_recipes


@session_handler(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str) -> None:
    first_recipe = (
        session.query(Recipe)
        .filter_by(name=first_recipe_name)
        .with_for_update()
        .one()
    )
    second_recipe = (
        session.query(Recipe)
        .filter_by(name=second_recipe_name)
        .with_for_update()
        .one()
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@session_handler(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()

    if recipe and recipe.chef_id:
        raise Exception(f'Recipe: {recipe_name} already has a related chef')

    chef = session.query(Chef).filter_by(name=chef_name).first()

    recipe.chef = chef

    return f'Related recipe {recipe_name} with chef {chef_name}'


@session_handler(session)
def get_recipes_with_chef() -> str:
    recipes = (
        session.query(Recipe.name, Chef.name)
        .join(Chef, Recipe.chef)
        .all()
    )

    result = [f'Recipe: {recipe_name} made by chef: {chef_name}' for recipe_name, chef_name in recipes]

    return '\n'.join(result)


recipes = [
    ('Spaghetti Carbonara', 'Pasta, Eggs, Pancetta, Cheese', 'Cook the pasta, mix it with eggs, pancetta, and cheese'),
    ('Chicken Stir-Fry', 'Chicken, Bell Peppers, Soy Sauce, Vegetables', 'Stir-fry chicken and vegetables with soy sauce'),
    ('Caesar Salad', 'Romaine Lettuce, Croutons, Caesar Dressing', 'Toss lettuce with dressing and top with croutons'),
]
