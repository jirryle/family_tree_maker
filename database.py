import sqlite3
from app import app
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
    # Check if the initial node has been created 
    cursor.execute('SELECT id FROM relatives')
    if cursor.fetchone() is None:
        # Insert the initial node
        cursor.execute('''
                INSERT INTO relatives (name, gender, birth_date, photo_url, father_id, mother_id)
                VALUES (?, ?, ?, ?, ?, ?)
                    ''', ("Me", "Gender", "Birth Date", "Photo URL", None, None))
    conn.commit()
    conn.close()

def add_father(node_id, name, gender, birth_date, photo_url):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Step 1: Check if the child already has a father_id set
        cursor.execute('SELECT father_id FROM relatives WHERE id = ?', (node_id,))
        existing_father_id = cursor.fetchone()

        if existing_father_id and existing_father_id[0]:
            # Handle the case where a father already exists (e.g., return an error or update the existing father)
            cursor.execute('''
            UPDATE relatives
            SET name = ?, gender = ?, birth_date = ?, photo_url = ?
            WHERE id = ?
        ''', (name, gender, birth_date, photo_url, existing_father_id))

        # Step 2: Insert the new father node
        cursor.execute('''
            INSERT INTO relatives (name, gender, birth_date, photo_url)
            VALUES (?, ?, ?, ?)
        ''', (name, gender, birth_date, photo_url))

        # Get the ID of the newly inserted father
        new_father_id = cursor.lastrowid

        # Step 3: Update the child's father_id to reference the new father's ID
        cursor.execute('''
            UPDATE relatives
            SET father_id = ?
            WHERE id = ?
        ''', (new_father_id, node_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return f"Failed to add father: {e}"
    finally:
        conn.close()

    return "Father added successfully"


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

