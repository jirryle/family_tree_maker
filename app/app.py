from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import database
from .models import db
import os

# Create application
def create_app(test_config=None):
    app = Flask(__name__)

    database_uri = os.getenv('DATABASE_URL')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri.replace("://", "ql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()
        database.insert_initial_data()

    # Register the routes with the app instance
    register_routes(app)
    return app


def register_routes(app):
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
            birthDate = data['birth_date']
            deathDate = data['death_date']
            photoUrl = data['photo_url']
            relationship = data['relationship']

            # Call different functions based on relationship type
            if relationship == 'Father':
                database.add_father(node_id, name, gender, birthDate, deathDate, photoUrl)
            elif relationship == 'Mother':
                database.add_mother(node_id, name, gender, birthDate, deathDate, photoUrl)
            elif relationship == 'Child':
                database.add_child(node_id, name, gender, birthDate, deathDate, photoUrl)
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
        return jsonify(people)

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
            death_date = data['death_date']
            photo_url = data['photo_url']
            database.edit_person(nodeId, name, gender, birth_date, death_date, photo_url)
        except KeyError as e:
            return jsonify({"error": f"Missing data: {e}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify({"message": "Person updated successfully"})
    
app = create_app()
if __name__ == '__main__':
    app.run()