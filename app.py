from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_relative', methods=['POST'])
def add_relative():
    data = request.form
    # You should process and store the data in the database
    database.add_relative(data)
    return jsonify(success=True)

@app.route('/get_family_trees')
def get_family_trees():
    people = database.fetch_all_people()
    family_tree_roots = database.build_trees(people)
    return jsonify([database.serialize_tree(root) for root in family_tree_roots])

if __name__ == '__main__':
    database.setup()
    app.run(debug=True)
