from flask import Flask, jsonify, request

app = Flask(__name__)

students = []

# HOME
@app.route('/')
def home():
    return "Flask REST API"

# GET DATA
@app.route('/students', methods=['GET'])
def get_students():

    return jsonify(students)

# INSERT DATA
@app.route('/students', methods=['POST'])
def add_student():

    data = request.json

    students.append(data)

    return jsonify({
        "message": "Student Added",
        "student": data
    })

# UPDATE DATA
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):

    for student in students:

        if student['id'] == id:

            student['name'] = request.json['name']

            return jsonify({
                "message": "Student Updated",
                "student": student
            })

    return jsonify({
        "message": "Student Not Found"
    })

# DELETE DATA
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    for student in students:

        if student['id'] == id:

            students.remove(student)

            return jsonify({
                "message": "Student Deleted"
            })

    return jsonify({
        "message": "Student Not Found"
    })

if __name__ == '__main__':
    app.run(debug=True)



