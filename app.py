from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
DB_CONFIG = {
    'host': '192.168.31.228',
    'user': 'lei',
    'password': 'Unitec123',
    'database': 'student_grades'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY last_name, first_name")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('students.html', students=students)
    else:
        flash('Database connection error')
        return render_template('students.html', students=[])

@app.route('/courses')
def courses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses ORDER BY course_code")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('courses.html', courses=courses)
    else:
        flash('Database connection error')
        return render_template('courses.html', courses=[])

@app.route('/grades')
def grades():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT g.grade_id, s.first_name, s.last_name, c.course_code, c.course_name, 
               g.grade, g.semester, g.year
        FROM grades g
        JOIN students s ON g.student_id = s.student_id
        JOIN courses c ON g.course_id = c.course_id
        ORDER BY s.last_name, s.first_name, c.course_code
        """
        cursor.execute(query)
        grades = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('grades.html', grades=grades)
    else:
        flash('Database connection error')
        return render_template('grades.html', grades=[])

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                """, (request.form['first_name'], request.form['last_name'], 
                      request.form['email'], request.form['enrollment_date']))
                conn.commit()
                flash('Student added successfully!')
                return redirect(url_for('students'))
            except Error as e:
                flash(f'Error adding student: {e}')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Database connection error')
    return render_template('add_student.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO courses (course_code, course_name, credits)
                VALUES (%s, %s, %s)
                """, (request.form['course_code'], request.form['course_name'], 
                      int(request.form['credits'])))
                conn.commit()
                flash('Course added successfully!')
                return redirect(url_for('courses'))
            except Error as e:
                flash(f'Error adding course: {e}')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Database connection error')
    return render_template('add_course.html')

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            try:
                cursor.execute("""
                INSERT INTO grades (student_id, course_id, grade, semester, year)
                VALUES (%s, %s, %s, %s, %s)
                """, (int(request.form['student_id']), int(request.form['course_id']),
                      float(request.form['grade']), request.form['semester'],
                      int(request.form['year'])))
                conn.commit()
                flash('Grade added successfully!')
                return redirect(url_for('grades'))
            except Error as e:
                flash(f'Error adding grade: {e}')
        
        # Get students and courses for dropdown
        cursor.execute("SELECT student_id, first_name, last_name FROM students ORDER BY last_name, first_name")
        students = cursor.fetchall()
        cursor.execute("SELECT course_id, course_code, course_name FROM courses ORDER BY course_code")
        courses = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('add_grade.html', students=students, courses=courses)
    else:
        flash('Database connection error')
        return render_template('add_grade.html', students=[], courses=[])

if __name__ == '__main__':
    app.run(debug=True)
