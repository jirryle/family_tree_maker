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
            death_date TEXT,
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
                INSERT INTO relatives (name, gender, birth_date, death_date, photo_url, father_id, mother_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', ("Me", "Gender", "Birth Date", "Death Date", "Photo URL", None, None))
    conn.commit()
    conn.close()

def add_father(node_id, name, gender, birth_date, death_date, photo_url):
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
            SET name = ?, gender = ?, birth_date = ?, death_date = ?, photo_url = ?
            WHERE id = ?
        ''', (name, gender, birth_date, death_date, photo_url, existing_father_id[0]))
        else:
            # Step 2: Insert the new father node
            cursor.execute('''
                INSERT INTO relatives (name, gender, birth_date, death_date, photo_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, gender, birth_date, death_date, photo_url))

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

def add_mother(node_id, name, gender, birth_date, death_date, photo_url):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Step 1: Check if the child already has a mother_id set
        cursor.execute('SELECT mother_id FROM relatives WHERE id = ?', (node_id,))
        existing_mother_id = cursor.fetchone()
        if existing_mother_id and existing_mother_id[0]:
            # Handle the case where a mother already exists (e.g., return an error or update the existing mother)
            cursor.execute('''
            UPDATE relatives
            SET name = ?, gender = ?, birth_date = ?, death_date = ?, photo_url = ?
            WHERE id = ?
        ''', (name, gender, birth_date, death_date, photo_url, existing_mother_id[0]))
        else:
            # Step 2: Insert the new mother node
            cursor.execute('''
                INSERT INTO relatives (name, gender, birth_date, death_date, photo_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, gender, birth_date, death_date, photo_url))

            # Get the ID of the newly inserted mother
            new_mother_id = cursor.lastrowid

            # Step 3: Update the child's mother_id to reference the new mother's ID
            cursor.execute('''
                UPDATE relatives
                SET mother_id = ?
                WHERE id = ?
            ''', (new_mother_id, node_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return f"Failed to add mother: {e}"
    finally:
        conn.close()

    return "Mother added successfully"

def add_child(node_id, name, gender, birth_date, death_date, photo_url):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Obtain the parent's gender (for mother_id/father_id)
        cursor.execute('SELECT gender FROM relatives WHERE id = ?', (node_id))
        parent_gender = cursor.fetchone()[0]

        # Insert child node data into database
        cursor.execute('''
            INSERT INTO relatives (name, gender, birth_date, death_date, photo_url)
            VALUES (?, ?, ?, ?, ?)
                       ''', (name, gender, birth_date, death_date, photo_url))
        new_child_id = cursor.lastrowid

        # Update child's mother_id/father_id
        if parent_gender == 'Female':
            cursor.execute('''
                UPDATE relatives
                SET mother_id = ?
                WHERE id = ?
                    ''', (node_id, new_child_id))
        else:
            cursor.execute('''
                UPDATE relatives
                SET father_id = ?
                WHERE id = ?
                    ''', (node_id, new_child_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return f"Failed to add child: {e}"
    finally:
        conn.close()
    return "Child added successfully"

def edit_person(nodeId, name, gender, birth_date, death_date, photo_url):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE relatives
            SET name = ?, gender = ?, birth_date = ?, death_date = ?, photo_url = ?
            WHERE id = ?
                       ''', (name, gender, birth_date, death_date, photo_url, nodeId))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occured: {e}")
        return f"Failed to update person: {e}"
    finally:
        conn.close()
    return "Person updated successfully"

class Person:
    def __init__(self, id, name, gender, birth_date, death_date, photo_url, father_id=None, mother_id=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.death_date = death_date
        self.photo_url = photo_url
        self.father_id = father_id
        self.mother_id = mother_id
        self.children = []

def fetch_node_details(nodeId):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, gender, birth_date, death_date, photo_url FROM relatives WHERE id = ?', (nodeId))
    node_details = cursor.fetchall()[0]
    conn.close()
    return {
        "name" : node_details[0],
        "gender" : node_details[1],
        "birth_date" : node_details[2],
        "death_date" : node_details[3],
        "photo_url" : node_details[4]
    }

def fetch_all_people():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, gender, birth_date, death_date, photo_url, father_id, mother_id FROM relatives')
    people_data = cursor.fetchall()
    conn.close()
    return [Person(*data) for data in people_data]

def serialize_tree(person):
    # Check if the person has an 'children' attribute
    children = getattr(person, 'children', None)
    return {
        "id": person.id,
        "name": person.name,
        "gender": person.gender,
        "birth_date": person.birth_date,
        "death_date": person.death_date,
        "photo_url": person.photo_url,
        "father_id": person.father_id,
        "mother_id": person.mother_id,
        # Use a list comprehension to serialize children if they exist
        "children": [serialize_tree(child) for child in children] if children else [] 
    }

