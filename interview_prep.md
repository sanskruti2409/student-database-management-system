# Interview Questions & Answers Guide
## Student Database Management System
*Tailored for BCA & M.Sc. Computer Applications freshers applying for SQL Developer, Junior DBA, and Software Support roles.*

---

### Category 1: Project Overview & Architecture

#### Q1. Can you briefly describe your project?
**Answer:**
> "I developed a **Student Database Management System** using Python with Flask and PostgreSQL. It follows a clean 3-tier architecture: the PostgreSQL database stores academic data across four relational tables (`departments`, `students`, `courses`, and `enrollments`); the Flask backend handles business logic and executes parameterized SQL queries via `psycopg2`; and the frontend renders responsive HTML5 templates styled with vanilla CSS. Key features include a live statistical dashboard, full student CRUD operations with validation, search functionality, and a course enrollment catalog."

---

#### Q2. What is the 3-Tier Architecture in your project?
**Answer:**
> "The 3 tiers are:
> 1. **Presentation Layer (Frontend):** Jinja2 HTML templates and custom CSS (`style.css`) displayed in the user's web browser.
> 2. **Application Layer (Backend):** Python and Flask (`app.py`, `db.py`) handling incoming HTTP requests, session management, input validation, and business logic.
> 3. **Database Layer:** PostgreSQL 16 (`student_db`), which stores the relational tables, enforces constraints, and ensures referential integrity."

---

### Category 2: Database Design & SQL Fundamentals

#### Q3. How did you structure your database schema, and why?
**Answer:**
> "I designed 4 normalized tables to eliminate data redundancy:
> - `departments`: stores department name and code.
> - `students`: stores demographic details and a foreign key to `departments`.
> - `courses`: stores course titles, codes, credit values, and department IDs.
> - `enrollments`: serves as a junction/bridge table linking students to courses with academic grades.
>
> By separating departments into their own table rather than repeating the department name as text in the students table, the schema adheres to Third Normal Form (3NF)."

---

#### Q4. What is a Primary Key and how did you implement it in PostgreSQL?
**Answer:**
> "A **Primary Key** uniquely identifies each tuple/row in a table and cannot contain `NULL` values. In PostgreSQL, I used `SERIAL PRIMARY KEY` (for example, `student_id SERIAL PRIMARY KEY`). Behind the scenes, PostgreSQL creates an integer sequence that automatically increments by 1 on every `INSERT` statement."

---

#### Q5. How did you model the relationship between Students and Courses?
**Answer:**
> "Students and Courses have a **Many-to-Many relationship**: one student can enroll in multiple courses, and one course has multiple students.
> Relational databases cannot directly link Many-to-Many relationships using a single foreign key. Therefore, I created an associative/junction table called `enrollments`. It contains:
> - `student_id` (Foreign Key referencing `students`)
> - `course_id` (Foreign Key referencing `courses`)
> - Additional attributes like `enrollment_date` and `grade`
> - A composite unique constraint: `CONSTRAINT unique_student_course UNIQUE (student_id, course_id)` to prevent duplicate enrollments of the same student in the same course."

---

#### Q6. What is the difference between `ON DELETE SET NULL` and `ON DELETE CASCADE` in your foreign keys?
**Answer:**
> "In my schema:
> - In `students`, `department_id` uses **`ON DELETE SET NULL`**: If a department is discontinued, we do not want to delete student records; their department field simply resets to `NULL`.
> - In `enrollments`, foreign keys use **`ON DELETE CASCADE`**: If a student leaves or is deleted, their enrollment records should automatically be purged to prevent orphaned references."

---

#### Q7. Why did you drop tables in reverse order in `schema.sql`?
**Answer:**
> "Because of **Foreign Key dependencies**. If I tried to drop the `departments` table first, PostgreSQL would reject the query because `students` and `courses` still hold foreign key references pointing to it. Therefore, we drop `enrollments` first, then `courses`, then `students`, and finally `departments`."

---

#### Q8. What constraints did you use, and why?
**Answer:**
> "- **`PRIMARY KEY`**: Enforces entity uniqueness and non-nullability.
> - **`NOT NULL`**: Ensures required fields (like first name, last name, email, credits) are never left blank.
> - **`UNIQUE`**: Guarantees distinct values (used on student email, course code, and department code).
> - **`CHECK (credits > 0)`**: Enforces domain integrity so course credits cannot be 0 or negative.
> - **`DEFAULT CURRENT_DATE`**: Automatically captures the current system date when an enrollment occurs."

---

### Category 3: SQL Queries & Performance

#### Q9. Explain the difference between `INNER JOIN` and `LEFT JOIN` using your project.
**Answer:**
> "- An **`INNER JOIN`** returns rows only when there is a match in both tables.
> - A **`LEFT JOIN`** returns all records from the left table, plus matched records from the right table (filling with `NULL` if no match exists).
> 
> *In my project:* When displaying students (`students.html`), I used a `LEFT JOIN departments ON students.department_id = departments.department_id`. This guarantees that if a new student does not have an assigned department yet, their profile is still displayed rather than being excluded."

---

#### Q10. What query did you write for the Courses catalog?
**Answer:**
> "I wrote an aggregate query combining `JOIN`, `LEFT JOIN`, `GROUP BY`, and `COUNT`:
> ```sql
> SELECT c.course_id, c.course_code, c.course_name, c.credits,
>        d.department_name,
>        COUNT(e.enrollment_id) AS enrolled_students
> FROM courses c
> JOIN departments d ON c.department_id = d.department_id
> LEFT JOIN enrollments e ON c.course_id = e.course_id
> GROUP BY c.course_id, c.course_code, c.course_name, c.credits, d.department_name
> ORDER BY c.course_code;
> ```
> This retrieves course and department details along with the total count of actively enrolled students, even if a course currently has 0 enrollments."

---

#### Q11. How does the student search query work?
**Answer:**
> "I used PostgreSQL's **`ILIKE`** operator, which performs case-insensitive wildcard searches:
> ```sql
> WHERE s.first_name ILIKE %s 
>    OR s.last_name ILIKE %s 
>    OR s.email ILIKE %s
> ```
> By passing `%query%` via parameterized values, if a user types 'sharma' or 'SHARMA', it finds Aarav Sharma regardless of letter case."

---

### Category 4: Python, Flask, and Security

#### Q12. What is SQL Injection, and how did you prevent it?
**Answer:**
> "**SQL Injection (SQLi)** is a vulnerability where malicious SQL commands are injected into user inputs, allowing attackers to view or delete database tables.
> In my project, I prevented SQL injection by using **parameterized queries** provided by `psycopg2`. Instead of using string interpolation (like `f'SELECT * WHERE email = {email}'`), I passed query parameters separately:
> `cur.execute('SELECT * FROM students WHERE email = %s', (email,))`
> The database driver escapes and treats all user input strictly as literal values, never as executable SQL code."

---

#### Q13. What is `RealDictCursor` in `psycopg2`?
**Answer:**
> "By default, `psycopg2` returns rows as tuples, which requires accessing columns by numerical index (e.g., `row[0]`). By setting `cursor_factory=RealDictCursor` in `db.py`, results are returned as dictionary-like objects where values can be accessed by column name (e.g., `student['first_name']`). This improves code readability and prevents index errors in templates."

---

#### Q14. How do you handle database transactions in Flask?
**Answer:**
> "In `psycopg2`, queries start an implicit transaction block:
> - For write operations (`INSERT`, `UPDATE`, `DELETE`), we explicitly call **`conn.commit()`** to persist changes.
> - If an exception occurs (e.g., an `IntegrityError` from a duplicate email), we call **`conn.rollback()`** to revert the transaction and keep the database in a consistent state.
> - Both cursors and connections are closed in a **`finally:`** block to prevent connection leaks."

---

#### Q15. How did you secure your database credentials?
**Answer:**
> "I followed the principle of separating configuration from code:
> - Credentials (`DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, `DB_PORT`) are stored in an external `.env` file loaded via `python-dotenv`.
> - The `.env` file is explicitly listed in `.gitignore` so passwords are never committed to version control or pushed to GitHub."
