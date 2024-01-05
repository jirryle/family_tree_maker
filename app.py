from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_relative/<node_id>', methods=['POST'])
def add_relative(node_id):
    data = request.get_json()
    print("data from app.route is ", data)
    print("node id for child is ", node_id)
    if not data or 'relationship' not in data:
        return jsonify({"error": "Missing necessary data"}), 400

    try:
        # Common data extraction
        name = data['name']
        gender = data['gender']
        birthDate = data['birth_date']
        photoUrl = data['photo_url']
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
    return jsonify([database.serialize_tree(person) for person in people])

@app.route('/get_node_details/<nodeId>', methods=["GET"])
def get_node_details(nodeId):
    node_details = database.fetch_node_details(nodeId)
    return jsonify(node_details)

@app.route('/edit_person/<nodeId>', methods=['POST'])
def edit_person(nodeId):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing necessary data"}), 400
    try:
        # Extract data
        name = data['name']
        gender = data['gender']
        birth_date = data['birth_date']
        photo_url = data['photo_url']
        database.edit_person(nodeId, name, gender, birth_date, photo_url)
    except KeyError as e:
        return jsonify({"error": f"Missing data: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Person updated successfully"})

if __name__ == '__main__':
    database.setup()
    app.run(debug=True)
