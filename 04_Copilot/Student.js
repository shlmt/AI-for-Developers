class Student {
	constructor(name, age, facult) {
		this.name = name
		this.age = age
		this.grades = []
		this.facult = facult
	}

	calculateAverageGrade = () => {
		return this.grades.reduce((sum, grade) => sum + grade, 0) / this.grades.length
	}

	addGrade = (grade) => {
		if (grade < 0 || grade > 100) {
			throw new Error('Invalid grade. Grades should be between 0 and 100.')
		}
		this.grades.push(grade)
	}
}

class University {
	constructor(name, location, faculties) {
		this.name = name
		this.location = location
		this.faculties = faculties
		this.students = []
	}

	addStudent = (student) => {
		this.students.push(student)
	}

	getAverage = () => {
		return this.students.reduce((sum, student) => sum + student.calculateAverageGrade(), 0) / this.students.length
	}

	findBestStudent = () => {
		return this.students.reduce((best, student) =>
			student.calculateAverageGrade() > best.calculateAverageGrade() ? student : best
		)
	}
}
