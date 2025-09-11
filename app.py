from socket import gethostname
import sqlite3
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

def initDB():
    # Initialize database and create table if it doesn't exist
    conn = sqlite3.connect('items.db')  # this will create 'items.db' if it doesn't exist
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    # Insert some sample data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO items (name) VALUES ('Sample Item 1')")
        cursor.execute("INSERT INTO items (name) VALUES ('Sample Item 2')")
        cursor.execute("INSERT INTO items (name) VALUES ('Sample Item 3')")
        conn.commit()
    conn.close()


@app.route('/')
def home():
    return "HELLO WORLD"

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    # Validate input
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing "name" in request data'}), 400

    name = data['name']

    # Insert into database
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()

    # Get the ID of the new item
    item_id = cursor.lastrowid
    conn.close()

    new_item = {'id': item_id, 'name': name}
    return jsonify(new_item), 201

# Define the GET /items endpoint
@app.route('/items', methods=['GET'])
def get_items():
    # Connect to the database and fetch all items
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    conn.close()
    # Convert the query result into a list of dictionaries
    items = []
    for row in rows:
        items.append({"id": row[0], "name": row[1]})
    # Return the list of items as JSON
    return jsonify(items)

if __name__ == '__main__':
    initDB()
    if 'liveconsole' not in gethostname():
        app.run()