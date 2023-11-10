from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

# Route 1: Make the API into json format to be more understandable
@app.route('/')
def dog_data():
    dog_response = requests.get("https://dogapi.dog/api/v2/breeds")
    all_dog_data = dog_response.json()
    return all_dog_data

# Route 2: List out all the names of the dog in the data
@app.route('/dog_names')
def all_dog_names():
    breeds_data = dog_data()

    # Extracting names from the data
    dog_names = []
    for breed in breeds_data['data']:
        dog_names.append(breed.get('attributes').get('name'))
    return jsonify({'dog_names': dog_names})

# Route 3: This route will return a random dog name from the list of dog names.
@app.route('/random_dog_name')
def random_dog_name():
    breeds_data = dog_data()

    # Extracting names from the data using a for loop
    dog_names = []
    for breed in breeds_data['data']:
        dog_names.append(breed.get('attributes').get('name'))

    # Choosing a random name from the list
    random_name = random.choice(dog_names)

    return jsonify({'random_dog_name': random_name})

# Route 4: List Names and Descriptions of All Dogs
@app.route('/all_dog_descriptions')
def all_dog_descriptions():
    # Fetch dog breed data from the external API
    breeds_data = dog_data()

    # Create a list to store dictionaries containing name and description for each dog
    dog_descriptions = []

    # Loop through breeds_data to gather names and descriptions for all dogs
    for breed in breeds_data['data']:
        name = breed.get('attributes').get('name')
        description = breed.get('attributes').get('description')
        dog_info = {'name': name, 'description': description}
        dog_descriptions.append(dog_info)

    # Return the list of dictionaries in JSON format
    return jsonify({'all_dog_descriptions': dog_descriptions})


# Route 5: Dog Description by Name
@app.route('/all_dog_descriptions/<name>')
def dog_description_by_name(name):
    # Fetch dog breed data from the external API
    breeds_data = dog_data()

    # Loop through breeds_data to find the breed with the specified name
    for breed in breeds_data.get('data'):
        if breed.get('attributes').get('name') == name:
            description = breed.get('attributes').get('description')
            break

    if description:
        # Return the description in JSON format
        return jsonify({'dog_description': description})
    else:
        # Return an error message if the dog breed is not found
        return jsonify({'error': 'Dog breed not found'})

if __name__ == "__main__":
    app.run(debug=True)