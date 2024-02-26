from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from .models import db, Relative

def insert_initial_data():
    if not Relative.query.first():  # Check if the table is empty
        initial_relative = Relative(
            name="Me",
            gender="Gender",
            birth_date="Birth Date",
            death_date="Death Date",
            photo_url="Photo URL"
        )
        db.session.add(initial_relative)
        db.session.commit()

def add_father(node_id, name, gender, birth_date, death_date, photo_url):
    try:
        # Step 1: Fetch the child and check if a father is already associated
        child = Relative.query.get(node_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404

        if child.father_id:
            # Father already exists, update existing father details
            father = Relative.query.get(child.father_id)
            father.name = name
            father.gender = gender
            father.birth_date = birth_date
            father.death_date = death_date
            father.photo_url = photo_url
        else:
            # No existing father, create a new father record
            new_father = Relative(name=name, gender=gender, birth_date=birth_date, death_date=death_date, photo_url=photo_url)
            db.session.add(new_father)
            db.session.flush()  # This assigns an ID to new_father without committing the transaction
            child.father_id = new_father.id
        
        db.session.commit()
        return jsonify({"message": "Father added/updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def add_mother(node_id, name, gender, birth_date, death_date, photo_url):
    try:
        # Step 1: Fetch the child and check if a mother is already associated
        child = Relative.query.get(node_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404

        if child.mother_id:
            # Mother already exists, update existing father details
            mother = Relative.query.get(child.mother_id)
            mother.name = name
            mother.gender = gender
            mother.birth_date = birth_date
            mother.death_date = death_date
            mother.photo_url = photo_url
        else:
            # No existing mother, create a new mother record
            new_mother = Relative(name=name, gender=gender, birth_date=birth_date, death_date=death_date, photo_url=photo_url)
            db.session.add(new_mother)
            db.session.flush()  # This assigns an ID to new_father without committing the transaction
            child.mother_id = new_mother.id
        
        db.session.commit()
        return jsonify({"message": "Mother added/updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
def add_child(node_id, name, gender, birth_date, death_date, photo_url):
    try:
        # 1. Find parent object
        parent = Relative.query.get(node_id)
        if not parent:
            return jsonify({"error": "Parent not found"}), 404

        # 2. Create new child record
        new_child = Relative(name=name, gender=gender, birth_date=birth_date, death_date=death_date, photo_url=photo_url)

        # 3. Assign child's mother_id/father_id
        if parent.gender == 'Female':
            new_child.mother_id = parent.id
        else:
            new_child.father_id = parent.id

        db.session.add(new_child)
        db.session.commit()
        return jsonify({"message": "Child added/updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def edit_person(nodeId, name, gender, birth_date, death_date, photo_url):
    try:
        person = Relative.query.get(nodeId)
        if person is None:
            return jsonify({"error": "Person not found"}), 404

        person.name = name
        person.gender = gender
        person.birth_date = birth_date
        person.death_date = death_date
        person.photo_url = photo_url

        db.session.commit()
        return jsonify({"message": "Person updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def fetch_node_details(nodeId):
    person = Relative.query.get(nodeId)
    if person:
        return {
            "name": person.name,
            "gender": person.gender,
            "birth_date": person.birth_date,
            "death_date": person.death_date,
            "photo_url": person.photo_url
        }
    else:
        return None

def fetch_all_people():
    all_people = Relative.query.all()
    return [serialize_tree(person) for person in all_people]

def serialize_tree(person):
    return {
        "id": person.id,
        "name": person.name,
        "gender": person.gender,
        "birth_date": person.birth_date,
        "death_date": person.death_date,
        "photo_url": person.photo_url,
        "father_id": person.father_id,
        "mother_id": person.mother_id,
        "children": [serialize_tree(child) for child in person.children] if person.children else []
    }