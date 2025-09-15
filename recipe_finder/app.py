import json

def load_recipes(filepath):
    """Loads recipes from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def find_matching_recipes(recipes, user_ingredients):
    """Finds recipes that can be made with the given ingredients."""
    matching_recipes = []
    for recipe in recipes:
        if all(ingredient in user_ingredients for ingredient in recipe['ingredients']):
            matching_recipes.append(recipe)
    return matching_recipes

def main():
    """Main function to run the recipe finder app."""
    recipes = load_recipes('recipes.json')

    print("Welcome to the Recipe Finder!")
    user_input = input("Enter the ingredients you have (separated by commas): ")
    user_ingredients = [item.strip().lower() for item in user_input.split(',')]

    matching_recipes = find_matching_recipes(recipes, user_ingredients)

    if matching_recipes:
        print("\nHere are the recipes you can make:")
        for recipe in matching_recipes:
            print(f"\n- {recipe['name']}")
            print(f"  Instructions: {recipe['instructions']}")
    else:
        print("\nSorry, no recipes found with the ingredients you have.")

if __name__ == "__main__":
    main()
