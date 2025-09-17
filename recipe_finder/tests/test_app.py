import unittest
import sys
import os

# Add the parent directory to the path so we can import from logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic import find_recipes_smart

class TestSmartRecipeFinder(unittest.TestCase):

    def setUp(self):
        self.recipes = [
            {
                "name": "Pancakes",
                "ingredients": ["flour", "milk", "egg", "sugar"]
            },
            {
                "name": "Omelette",
                "ingredients": ["egg", "milk", "cheese", "salt", "pepper"]
            }
        ]
        self.substitutions = {
            "milk": ["almond milk", "soy milk"],
            "sugar": ["honey", "maple syrup"]
        }

    def test_exact_match(self):
        user_ingredients = ["flour", "milk", "egg", "sugar"]
        result = find_recipes_smart(self.recipes, user_ingredients, self.substitutions)
        self.assertEqual(len(result['exact_matches']), 1)
        self.assertEqual(result['exact_matches'][0]['name'], 'Pancakes')
        self.assertEqual(len(result['partial_matches']), 0)

    def test_partial_match_with_substitution(self):
        user_ingredients = ["flour", "egg", "sugar"] # Missing milk
        result = find_recipes_smart(self.recipes, user_ingredients, self.substitutions)
        self.assertEqual(len(result['exact_matches']), 0)
        self.assertEqual(len(result['partial_matches']), 1)

        partial_match = result['partial_matches'][0]
        self.assertEqual(partial_match['name'], 'Pancakes')
        self.assertEqual(partial_match['missing_ingredients'], ['milk'])
        self.assertIn('milk', partial_match['substitutions'])
        self.assertEqual(partial_match['substitutions']['milk'], ["almond milk", "soy milk"])

    def test_partial_match_without_substitution(self):
        user_ingredients = ["milk", "egg", "sugar"] # Missing flour
        result = find_recipes_smart(self.recipes, user_ingredients, self.substitutions)
        self.assertEqual(len(result['exact_matches']), 0)
        self.assertEqual(len(result['partial_matches']), 1)

        partial_match = result['partial_matches'][0]
        self.assertEqual(partial_match['name'], 'Pancakes')
        self.assertEqual(partial_match['missing_ingredients'], ['flour'])
        self.assertNotIn('flour', partial_match['substitutions'])

    def test_no_match(self):
        user_ingredients = ["beef", "carrots"]
        result = find_recipes_smart(self.recipes, user_ingredients, self.substitutions)
        self.assertEqual(len(result['exact_matches']), 0)
        self.assertEqual(len(result['partial_matches']), 0)

    def test_match_with_extra_ingredients(self):
        user_ingredients = ["flour", "milk", "egg", "sugar", "baking powder"]
        result = find_recipes_smart(self.recipes, user_ingredients, self.substitutions)
        self.assertEqual(len(result['exact_matches']), 1)
        self.assertEqual(result['exact_matches'][0]['name'], 'Pancakes')

if __name__ == '__main__':
    unittest.main()
