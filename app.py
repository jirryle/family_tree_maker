from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_relative', methods=['POST'])
def add_relative():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    #Validate that all required fields are present
    required_fields = ['name', 'gender', 'birth_date', 'photo_url', 'father_id', 'mother_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    database.add_relative(data)
    return jsonify("Relative added successfully")

@app.route('/get_family_trees')
def get_family_trees():
    people = database.fetch_all_people()
    family_tree_roots = database.build_trees(people)
    return jsonify([database.serialize_tree(root) for root in family_tree_roots])

if __name__ == '__main__':
    database.setup()
    app.run(debug=True)
