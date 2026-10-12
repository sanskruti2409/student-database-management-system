# ====================================================================
# Project: Student Database Management System
# File: app.py
# Description: Main Flask application with routing, CRUD operations,
#              and parameterized PostgreSQL queries.
# ====================================================================

from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from db import get_db_connection

app = Flask(__name__)
# Secret key is required by Flask for session flash messages
app.secret_key = "student_db_secret_key_for_practice"

# --------------------------------------------------------------------
# 1. HOME DASHBOARD ROUTE
# Displays total count statistics and recent students
# --------------------------------------------------------------------
@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Count total students
        cur.execute("SELECT COUNT(*) AS total_students FROM students;")
        total_students = cur.fetchone()["total_students"]

        # Count total departments
        cur.execute("SELECT COUNT(*) AS total_departments FROM departments;")
        total_departments = cur.fetchone()["total_departments"]

        # Count total courses
        cur.execute("SELECT COUNT(*) AS total_courses FROM courses;")
        total_courses = cur.fetchone()["total_courses"]

        # Fetch 5 most recently enrolled students with their department names
        cur.execute("""
            SELECT s.student_id, s.first_name, s.last_name, s.email, 
                   s.enrollment_date, d.department_name
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.department_id
            ORDER BY s.student_id DESC
            LIMIT 5;
        """)
        recent_students = cur.fetchall()

        return render_template(
            "index.html",
            total_students=total_students,
            total_departments=total_departments,
            total_courses=total_courses,
            recent_students=recent_students
        )
    finally:
        cur.close()
        conn.close()

# --------------------------------------------------------------------
# 2. STUDENTS LIST & SEARCH ROUTE
# Displays all students, supports search by name or email
# --------------------------------------------------------------------
@app.route("/students")
def students():
    search_query = request.args.get("search", "").strip()
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        if search_query:
            # Parameterized search using ILIKE (case-insensitive in PostgreSQL)
            term = f"%{search_query}%"
            query = """
                SELECT s.student_id, s.first_name, s.last_name, s.email, 
                       s.phone, s.date_of_birth, s.enrollment_date, d.department_name
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.department_id
                WHERE s.first_name ILIKE %s 
                   OR s.last_name ILIKE %s 
                   OR s.email ILIKE %s
                ORDER BY s.student_id;
            """
            cur.execute(query, (term, term, term))
        else:
            # Return all students ordered by student_id
            query = """
                SELECT s.student_id, s.first_name, s.last_name, s.email, 
                       s.phone, s.date_of_birth, s.enrollment_date, d.department_name
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.department_id
                ORDER BY s.student_id;
            """
            cur.execute(query)

        student_list = cur.fetchall()
        return render_template("students.html", students=student_list, search_query=search_query)
    finally:
        cur.close()
        conn.close()

# --------------------------------------------------------------------
# 3. ADD STUDENT ROUTE
# GET: Displays the student creation form
# POST: Validates inputs and inserts a new student record
# --------------------------------------------------------------------
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        if request.method == "POST":
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip() or None
            date_of_birth = request.form.get("date_of_birth", "").strip() or None
            department_id = request.form.get("department_id", "").strip() or None

            # Server-side validation for required fields
            if not first_name or not last_name or not email:
                flash("First Name, Last Name, and Email are required.", "danger")
                # Reload departments for the form
                cur.execute("SELECT department_id, department_name FROM departments ORDER BY department_name;")
                departments = cur.fetchall()
                return render_template("add_student.html", departments=departments)

            # Insert student with parameterized values (prevents SQL Injection)
            insert_query = """
                INSERT INTO students (first_name, last_name, email, phone, date_of_birth, department_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            try:
                cur.execute(insert_query, (first_name, last_name, email, phone, date_of_birth, department_id))
                conn.commit()
                flash(f"Student '{first_name} {last_name}' was added successfully!", "success")
                return redirect(url_for("students"))
            except psycopg2.IntegrityError:
                conn.rollback()
                flash(f"Error: A student with email '{email}' already exists.", "danger")
                cur.execute("SELECT department_id, department_name FROM departments ORDER BY department_name;")
                departments = cur.fetchall()
                return render_template("add_student.html", departments=departments)

        # GET Request: Fetch available departments for dropdown
        cur.execute("SELECT department_id, department_name FROM departments ORDER BY department_name;")
        departments = cur.fetchall()
        return render_template("add_student.html", departments=departments)
    finally:
        cur.close()
        conn.close()

# --------------------------------------------------------------------
# 4. EDIT STUDENT ROUTE
# GET: Pre-populates the form with existing student details
# POST: Updates the student record in PostgreSQL
# --------------------------------------------------------------------
@app.route("/edit-student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        if request.method == "POST":
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip() or None
            date_of_birth = request.form.get("date_of_birth", "").strip() or None
            department_id = request.form.get("department_id", "").strip() or None

            if not first_name or not last_name or not email:
                flash("First Name, Last Name, and Email cannot be empty.", "danger")
                return redirect(url_for("edit_student", student_id=student_id))

            update_query = """
                UPDATE students
                SET first_name = %s, last_name = %s, email = %s, 
                    phone = %s, date_of_birth = %s, department_id = %s
                WHERE student_id = %s;
            """
            try:
                cur.execute(update_query, (first_name, last_name, email, phone, date_of_birth, department_id, student_id))
                conn.commit()
                flash(f"Student #{student_id} updated successfully!", "success")
                return redirect(url_for("students"))
            except psycopg2.IntegrityError:
                conn.rollback()
                flash(f"Error: Email '{email}' is already in use by another student.", "danger")
                return redirect(url_for("edit_student", student_id=student_id))

        # GET: Fetch existing student info
        cur.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
        student = cur.fetchone()

        if not student:
            flash("Student not found.", "danger")
            return redirect(url_for("students"))

        # Fetch departments for select dropdown
        cur.execute("SELECT department_id, department_name FROM departments ORDER BY department_name;")
        departments = cur.fetchall()

        return render_template("edit_student.html", student=student, departments=departments)
    finally:
        cur.close()
        conn.close()

# --------------------------------------------------------------------
# 5. DELETE STUDENT ROUTE
# Deletes a student record (with confirmation from frontend)
# --------------------------------------------------------------------
@app.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        conn.commit()
        flash(f"Student #{student_id} has been deleted successfully.", "info")
        return redirect(url_for("students"))
    except Exception as e:
        conn.rollback()
        flash(f"Failed to delete student: {str(e)}", "danger")
        return redirect(url_for("students"))
    finally:
        cur.close()
        conn.close()

# --------------------------------------------------------------------
# 6. COURSES LIST ROUTE
# Displays all courses, their department, and total enrolled students
# --------------------------------------------------------------------
@app.route("/courses")
def courses():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Multi-table query: courses + departments + count of enrollments
        query = """
            SELECT c.course_id, c.course_code, c.course_name, c.credits,
                   d.department_name,
                   COUNT(e.enrollment_id) AS enrolled_students
            FROM courses c
            JOIN departments d ON c.department_id = d.department_id
            LEFT JOIN enrollments e ON c.course_id = e.course_id
            GROUP BY c.course_id, c.course_code, c.course_name, c.credits, d.department_name
            ORDER BY c.course_code;
        """
        cur.execute(query)
        course_list = cur.fetchall()
        return render_template("courses.html", courses=course_list)
    finally:
        cur.close()
        conn.close()

# --------------------------------------------------------------------
# APPLICATION ENTRY POINT
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Runs the local development server at http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
