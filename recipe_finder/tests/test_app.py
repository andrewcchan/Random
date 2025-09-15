import unittest
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import find_matching_recipes

class TestRecipeFinder(unittest.TestCase):

    def setUp(self):
        self.recipes = [
            {
                "name": "Spaghetti Carbonara",
                "ingredients": ["spaghetti", "eggs", "parmesan cheese", "pancetta", "black pepper"]
            },
            {
                "name": "Scrambled Eggs",
                "ingredients": ["eggs", "butter", "milk", "salt", "pepper"]
            }
        ]

    def test_find_one_recipe(self):
        user_ingredients = ["eggs", "butter", "milk", "salt", "pepper"]
        matches = find_matching_recipes(self.recipes, user_ingredients)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'Scrambled Eggs')

    def test_find_no_recipes(self):
        user_ingredients = ["flour", "sugar"]
        matches = find_matching_recipes(self.recipes, user_ingredients)
        self.assertEqual(len(matches), 0)

    def test_find_with_extra_ingredients(self):
        user_ingredients = ["eggs", "butter", "milk", "salt", "pepper", "bacon"]
        matches = find_matching_recipes(self.recipes, user_ingredients)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'Scrambled Eggs')

    def test_find_with_missing_ingredients(self):
        user_ingredients = ["eggs", "butter", "milk"]
        matches = find_matching_recipes(self.recipes, user_ingredients)
        self.assertEqual(len(matches), 0)

if __name__ == '__main__':
    unittest.main()
