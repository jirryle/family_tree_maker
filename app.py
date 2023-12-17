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

if __name__ == '__main__':
    database.setup()
    app.run(debug=True)
