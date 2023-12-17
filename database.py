import sqlite3

from flask import app, jsonify

DATABASE_NAME = "family_tree.db"

def setup():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatives (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            birth_date TEXT,
            photo_url TEXT,
            father_id INTEGER,
            mother_id INTEGER,
            FOREIGN KEY (father_id) REFERENCES relatives (id),
            FOREIGN KEY (mother_id) REFERENCES relatives (id)
        )
    ''')
    conn.commit()
    conn.close()

def add_relative(data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO relatives (name, gender, birth_date, photo_url, father_id, mother_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['gender'], data['birth_date'], data['photo_url'], data['father_id'], data['mother_id']))
    conn.commit()
    conn.close()

class Person:
    def __init__(self, id, name, gender, birth_date, photo_url, father_id=None, mother_id=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.photo_url = photo_url
        self.father_id = father_id
        self.mother_id = mother_id
        self.children = []

def fetch_all_people():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, gender, birth_date, photo_url, father_id, mother_id FROM relatives')
    people_data = cursor.fetchall()
    conn.close()
    return [Person(*data) for data in people_data]

def build_trees(people):
    people_dict = {person.id: person for person in people}
    roots = [person for person in people if person.father_id is None and person.mother_id is None]

    for person in people:
        if person.father_id:
            father = people_dict.get(person.father_id)
            if father:
                father.children.append(person)
        if person.mother_id:
            mother = people_dict.get(person.mother_id)
            if mother:
                mother.children.append(person)
    return roots

def serialize_tree(person):
    return {
        "id": person.id,
        "name": person.name,
        "gender": person.gender,
        "birth_date": person.birth_date,
        "photo_url": person.photo_url,
        "father_id": person.father_id,
        "mother_id": person.mother_id,
        "children": [serialize_tree(child) for child in person.children] 
    }

def serialize_trees(roots):
    return [serialize_tree(root) for root in roots]

@app.route('/get_family_trees')
def get_family_trees():
    people = database.fetch_all_people()
    family_tree_roots = build_trees(people)
    return jsonify([serialize_tree(root) for root in family_tree_roots])