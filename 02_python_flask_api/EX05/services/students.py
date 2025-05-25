from pymongo import MongoClient

class StudentsService:
    def __init__(self):
        self.students = MongoClient(port=27017)['ai']['students']

    def get_all_students(self):
        return list(self.students.find({}))
        
    def get_student_by_firstname(self, first_name):
        return list(self.students.find({"firstName":first_name}))