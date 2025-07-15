import sqlite3
from typing import List, Tuple


def create_sample_university_data(db_path: str = "sample_university.db") -> None:
    """
    Creates a SQLite database at `db_path` with the university schema and seed data.
    Drops existing tables and recreates them.
    """
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")

        # Drop existing tables if they exist (in reverse order of dependencies)
        tables_to_drop: List[str] = [
            "attendance",
            "grades",
            "enrollments",
            "course_professors",
            "schedules",
            "classrooms",
            "courses",
            "students",
            "professors",
            "departments",
        ]
        for tbl in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {tbl}")

        # Create departments table
        cursor.execute(
            """
            CREATE TABLE departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                building TEXT
            )
        """
        )

        # Create professors table
        cursor.execute(
            """
            CREATE TABLE professors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                department_id INTEGER,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            )
        """
        )

        # Create students table
        cursor.execute(
            """
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                dob DATE,
                department_id INTEGER,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            )
        """
        )

        # Create courses table
        cursor.execute(
            """
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                code TEXT UNIQUE,
                credits INTEGER,
                department_id INTEGER,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            )
        """
        )

        # Create classrooms table
        cursor.execute(
            """
            CREATE TABLE classrooms (
                id INTEGER PRIMARY KEY,
                building TEXT,
                room_number TEXT,
                capacity INTEGER
            )
        """
        )

        # Create schedules table
        cursor.execute(
            """
            CREATE TABLE schedules (
                id INTEGER PRIMARY KEY,
                course_id INTEGER,
                classroom_id INTEGER,
                day_of_week TEXT,
                start_time TEXT,
                end_time TEXT,
                FOREIGN KEY(course_id) REFERENCES courses(id),
                FOREIGN KEY(classroom_id) REFERENCES classrooms(id)
            )
        """
        )

        # Create course_professors table
        cursor.execute(
            """
            CREATE TABLE course_professors (
                id INTEGER PRIMARY KEY,
                course_id INTEGER,
                professor_id INTEGER,
                FOREIGN KEY(course_id) REFERENCES courses(id),
                FOREIGN KEY(professor_id) REFERENCES professors(id)
            )
        """
        )

        # Create enrollments table
        cursor.execute(
            """
            CREATE TABLE enrollments (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date DATE,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        """
        )

        # Create grades table
        cursor.execute(
            """
            CREATE TABLE grades (
                id INTEGER PRIMARY KEY,
                enrollment_id INTEGER,
                grade TEXT,
                FOREIGN KEY(enrollment_id) REFERENCES enrollments(id)
            )
        """
        )

        # Create attendance table
        cursor.execute(
            """
            CREATE TABLE attendance (
                id INTEGER PRIMARY KEY,
                enrollment_id INTEGER,
                date DATE,
                present BOOLEAN,
                FOREIGN KEY(enrollment_id) REFERENCES enrollments(id)
            )
        """
        )

        # Insert sample data
        departments: List[Tuple[int, str, str]] = [
            (1, "Computer Science", "Engineering Hall"),
            (2, "Mathematics", "Science Building"),
            (3, "Physics", "Quantum Block"),
        ]
        cursor.executemany("INSERT INTO departments VALUES (?, ?, ?)", departments)

        professors: List[Tuple[int, str, str, int]] = [
            (1, "John Smith", "jsmith@univ.edu", 1),
            (2, "Alice Johnson", "ajohnson@univ.edu", 2),
            (3, "Michael Lee", "mlee@univ.edu", 1),
            (4, "No Course Prof", "ncp@univ.edu", 3),
        ]
        cursor.executemany("INSERT INTO professors VALUES (?, ?, ?, ?)", professors)

        students: List[Tuple[int, str, str, str, int]] = [
            (1, "Fatima Zahra", "fatima@univ.edu", "1999-03-10", 1),
            (2, "Mohammed Idris", "idris@univ.edu", "2001-07-21", 1),
            (3, "Alice Kim", "alice@univ.edu", "1998-11-02", 2),
            (4, "James Bond", "jbond@univ.edu", "1997-04-04", 3),
        ]
        cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", students)

        courses: List[Tuple[int, str, str, int, int]] = [
            (1, "Machine Learning", "CS301", 3, 1),
            (2, "Calculus I", "MA101", 4, 2),
            (3, "Quantum Physics", "PH201", 4, 3),
            (4, "Operating Systems", "CS202", 3, 1),
        ]
        cursor.executemany("INSERT INTO courses VALUES (?, ?, ?, ?, ?)", courses)

        classrooms: List[Tuple[int, str, str, int]] = [
            (1, "Engineering Hall", "E101", 120),
            (2, "Science Building", "S204", 90),
            (3, "Quantum Block", "Q303", 60),
        ]
        cursor.executemany("INSERT INTO classrooms VALUES (?, ?, ?, ?)", classrooms)

        schedules: List[Tuple[int, int, int, str, str, str]] = [
            (1, 1, 1, "Monday", "10:00", "12:00"),
            (2, 2, 2, "Tuesday", "09:00", "11:00"),
            (3, 3, 3, "Wednesday", "14:00", "16:00"),
            (4, 4, 1, "Monday", "10:00", "12:00"),
        ]
        cursor.executemany("INSERT INTO schedules VALUES (?, ?, ?, ?, ?, ?)", schedules)

        course_professors: List[Tuple[int, int, int]] = [
            (1, 1, 1),
            (2, 2, 2),
            (3, 3, 3),
            (4, 4, 1),
        ]
        cursor.executemany(
            "INSERT INTO course_professors VALUES (?, ?, ?)", course_professors
        )

        enrollments: List[Tuple[int, int, int, str]] = [
            (1, 1, 1, "2024-09-01"),
            (2, 2, 1, "2024-09-01"),
            (3, 1, 4, "2024-09-01"),
            (4, 3, 2, "2024-09-01"),
            (5, 4, 3, "2024-09-01"),
            (6, 2, 2, "2024-09-01"),
        ]
        cursor.executemany("INSERT INTO enrollments VALUES (?, ?, ?, ?)", enrollments)

        grades: List[Tuple[int, int, str]] = [
            (1, 1, "A"),
            (2, 2, "B"),
            (3, 3, "A"),
            (4, 4, "C"),
            (5, 5, "B"),
            (6, 6, "D"),
        ]
        cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)

        attendance: List[Tuple[int, int, str, int]] = [
            (1, 1, "2025-03-18", 0),
            (2, 2, "2025-03-18", 1),
            (3, 4, "2025-03-18", 1),
            (4, 3, "2025-03-18", 0),
            (5, 1, "2025-04-05", 1),
            (6, 2, "2025-04-05", 1),
            (7, 3, "2025-04-05", 1),
            (8, 4, "2025-04-05", 0),
        ]
        cursor.executemany("INSERT INTO attendance VALUES (?, ?, ?, ?)", attendance)

        conn.commit()
        print(f"Database '{db_path}' seeded successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
