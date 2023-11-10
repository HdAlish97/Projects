from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

# Route 1: Make the API into json format to be more understandable
@app.route('/')
def meal_data():
    # Make a request to the meal database API and return the JSON data
    meal_response = requests.get("https://www.themealdb.com/api/json/v1/1/search.php?f=a")
    all_meal_data = meal_response.json()
    return all_meal_data

# Route 2: List all desserts with their respective instructions
@app.route('/desserts')
def all_desserts():
    # Get meal data
    desserts_data = meal_data()
    
    # Create a list of dictionaries containing dessert name and description
    dessert_info_list = []
    for dessert in desserts_data['meals']:
        name = dessert.get('strMeal')
        description = dessert.get('strInstructions')
        dessert_info = {'name': name, 'description': description}
        dessert_info_list.append(dessert_info)

    # Return the list of desserts in JSON format
    return jsonify({'all_desserts': dessert_info_list})

# Route 3: Get Random Dessert
@app.route('/random_dessert')
def random_dessert():
    desserts_data = meal_data()

    # Choose a random dessert
    random_dessert = random.choice(desserts_data['meals'])

    # Extract name and instructions
    dessert_name = random_dessert.get('strMeal')
    instructions = random_dessert.get('strInstructions')

    return jsonify({'dessert_name': dessert_name, 'instructions': instructions})

# Route 4: Get Dessert Ingredients by Name
@app.route('/dessert_ingredients/<dessert_name>')
def dessert_ingredients(dessert_name):
    # Get meal data
    desserts_data = meal_data()

    # Search for the dessert by name
    for dessert in desserts_data['meals']:
        if dessert.get('strMeal') == dessert_name:
            # Create a list of ingredients for the dessert
            ingredients = []
            for i in range(1, 21):
                ingredient = dessert.get('strIngredient' + str(i))
                ingredients.append(ingredient)
            
            return jsonify({'dessert_name': dessert_name, 'ingredients': ingredients})

    # If the dessert is not found, return an error message
    return jsonify({'error': 'Dessert not found'})

if __name__ == "__main__":
    app.run(debug=True)
