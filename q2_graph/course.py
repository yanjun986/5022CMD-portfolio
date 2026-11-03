class Course:
    """One course offered by the university."""

    def __init__(self, course_code, course_name, credit_hours, level, year, lecturer, description):
        self.course_code = course_code      # str   e.g. "CS201" (graph vertex key)
        self.course_name = course_name      # str   e.g. "Data Structures"
        self.credit_hours = credit_hours    # int   e.g. 4
        self.level = level                  # str   "core" or "elective"
        self.year = year                    # int   year of study, e.g. 2
        self.lecturer = lecturer            # str   e.g. "Dr. Kumar"
        self.description = description      # str   short summary

    def __str__(self):
        """One-line summary, used in lists."""
        return f"{self.course_code} - {self.course_name} ({self.level}, {self.credit_hours} credits)"

    def details(self):
        """Every attribute (feature b: ignores core/elective)."""
        return (f"  Code         : {self.course_code}\n"
                f"  Name         : {self.course_name}\n"
                f"  Credit hours : {self.credit_hours}\n"
                f"  Level        : {self.level.title()}\n"
                f"  Year         : {self.year}\n"
                f"  Lecturer     : {self.lecturer}\n"
                f"  Description  : {self.description}")

    def public_profile(self):
        """Feature f: core shows everything, elective shows only the name."""
        if self.level == "core":
            return self.details()
        return (f"  Name         : {self.course_name}\n"
                f"  (Elective course - other details are hidden)")


# Pre-defined courses (brief: minimum 5, maximum 10)
SAMPLE_COURSES = [
    Course("CS101", "Programming Fundamentals", 4, "core", 1,
           "Dr. Tan", "Variables, control flow, functions and problem solving."),
    Course("MA101", "Discrete Mathematics", 3, "core", 1,
           "Dr. Lim", "Logic, sets, relations, counting and graph basics."),
    Course("CS102", "Object-Oriented Programming", 4, "core", 1,
           "Ms. Wong", "Classes, inheritance and polymorphism."),
    Course("CS201", "Data Structures", 4, "core", 2,
           "Dr. Kumar", "Lists, stacks, queues, trees, hash tables and graphs."),
    Course("CS202", "Database Systems", 3, "core", 2,
           "Mr. Lee", "Relational model, SQL and normalisation."),
    Course("CS301", "Advanced Algorithms", 4, "core", 3,
           "Dr. Rao", "Complexity analysis, graph algorithms and concurrency."),
    Course("CS310", "Machine Learning", 3, "elective", 3,
           "Dr. Chong", "Supervised and unsupervised learning."),
    Course("CS320", "Game Development", 3, "elective", 3,
           "Mr. Ng", "Game loops, physics and game engines."),
]

# Prerequisites as (prerequisite, course it unlocks) -> edge prerequisite -> course
SAMPLE_PREREQUISITES = [
    ("CS101", "CS102"),
    ("CS101", "CS201"),
    ("MA101", "CS201"),
    ("CS102", "CS202"),
    ("CS201", "CS301"),
    ("MA101", "CS301"),
    ("CS201", "CS310"),
    ("CS102", "CS320"),
]


if __name__ == "__main__":
    core = SAMPLE_COURSES[3]        # CS201 - a core course
    elective = SAMPLE_COURSES[6]    # CS310 - an elective course

    print("=== TEST 1: One-line summary (__str__) ===")
    print(f"  {core}")

    print("\n=== TEST 2: Full details of a core course (feature b) ===")
    print(core.details())

    print("\n=== TEST 3: Public profile of a core course (feature f) ===")
    print(core.public_profile())

    print("\n=== TEST 4: Public profile of an elective course (feature f) ===")
    print(elective.public_profile())

    print("\n=== TEST 5: Sample data ===")
    print(f"  {len(SAMPLE_COURSES)} courses, {len(SAMPLE_PREREQUISITES)} prerequisite links")