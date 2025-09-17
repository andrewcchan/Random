# Recipe Finder Web App

This web application helps you find recipes based on the ingredients you have at home. It includes a "smart search" feature that can find recipes even if you are missing a few ingredients, and it will even suggest common substitutions!

## Features

-   **Web-based interface:** Easy to use in your browser.
-   **Smart Search:** Finds recipes that are a close match to your ingredients.
-   **Ingredient Substitutions:** Suggests alternative ingredients if you're missing something.

## How to Use

### 1. Installation

First, clone the repository. Then, navigate to the project's root directory and install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 2. Running the Application

To start the web server, run the following command from the project's root directory:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:8080` in your web browser.

### 3. Using the App

-   Open the web application in your browser.
-   Enter the ingredients you have in the text box, separated by commas.
-   Click "Find Recipes" to see the results.
-   The results will show you "Perfect Matches" (where you have all ingredients) and "Close Matches" (where you are missing one or two ingredients).
-   For close matches, the app will list the missing ingredients and suggest possible substitutions.
