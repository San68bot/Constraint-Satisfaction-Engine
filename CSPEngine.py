class CSPEngine:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assignments = {}

    def is_consistent(self, var, value):
        # Assign a temporary value to the variable and check consistency
        self.assignments[var] = value
        consistent = self.constraints(self.assignments, var, value)
        if not consistent:
            del self.assignments[var]
        return consistent

    def backtrack_and_solve(self):
        # If all variables assigned return solved
        if len(self.assignments) == len(self.variables):
            return self.assignments

        # pick an unassigned variable
        unassigned_vars = [v for v in self.variables if v not in self.assignments]
        var = unassigned_vars[0]

        for value in self.domains[var]:
            if self.is_consistent(var, value):
                # assign it temporarily
                self.assignments[var] = value

                # check everything else
                result = self.backtrack_and_solve()
                if result is not None:
                    return result

                # cmd z and try next value if we get a none back
                del self.assignments[var]

        # If absolutely no value leads the system to a solution it will return none
        return None


time_blocks = [
    '9am-10am',
    '10am-11am',
    '11am-12pm',
    '12pm-1pm',
    '1pm-2pm',
    '2pm-3pm',
    '3pm-4pm',
    '4pm-5pm'
]

subjects = ['Math', 'English', 'Science', 'History']

# Teachers and their qualifications
teachers = {
    'Teacher1': ['Math', 'Science'],
    'Teacher2': ['English', 'History'],
    'Teacher3': ['Math', 'English'],
    'Teacher4': ['Science', 'History']
}

# Define multiple classes (sections)
classes = ['Class1', 'Class2', 'Class3']

# List of days in the week
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Global teacher availability tracker (reset daily)
def reset_teacher_availability():
    return {time_block: [] for time_block in time_blocks}

# Constraints: each time block must be assigned a teacher qualified for its subject and not already scheduled in another class.
def constraints(assignments, var, value, teacher_availability):
    # Get the subject for this time block
    subject = subject_assignments[var]

    # Check if the teacher is qualified for the subject
    if subject not in teachers[value]:
        return False

    # Check if the teacher is already scheduled for this time block in another class
    if value in teacher_availability[var]:
        return False

    # Make sure the teacher's workload is balanced across the time blocks
    teacher_counts = {teacher: 0 for teacher in teachers}
    for time_block in assignments:
        teacher = assignments[time_block]
        teacher_counts[teacher] += 1

    counts = list(teacher_counts.values())
    if max(counts) - min(counts) > 1:
        return False
    return True

# Run the CSP solver for each class on each day
weekly_schedule = {}

for day in week_days:
    print(f"\n--- {day} Schedule ---")
    weekly_schedule[day] = {}  # Store schedule per day

    # Reset teacher availability at the start of each day
    teacher_availability = reset_teacher_availability()

    for class_name in classes:
        print(f"\n--- {class_name} Schedule for {day} ---")

        # Assign subjects to time blocks using round-robin for each class
        subject_assignments = {}
        for i, time_block in enumerate(time_blocks):
            subject_assignments[time_block] = subjects[i % len(subjects)]

        # Create domains for each time block based on teacher qualifications
        domains = {}
        for time_block in time_blocks:
            subject = subject_assignments[time_block]
            qualified_teachers = [teacher for teacher, quals in teachers.items() if subject in quals]
            domains[time_block] = qualified_teachers

        # CSP solver initialization
        solver = CSPEngine(time_blocks, domains, lambda a, v, val: constraints(a, v, val, teacher_availability))
        solution = solver.backtrack_and_solve()

        if solution:
            # Store the schedule for the current class and day
            day_schedule = {}
            for time_block in time_blocks:
                teacher = solution[time_block]
                subject = subject_assignments[time_block]
                day_schedule[time_block] = f"{subject} - {teacher}"
                teacher_availability[time_block].append(teacher)  # Mark teacher as unavailable for this time block
                print(f"{time_block}: {subject} - {teacher}")
            weekly_schedule[day][class_name] = day_schedule
        else:
            print(f"No solution for {class_name} on {day} :(")

# Print the complete weekly schedule
print("\nComplete Weekly Schedule:")
for day, day_schedule in weekly_schedule.items():
    print(f"\n--- {day} ---")
    for class_name, schedule in day_schedule.items():
        print(f"\n--- {class_name} ---")
        for time_block, assignment in schedule.items():
            print(f"{time_block}: {assignment}")
