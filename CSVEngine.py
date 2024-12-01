import csv

"""
Innovation 4 Impact CSP Scheduling Algorithm for solving school scheduling challenges.
"""

# Option to export the schedule to text files or print to console
_export = True # Set to True to export the schedule to text files and False to print to console

# Option to choose one grade or multiple grades
_one_grade = False # Set to True to solve for one grade only and False to solve for multiple grades

if _one_grade:
    grades = [1]
else:
    grades = [1, 2]

sections = ['A', 'B']

time_slots = {
    1: '9:00am - 11:00am',
    2: '11:00am - 1:00pm',
    3: '1:00pm - 3:00pm',
    4: '3:00pm - 5:00pm'
}

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
day_schedule_map = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 1,
    'Thursday': 2,
    'Friday': 1
}

subjects_day = {
    1: ['English', 'Math', 'Science', 'History'],
    2: ['Art', 'Music', 'Language', 'PE']
}

if _one_grade:
    teachers = {
        1: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8'],  # Grade 1 teachers
    }
else:
    teachers = {
        1: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8'],  # Grade 1 teachers
        2: ['T9', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16']  # Grade 2 teachers
    }

if _one_grade:
    teacher_subject_map = {
        1: {
            'T1': 'English',
            'T2': 'Math',
            'T3': 'Science',
            'T4': 'History',
            'T5': 'Art',
            'T6': 'Music',
            'T7': 'Language',
            'T8': 'PE',
        }
    }
else:
    teacher_subject_map = {
        1: {
            'T1': 'English',
            'T2': 'Math',
            'T3': 'Science',
            'T4': 'History',
            'T5': 'Art',
            'T6': 'Music',
            'T7': 'Language',
            'T8': 'PE',
        },
        2: {
            'T9': 'English',
            'T10': 'Math',
            'T11': 'Science',
            'T12': 'History',
            'T13': 'Art',
            'T14': 'Music',
            'T15': 'Language',
            'T16': 'PE'
        }
    }

subject_teacher_map = {}
for g in grades:
    subject_teacher_map[g] = {}
    for teacher, subject in teacher_subject_map[g].items():
        if subject not in subject_teacher_map[g]:
            subject_teacher_map[g][subject] = []
        subject_teacher_map[g][subject].append(teacher)

variables = []
domains = {}

for g in grades:
    for day in days_of_week:
        d = day_schedule_map[day]
        for s in sections:
            for t in time_slots:
                var_name = f'G{g}_{day}_S{s}_T{t}'
                variables.append(var_name)
                # Assign the day's subjects and possible teachers as the domain for the variable
                domains[var_name] = []
                for subject in subjects_day[d]:
                    for teacher in subject_teacher_map[g][subject]:
                        domains[var_name].append((subject, teacher))

# The constraints

def constraint1(var, value, assignment, variables, domains):
    """
    Ensures no duplicate subjects in the same section on the same day for the same grade.
    """
    tokens = var.split('_')
    g = int(tokens[0][1])
    day = tokens[1]
    s = tokens[2][1]
    t = int(tokens[3][1])
    subject, teacher = value

    for time in time_slots:
        other_var = f'G{g}_{day}_S{s}_T{time}'
        if other_var in assignment and other_var != var:
            assigned_subject, assigned_teacher = assignment[other_var]
            if assigned_subject == subject:
                return False
    return True

def constraint2(var, value, assignment, variables, domains):
    """
    Ensures a teacher is not assigned to teach two classes at the same time, in any grade.
    """
    tokens = var.split('_')
    g = int(tokens[0][1])  # Grade of the current variable
    day = tokens[1]
    s = tokens[2][1]
    t = int(tokens[3][1])
    subject, teacher = value

    # Teachers are unique to their grade, so they only need to be checked within their grade
    for other_s in sections:
        other_var = f'G{g}_{day}_S{other_s}_T{t}'
        if other_var in assignment and other_var != var:
            assigned_subject, assigned_teacher = assignment[other_var]
            if assigned_teacher == teacher:
                return False
    return True

def constraint3(var, value, assignment, variables, domains):
    """
    Ensures a teacher does not teach back-to-back time slots within their grade.
    """
    tokens = var.split('_')
    g = int(tokens[0][1])
    day = tokens[1]
    s = tokens[2][1]
    t = int(tokens[3][1])
    subject, teacher = value

    for dt in [-1, 1]:
        adjacent_time = t + dt
        if adjacent_time not in time_slots:
            continue
        for sec in sections:
            adj_var = f'G{g}_{day}_S{sec}_T{adjacent_time}'
            if adj_var in assignment:
                adj_subject, adj_teacher = assignment[adj_var]
                if adj_teacher == teacher:
                    return False
    return True

constraints = [constraint1, constraint2, constraint3]

# CSPEngine - Our custom Constraint Satisfaction Problem solver
class CSPEngine:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def is_consistent(self, var, value, assignment):
        for constraint in self.constraints:
            if not constraint(var, value, assignment, self.variables, self.domains):
                return False
        return True

    def select_unassigned_variable(self, assignment):
        # MRV Can also be implemented here
        unassigned_vars = [v for v in self.variables if v not in assignment]
        return unassigned_vars[0] if unassigned_vars else None

    def order_domain_values(self, var, assignment):
        # LCV Can also be implemented here
        return self.domains[var]

    def backtracking_search(self):
        assignment = {}
        return self._backtrack(assignment)

    def _backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment  # Solution exists

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self._backtrack(assignment)
                if result:
                    return result
                del assignment[var]
        return None

csp_engine = CSPEngine(variables, domains, constraints)
solution = csp_engine.backtracking_search()

if solution:
    schedule = {}
    for var, value in solution.items():
        subject, teacher = value
        tokens = var.split('_')
        g = int(tokens[0][1])
        day = tokens[1]
        s = tokens[2][1]
        t = int(tokens[3][1])
        if g not in schedule:
            schedule[g] = {}
        if day not in schedule[g]:
            schedule[g][day] = {}
        if s not in schedule[g][day]:
            schedule[g][day][s] = {}
        schedule[g][day][s][t] = (subject, teacher)

    for g in sorted(schedule.keys()):
        output_lines = [f"Grade {g} Weekly Schedule:\n"]
        output_data = []
        output_data.append(["Grade", "Day", "Section", "Time Slot", "Subject", "Teacher"])
        for day in days_of_week:
            output_lines.append(f"{day}:\n")
            d = day_schedule_map[day]
            for s in sections:
                output_lines.append(f"  Section {s}:\n")
                for t in sorted(time_slots):
                    time_range = time_slots[t]
                    if t in schedule[g][day][s]:
                        subject, teacher = schedule[g][day][s][t]
                        output_lines.append(f"    {time_range}: {subject} (Teacher: {teacher})\n")
                        output_data.append([g, day, s, time_range, subject, teacher])
                    else:
                        output_lines.append(f"    {time_range}: Free Period\n")
                        output_data.append([g, day, s, time_range, "Free Period", "N/A"])
            output_lines.append("\n")
        if _export:
            # Export to text file
            filename_txt = f"Grade{g}_Schedule.txt"
            with open(filename_txt, 'w') as file:
                file.writelines(output_lines)
            print(f"Schedule for Grade {g} has been exported to {filename_txt}.")
            
            # Export to CSV file
            filename_csv = f"Grade{g}_Schedule.csv"
            with open(filename_csv, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(output_data)
            print(f"Schedule for Grade {g} has been exported to {filename_csv}.")
        else:
            print("".join(output_lines))
else:
    print("No solution found.")

def substituteTeacher(tea, grade, section, timeslot, day):
    allteachList = []
    for i in teachers.values():
        for y in i:
            if y not in allteachList:
                allteachList.append(y)

def priortyList(grade, section, subject, timeslot, day, allteachLists):
    teachDict = {}
    
                

