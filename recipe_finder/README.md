# Recipe Finder Streamlit App

This web application, built with Streamlit, helps you find recipes based on the ingredients you have at home. It includes a "smart search" feature that can find recipes even if you are missing a few ingredients, and it will even suggest common substitutions!

## Features

-   **Interactive Interface:** Built with Streamlit for a clean and responsive user experience.
-   **Smart Search:** Finds recipes that are a close match to your ingredients.
-   **Ingredient Substitutions:** Suggests alternative ingredients if you're missing something.

## How to Use

### 1. Installation

First, clone the repository. Then, navigate to the project's root directory and install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 2. Running the Application

To start the application, run the following command from the project's root directory:

```bash
streamlit run streamlit_app.py
```

The application will open in your web browser.

### 3. Using the App

-   Once the app is running, you will see the user interface in your browser.
-   Enter the ingredients you have in the text box, separated by commas.
-   Click the "Find Recipes" button to see the results.
-   The results will show you "Perfect Matches" (where you have all ingredients) and "Close Matches" (where you are missing one or two ingredients).
-   For close matches, the app will list the missing ingredients and suggest possible substitutions.
