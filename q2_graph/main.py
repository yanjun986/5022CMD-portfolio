from graph import Graph
from course import Course, SAMPLE_COURSES, SAMPLE_PREREQUISITES


class CourseSystem:
    """Connects Course objects to the Graph. Edge rule: prerequisite -> course it unlocks."""

    def __init__(self):
        self.graph = Graph()     # stores the arrows between course codes
        self.courses = {}        # course code -> Course object

    def add_course(self, course):
        """Add a course as a new vertex (feature e). Returns False if the code exists."""
        if not self.graph.addVertex(course.course_code):
            return False
        self.courses[course.course_code] = course
        return True

    def add_prerequisite(self, course_code, prereq_code):
        """Make prereq_code a prerequisite of course_code (feature g)."""
        if self.graph.wouldCreateCycle(prereq_code, course_code):
            return "cycle"
        if self.graph.addEdge(prereq_code, course_code):
            return "added"
        return "exists"

    def remove_prerequisite(self, course_code, prereq_code):
        """Remove prereq_code as a prerequisite of course_code (feature h)."""
        return self.graph.removeEdge(prereq_code, course_code)

    def prerequisites_of(self, code):
        """Incoming edges = direct prerequisites (feature c)."""
        return [self.courses[c] for c in self.graph.listIncomingAdjacentVertex(code)]

    def unlocked_by(self, code):
        """Outgoing edges = courses this one unlocks (feature d)."""
        return [self.courses[c] for c in self.graph.listOutgoingAdjacentVertex(code)]

    def all_prerequisites(self, code):
        """Every course needed before this one, direct AND indirect (extra)."""
        found = []
        to_check = list(self.graph.listIncomingAdjacentVertex(code))
        while to_check:
            c = to_check.pop()
            if c not in found:
                found.append(c)
                to_check.extend(self.graph.listIncomingAdjacentVertex(c))
        return [self.courses[c] for c in sorted(found)]

    def has(self, code):
        """True if a course with this code exists."""
        return self.graph.hasVertex(code)

    def all_courses(self):
        """Every Course object, in the order they were added."""
        return [self.courses[c] for c in self.graph.vertices()]

    def load_samples(self):
        """Load the pre-defined courses and prerequisites."""
        for course in SAMPLE_COURSES:
            self.add_course(course)
        for prereq, course in SAMPLE_PREREQUISITES:
            self.add_prerequisite(course, prereq)


# ======================================================================
# Input helpers - keep asking until the input is valid
# ======================================================================
def ask_existing_code(system, prompt):
    """Ask for a course code that exists. Blank = cancel (returns None)."""
    while True:
        code = input(prompt).strip().upper()
        if code == "":
            return None
        if system.has(code):
            return code
        print(f"  {code} does not exist. Try again, or press Enter to cancel.")


def ask_new_code(system, prompt):
    """Ask for a new code: 2 letters + 3 digits (e.g. CS401) that isn't used yet."""
    while True:
        code = input(prompt).strip().upper()
        if code == "":
            return None
        if not (len(code) == 5 and code[:2].isalpha() and code[2:].isdigit()):
            print("  Code must be 2 letters followed by 3 digits (e.g. CS401).")
        elif system.has(code):
            print(f"  {code} already exists.")
        else:
            return code


def ask_text(prompt):
    """Ask for text that cannot be empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This cannot be empty. Please try again.")


def ask_name(prompt):
    """Ask for a name that contains at least one letter (e.g. not just '23')."""
    while True:
        value = input(prompt).strip()
        if any(ch.isalpha() for ch in value):
            return value
        print("  Please enter a name that contains letters.")


def ask_int(prompt, low, high):
    """Ask for a whole number between low and high."""
    while True:
        value = input(prompt).strip()
        if value.isdigit() and low <= int(value) <= high:
            return int(value)
        print(f"  Please enter a whole number from {low} to {high}.")


def ask_level(prompt):
    """Ask for 'core' or 'elective'."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("core", "elective"):
            return value
        print("  Please type core or elective.")


def print_courses(title, courses, empty_message):
    """Print a heading and one line per course, or a message if there are none."""
    print(f"\n{title}")
    if not courses:
        print(f"  {empty_message}")
    for c in courses:
        print(f"  {c}")


# ======================================================================
# Menu options
# ======================================================================
def list_course_names(system):                                   # a
    """Feature a: display all course names."""
    courses = system.all_courses()
    print(f"\n--- All courses ({len(courses)}) ---")
    for c in courses:
        print(f"  {c.course_code}  {c.course_name}")


def view_course_details(system):                                 # b
    """Feature b: every detail, ignoring core/elective."""
    code = ask_existing_code(system, "\nCourse code: ")
    if code:
        print(system.courses[code].details())


def view_prerequisites(system):                                  # c
    """Feature c: incoming edges = prerequisites."""
    code = ask_existing_code(system, "\nCourse code: ")
    if not code:
        return
    direct = system.prerequisites_of(code)
    print_courses(f"Prerequisites of {code}:", direct, "None - this course has no prerequisites.")
    chain = system.all_prerequisites(code)
    if len(chain) > len(direct):          # only show if there are indirect ones too
        print_courses("Full chain (direct + indirect):", chain, "")


def view_unlocked_courses(system):                               # d
    """Feature d: outgoing edges = courses this one unlocks."""
    code = ask_existing_code(system, "\nCourse code: ")
    if code:
        print_courses(f"Courses unlocked by {code}:", system.unlocked_by(code),
                      "None - this course is not a prerequisite for any course.")


def add_course(system):                                          # e
    """Feature e: create a new vertex on demand."""
    print("\n--- Add a new course (press Enter at the code to cancel) ---")
    code = ask_new_code(system, "Course code (e.g. CS401): ")
    if not code:
        return
    course = Course(
        code,
        ask_name("Course name: "),
        ask_int("Credit hours (1-12): ", 1, 12),
        ask_level("Level (core/elective): "),
        ask_int("Year of study (1-5): ", 1, 5),
        ask_name("Lecturer: "),
        ask_text("Description: "),
    )
    system.add_course(course)
    print(f"  {code} added as a new vertex.")


def view_public_profile(system):                                 # f
    """Feature f: elective shows name only, core shows everything."""
    code = ask_existing_code(system, "\nCourse code: ")
    if code:
        print(system.courses[code].public_profile())


def add_prerequisite(system):                                    # g
    """Feature g: course X gets course Y as a prerequisite (new edge Y -> X)."""
    x = ask_existing_code(system, "\nCourse X (the course): ")
    if not x:
        return
    y = ask_existing_code(system, "Course Y (the new prerequisite of X): ")
    if not y:
        return
    result = system.add_prerequisite(x, y)
    if result == "added":
        print(f"  Done: {y} is now a prerequisite of {x} (edge {y} -> {x}).")
    elif result == "exists":
        print(f"  {y} is already a prerequisite of {x}.")
    else:
        print(f"  Rejected: {y} -> {x} would create a circular requirement.")


def remove_prerequisite(system):                                 # h
    """Feature h: remove course Y as a prerequisite of course X (remove edge Y -> X)."""
    x = ask_existing_code(system, "\nCourse X (the course): ")
    if not x:
        return
    y = ask_existing_code(system, "Course Y (the prerequisite to remove): ")
    if not y:
        return
    if system.remove_prerequisite(x, y):
        print(f"  Done: {y} is no longer a prerequisite of {x}.")
    else:
        print(f"  {y} is not a prerequisite of {x}.")


# Menu letter -> (label, function). Adding an option needs only one new line.
MENU = {
    "a": ("Display all course names", list_course_names),
    "b": ("View course details", view_course_details),
    "c": ("View prerequisites of a course", view_prerequisites),
    "d": ("View courses unlocked by a course", view_unlocked_courses),
    "e": ("Add a new course", add_course),
    "f": ("View public course profile", view_public_profile),
    "g": ("Add a prerequisite to a course", add_prerequisite),
    "h": ("Remove a prerequisite from a course", remove_prerequisite),
}


def main():
    system = CourseSystem()
    system.load_samples()
    print(f"Loaded {len(system.courses)} courses.")

    while True:
        print("\n========= COURSE PREREQUISITE SYSTEM =========")
        for key, (label, _) in MENU.items():
            print(f" {key}. {label}")
        print(" 0. Exit")
        print("==============================================")
        choice = input("Choose an option: ").strip().lower()

        if choice == "0":
            print("Goodbye!")
            break
        if choice in MENU:
            _, action = MENU[choice]
            action(system)
        else:
            print("  Invalid option, please choose a-h or 0.")


if __name__ == "__main__":
    main()