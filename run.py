from flask import Flask, render_template, request
import sys
import os

# Add the recipe_finder directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'recipe_finder')))

# Now we can import from logic
from logic import load_recipes, load_substitutions, find_recipes_smart

app = Flask(__name__, template_folder='recipe_finder/templates', static_folder='recipe_finder/static')

# Load data once when the app starts
recipes = load_recipes('recipe_finder/recipes.json')
substitutions = load_substitutions('recipe_finder/substitutions.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form['ingredients']
    user_ingredients = [item.strip().lower() for item in user_input.split(',')]

    # Use the new smart search function
    found_recipes = find_recipes_smart(recipes, user_ingredients, substitutions)

    return render_template('results.html', recipes=found_recipes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
