import tkinter as tk
from tkinter import ttk

class CSPEngine:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def is_consistent(self, var, value, assignment):
        for constraint in self.constraints:
            if not constraint(var, value, assignment):
                return False
        return True

    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var
        return None

    def backtracking_and_solve(self):
        assignment = {}
        return self.do_the_thing(assignment)

    def do_the_thing(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.do_the_thing(assignment)
                if result:
                    return result
                del assignment[var]
        return None

# Data initialization
sections = ['A', 'B', 'C']
time_slots = [1, 2, 3, 4]
days = [1, 2]
subjects_day = {
    1: ['English', 'Math', 'Science', 'History'],
    2: ['Art', 'Music', 'Language', 'PE']
}

teacher_subject_map = {
    'T1': 'English',
    'T2': 'Math',
    'T3': 'Science',
    'T4': 'History',
    'T5': 'Art',
    'T6': 'Music',
    'T7': 'Language',
    'T8': 'PE',
    'T9': 'English',
    'T10': 'Math',
    'T11': 'Science',
    'T12': 'History',
    'T13': 'Art',
    'T14': 'Music',
    'T15': 'Language',
    'T16': 'PE',
}

subject_teacher_map = {}
for teacher, subject in teacher_subject_map.items():
    subject_teacher_map.setdefault(subject, []).append(teacher)

variables = []
domains = {}

for day in days:
    for section in sections:
        for time in time_slots:
            var_name = f'D{day}_S{section}_T{time}'
            variables.append(var_name)
            domains[var_name] = []
            for subject in subjects_day[day]:
                for teacher in subject_teacher_map[subject]:
                    domains[var_name].append((subject, teacher))

def c1(var, value, assignment):
    # Constraint 1: No duplicate subjects in the same section on the same day
    day, section, _ = var.split('_')
    subject, _ = value
    for time in time_slots:
        other_var = f'{day}_{section}_T{time}'
        if other_var in assignment and other_var != var:
            assigned_subject, _ = assignment[other_var]
            if assigned_subject == subject:
                return False
    return True

def c2(var, value, assignment):
    # Constraint 2: A teacher cannot teach two classes at the same time
    day, _, time_slot = var.split('_')
    _, teacher = value
    for section in sections:
        other_var = f'{day}_S{section}_{time_slot}'
        if other_var in assignment and other_var != var:
            _, assigned_teacher = assignment[other_var]
            if assigned_teacher == teacher:
                return False
    return True

def c3(var, value, assignment):
    # Constraint 3: A teacher cannot teach back-to-back time slots
    day, _, time_slot = var.split('_')
    time = int(time_slot[1])
    _, teacher = value
    for dt in [-1, 1]:
        adjacent_time = time + dt
        if adjacent_time < 1 or adjacent_time > 4:
            continue
        for section in sections:
            adj_var = f'{day}_S{section}_T{adjacent_time}'
            if adj_var in assignment:
                _, adj_teacher = assignment[adj_var]
                if adj_teacher == teacher:
                    return False
    return True

csp_engine = CSPEngine(variables, domains, [c1, c2, c3])
solution = csp_engine.backtracking_and_solve()

if solution:
    schedule = {}
    for var, value in solution.items():
        subject, teacher = value
        day, section, time_slot = var.split('_')
        time = int(time_slot[1])
        schedule.setdefault(day, {}).setdefault(section, {})[time] = (subject, teacher)
else:
    print("No solution found.")
    exit()

# Create the GUI application
root = tk.Tk()
root.title("School Schedule")

def display_schedule(section):
    # Clear the previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    for day in sorted(schedule.keys()):
        day_label = tk.Label(frame, text=f"Day {day[1]} Schedule for Section {section}", font=('Helvetica', 14, 'bold'))
        day_label.pack(pady=5)

        tree = ttk.Treeview(frame)
        tree['columns'] = ('Time Slot', 'Subject', 'Teacher')
        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('Time Slot', anchor=tk.CENTER, width=80)
        tree.column('Subject', anchor=tk.W, width=120)
        tree.column('Teacher', anchor=tk.W, width=100)

        tree.heading('#0', text='', anchor=tk.W)
        tree.heading('Time Slot', text='Time Slot', anchor=tk.CENTER)
        tree.heading('Subject', text='Subject', anchor=tk.W)
        tree.heading('Teacher', text='Teacher', anchor=tk.W)

        for time in sorted(time_slots):
            if time in schedule[day][f'S{section}']:
                subject, teacher = schedule[day][f'S{section}'][time]
                tree.insert('', 'end', text='', values=(time, subject, teacher))
            else:
                tree.insert('', 'end', text='', values=(time, 'Free Period', ''))

        tree.pack(pady=5)

# Create a frame to hold the buttons and schedule
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=10)

frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create buttons for each section
for section in sections:
    btn = tk.Button(button_frame, text=f"Section {section}", command=lambda s=section: display_schedule(s))
    btn.pack(side=tk.LEFT, padx=10)

root.mainloop()
