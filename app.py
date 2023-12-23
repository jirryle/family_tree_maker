from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_relative/<node_id>', methods=['POST'])
def add_relative(node_id):
    data = request.get_json()

    if not data or 'relationship' not in data:
        return jsonify({"error": "Missing necessary data"}), 400

    try:
        # Common data extraction
        name = data['name']
        gender = data['gender']
        birthDate = data['birthDate']
        photoUrl = data['photoUrl']
        relationship = data['relationship']

        # Call different functions based on relationship type
        if relationship == 'Father':
            database.add_father(node_id, name, gender, birthDate, photoUrl)
        elif relationship == 'Mother':
            database.add_mother(node_id, name, gender, birthDate, photoUrl)
        elif relationship == 'Child':
            database.add_child(node_id, name, gender, birthDate, photoUrl)
        else:
            return jsonify({"error": "Invalid relationship type"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing data: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Relative added successfully"})


@app.route('/get_family_trees')
def get_family_trees():
    people = database.fetch_all_people()
    family_tree_roots = database.build_trees(people)
    return jsonify([database.serialize_tree(root) for root in family_tree_roots])

if __name__ == '__main__':
    database.setup()
    app.run(debug=True)
