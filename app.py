from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

recipes = [
    {
        'id': 1,
        'name': 'Egg salad',
        'description': 'This is a lovely egg salad recipe.',
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This a lovely tomato pasta recipe.',
    }
]


@app.route('/recipes')
def get_recipes():  # put application's code here
    return jsonify({'data': recipes})


@app.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND


@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(recipe)
    return jsonify(recipe), HTTPStatus.CREATED


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND
    data = request.get_json()
    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )
    return jsonify(recipe), HTTPStatus.OK


@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    global recipes
    recipes = [recipe for recipe in recipes if recipe['id'] != recipe_id]
    return {'message': 'Recipe deleted.'}, HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
