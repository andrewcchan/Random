import json

def load_recipes(filepath):
    """Loads recipes from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def load_substitutions(filepath):
    """Loads substitutions from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def find_recipes_smart(recipes, user_ingredients, substitutions, missing_threshold=2):
    """
    Finds recipes that can be made with the given ingredients, allowing for a
    certain number of missing ingredients and suggesting substitutions.
    """
    exact_matches = []
    partial_matches = []

    for recipe in recipes:
        recipe_ingredients = set(recipe['ingredients'])
        user_ingredients_set = set(user_ingredients)

        missing_ingredients = list(recipe_ingredients - user_ingredients_set)

        if not missing_ingredients:
            exact_matches.append(recipe)
        elif len(missing_ingredients) <= missing_threshold:
            # It's a partial match
            recipe_suggestion = recipe.copy()
            recipe_suggestion['missing_ingredients'] = missing_ingredients

            # Find substitutions for missing ingredients
            subs_for_recipe = {}
            for item in missing_ingredients:
                if item in substitutions:
                    subs_for_recipe[item] = substitutions[item]
            recipe_suggestion['substitutions'] = subs_for_recipe

            partial_matches.append(recipe_suggestion)

    return {
        'exact_matches': exact_matches,
        'partial_matches': partial_matches
    }
