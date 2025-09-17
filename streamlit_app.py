import streamlit as st
import sys
import os

# Add the recipe_finder directory to the path to import logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'recipe_finder')))
from logic import load_recipes, load_substitutions, find_recipes_smart

# --- Page Configuration ---
st.set_page_config(
    page_title="Recipe Finder",
    page_icon="🍳",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data
def get_data():
    recipes = load_recipes('recipe_finder/recipes.json')
    substitutions = load_substitutions('recipe_finder/substitutions.json')
    return recipes, substitutions

recipes, substitutions = get_data()

# --- UI Layout ---
st.title("🍳 Recipe Finder")
st.write("Find recipes based on the ingredients you have at home. You can also find recipes you're close to making!")

ingredients_input = st.text_area(
    "Enter your ingredients, separated by commas:",
    placeholder="e.g., flour, sugar, eggs"
)

if st.button("Find Recipes"):
    if ingredients_input:
        user_ingredients = [item.strip().lower() for item in ingredients_input.split(',')]

        found_recipes = find_recipes_smart(recipes, user_ingredients, substitutions)

        st.header("Results")

        if not found_recipes['exact_matches'] and not found_recipes['partial_matches']:
            st.warning("No recipes found with your ingredients.")
        else:
            if found_recipes['exact_matches']:
                st.subheader("Perfect Matches!")
                for recipe in found_recipes['exact_matches']:
                    with st.expander(f"{recipe['name']}"):
                        st.write(f"**Instructions:** {recipe['instructions']}")

            if found_recipes['partial_matches']:
                st.subheader("Close Matches!")
                for recipe in found_recipes['partial_matches']:
                    with st.expander(f"{recipe['name']}"):
                        st.write(f"**Instructions:** {recipe['instructions']}")
                        st.info(f"**Missing:** {', '.join(recipe['missing_ingredients'])}")
                        if recipe['substitutions']:
                            for item, subs in recipe['substitutions'].items():
                                st.success(f"**For {item}, you could use:** {', '.join(subs)}")
    else:
        st.error("Please enter some ingredients.")
