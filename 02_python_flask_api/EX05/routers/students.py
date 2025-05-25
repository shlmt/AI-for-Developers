from flask import Blueprint, jsonify
from services.students import StudentsService

students_router = Blueprint('/students', __name__)

students_service = StudentsService()

@students_router.route('/', methods=['GET'])
def get_all_students():
    students = students_service.get_all_students()
    return jsonify(students)

@students_router.route('/<firstName>', methods=['GET'])
def get_student_by_firstname(firstName):
    students = students_service.get_student_by_firstname(firstName)
    if not students:
        return jsonify({"error": "students not found"})
    return jsonify(students)