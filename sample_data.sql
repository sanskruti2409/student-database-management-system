INSERT INTO departments (department_name, department_code) VALUES
('Computer Science', 'CS'),
('Computer Applications', 'MCA'),
('Information Technology', 'IT');

INSERT INTO courses (course_code, course_name, credits, department_id) VALUES
('CS101', 'Database Management Systems', 4, 1),
('CA201', 'Web Application Development', 4, 2),
('IT301', 'Data Structures & Algorithms', 4, 3),
('CS102', 'Operating Systems', 3, 1),
('CA202', 'Software Engineering Principles', 3, 2);

INSERT INTO students (first_name, last_name, email, phone, date_of_birth, department_id, enrollment_date) VALUES
('Aarav', 'Sharma', 'aarav.sharma@example.edu', '9876543210', '2001-05-14', 1, '2023-08-01'),
('Ananya', 'Patel', 'ananya.patel@example.edu', '9876543211', '2002-09-21', 2, '2023-08-01'),
('Rohan', 'Verma', 'rohan.verma@example.edu', '9876543212', '2001-12-03', 1, '2023-08-01'),
('Pooja', 'Iyer', 'pooja.iyer@example.edu', '9876543213', '2002-03-18', 3, '2023-08-01'),
('Vikram', 'Singh', 'vikram.singh@example.edu', '9876543214', '2001-07-29', 2, '2023-08-01');

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2023-08-10', 'A'),
(1, 4, '2023-08-10', 'B'),
(2, 2, '2023-08-10', 'A'),
(2, 5, '2023-08-10', 'A'),
(3, 1, '2023-08-11', 'B'),
(3, 3, '2023-08-11', 'A'),
(4, 3, '2023-08-12', 'A'),
(4, 2, '2023-08-12', 'B'),
(5, 2, '2023-08-12', 'B'),
(5, 5, '2023-08-12', 'C');
