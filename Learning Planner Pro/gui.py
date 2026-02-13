import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from logic import *
from main import *
from datetime import datetime

class StudentPlannerApp:

    # Initialisation functions

    def __init__(self, main):
        self.main = main
        self.main.geometry("950x700")
        self.main.title("Student Planner")
        self.main.configure(bg="white")
        self.main.resizable(False, False)

        self.creds = authentication()
        #json_setup()
        self.task_vars = []

        self.setup_styles()
        self.build_main_window()
    
    def setup_styles(self):
        style = ttk.Style(self.main)
        style.theme_use("clam")
        style.configure("Green.TButton",
                        background="green",
                        foreground="white",
                        font=("Helvetica", 12),
                        padding=6),
        style.configure("Green.Horizontal.TProgressbar", 
                        troughcolor="white",
                        background="green",
                        foreground="green",
                        bordercolor="black",
                        text="Progress")
        
    def build_main_window(self):
        now = datetime.now()
        day_of_week = now.strftime("%A %d %B")
        today = now.strftime('%Y-%m-%d')

        header = tk.Label(main, text=day_of_week, font=("Arial", 40), bg="white", fg="green")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=210, pady=5)

        self.construct_checklist()
        self.construct_buttons()


        with open(working_reminder_path, 'r') as file:
            reminder = json.load(file)
            reminded = reminder['reminded']
            reminder_date = reminder['date']

        for assignment in self.upcoming_assignments: 
            if assignment[1] != 'No assignments' and reminded == 'False':
                messagebox.showinfo(title='Reminder', message=f'You have an upcoming deadline for {assignment[1]} today')
                reminded = 'True'
                reminder_date = today
        if reminded == 'True' and (((int(reminder_date[-2:])) < (int(today[-2:]))) or ((int(reminder_date[5:-3])) < (int(today[5:-3])))):
            reminded = 'False'

        save_reminder_state(reminded, reminder_date)


    def construct_checklist(self):

        self.events = get_upcoming_events(self.creds)
        self.upcoming_assignments = get_assignments(self.creds, True)
        self.assignments = get_assignments(self.creds, False)

        def toggle():
            """
            Function to toggle the state of the checkbox and update the progress bar.
            """
            checked = 0
            unchecked = 0
            total = 0

            for var in self.task_vars:
                if var.get():
                    checked += 1
                else:
                    unchecked += 1
                total += 1

            self.progress["value"] = (checked / total) * 100 if total > 0 else 0

        checklist_frame = tk.Frame(main, width=30, height=20, bg = "white", highlightbackground="green", highlightthickness=1)
        checklist_frame.grid(row=1, column=0, sticky="nsw", padx=45, pady=50, rowspan=2)

        checklist_header = tk.Label(checklist_frame, text="To-Do", font=("Arial", 20), bg="white", fg="green")
        checklist_header.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")


        try:
            with open(working_checkbox_path, 'r') as file:
                states = json.load(file)
        except FileNotFoundError:
            states = {}

        self.task_vars = []

        print(self.events)
        for id, summary, colour_id in self.events:
            if colour_id == "10":
                colour = "dark green"
            elif colour_id == "9":
                colour = "blue"
            elif colour_id == "6":
                colour = "orange"
            elif colour_id == "8":
                colour = "grey"
            else:
                colour = "black"
            var = tk.BooleanVar(value=states.get(id, False))  # Use the saved state if it exists, otherwise default to False
            self.task_vars.append(var)
            checkbox = tk.Checkbutton(checklist_frame, text=summary, variable=var, bg="white", fg=colour, width=30, justify="left", anchor="w", selectcolor="white", padx=3, command=toggle, font=("Arial 15 bold"))
            checkbox.grid(row=len(self.task_vars), column=0, sticky="nsw", padx=30, pady=5)

        self.progress = ttk.Progressbar(self.main, orient="horizontal", length=458, mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress.grid(row=3, column=0, padx=45, pady=0, sticky='nw')

        toggle()


    def construct_buttons(self):
        file_exists_flag = file_exists(working_modules_path)

        task_actions_frame = tk.Frame(self.main, width=50, height=20, bg = "white", highlightbackground="black", highlightthickness=1)
        task_actions_frame.grid(row=1, column=1, sticky="nsw", padx=10, pady=50)

        task_header = tk.Label(task_actions_frame, text="Task/Assignemnt Actions", font=("Arial", 20), bg="white", fg="black")
        task_header.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        add_button = ttk.Button(task_actions_frame, text="Add Task", style="Green.TButton", command=lambda: [self.add_task_popup(), main.iconify()], state="disabled" if not file_exists_flag else "normal")
        add_button.grid(row=1, column=1, pady=10, sticky='w', padx=23)

        edit_button = ttk.Button(task_actions_frame, text="Edit Task", style="Green.TButton", command=lambda: [self.edit_task_popup(self.events), main.iconify()], state="disabled" if not file_exists_flag else "normal")
        edit_button.grid(row=1, column=2, pady=10, padx=9)

        add_assignment_button = ttk.Button(task_actions_frame, text="Add Assignment", style="Green.TButton", command=lambda: [self.add_assignment(), main.iconify()], state="disabled" if not file_exists_flag else "normal")
        add_assignment_button.grid(row=2, column=1, pady=10, sticky='w', padx=23)

        edit_assignment_button = ttk.Button(task_actions_frame, text="Edit Assignment", style="Green.TButton", command=lambda: [self.edit_assignment(self.assignments), main.iconify()], state="disabled" if not file_exists_flag else "normal")
        edit_assignment_button.grid(row=2, column=2, pady=10, padx=9)

        delete_button = ttk.Button(task_actions_frame, text="Delete", style="Green.TButton", command=lambda: [self.delete_date(), main.iconify()])
        delete_button.grid(row=3, column=1, pady=10, sticky='w', padx=23)

        other_action_frame = tk.Frame(main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=1)
        other_action_frame.grid(row=2, column=1, sticky="nsw", padx=10, pady=50)

        other_header = tk.Label(other_action_frame, text="Module Actions             ", font=("Arial", 20), bg="white", fg="black")
        other_header.grid(row=0, column=1, pady=10, padx=10, columnspan=2)

        add_modules_button = ttk.Button(other_action_frame, text="Add Modules", style="Green.TButton", command=lambda: [self.add_modules_popup(add_modules_button, add_button, clear_modules_button, add_assignment_button, edit_assignment_button, edit_button), main.iconify()], state="disabled" if file_exists_flag else "normal")
        add_modules_button.grid(row=1, column=1, pady=10, sticky='w', padx=23)

        clear_modules_button = ttk.Button(other_action_frame, text="Clear Modules", style="Green.TButton", command=lambda: self.clear_modules(add_modules_button, add_button, clear_modules_button, add_assignment_button, edit_assignment_button, edit_button), state="normal" if file_exists_flag else "disabled")
        clear_modules_button.grid(row=1, column=2, pady=10, padx=25)

        view_key_button = ttk.Button(other_action_frame, text="View Key", style="Green.TButton", command= lambda: [self.view_key(), main.iconify()])
        view_key_button.grid(row=2, column=1, pady=10, sticky='w', padx=23)

    # Validation functions

    def time_values(self):
        times = []
        postfix = 'AM'
        for minute in range(0, 1440):
            if minute >= 720:
                postfix = 'PM'
            hour = minute // 60
            minutes = minute - (hour * 60)
            if hour < 10:
                hour = f'0{hour}'
            if minutes < 10:
                minutes = f'0{minutes}'
            times.append(f'{hour}:{minutes} {postfix}')

        return times

    def entry_validation(self, **kwargs):
        for entry_name, entry_value in kwargs.items():
            if entry_value == "" or entry_value == " ":
                messagebox.showerror(title="Error", message=f"{entry_name} must be filled")
                return False
        return True

    def dropdown_validation(self, dropdowns):
        for dropdown_name, dropdown_value, dropdown_values in dropdowns:
            if dropdown_value == "" or dropdown_value == " ":
                messagebox.showerror(title="Error", message=f"{dropdown_name} must be selected")
                return False
            elif dropdown_value not in dropdown_values:
                messagebox.showerror(title="Error", message=f"Invalid selection in {dropdown_name}")
                return False
            return True

    def date_validation(self, date):
        if not datetime.strptime(str(date), "%Y-%m-%d"):
            messagebox.showinfo(title='Error', message='Date is invalid')
            return False
        else:
            return True

    def time_validation(self, type, selected_time):
        if type == 'end' and selected_time == '00:00 AM':
            messagebox.showinfo(title='Error', message='End time must be current day')
            return False
        all_times = self.time_values()
        for time in all_times:
            if time == selected_time:
                return True
        messagebox.showinfo(title='Error', message=f'{type} time is invalid')
        return False

    def start_end_time_validation(self, start_time, end_time):
        stripped_start = start_time.strip(":APM ")
        stripped_start = stripped_start.replace(":", "")
        stripped_end = end_time.strip(":APM ")
        stripped_end = stripped_end.replace(":", "")

        if int(stripped_start) > int(stripped_end):
            messagebox.showinfo(title='Error', message='Start time must be ealier than end time')
            return False
        else:
            return True
        
        

    def on_task_submit(self, task_id, title, module_chosen, module_dropdown, start_time, end_time, date, submit_type, popup):
        valid = True

        if not self.entry_validation(title=title):
            valid = False
        if not self.dropdown_validation([('module', module_chosen, module_dropdown['values'])]):
            valid = False
        if not self.time_validation('start', start_time) or not self.time_validation('end', end_time):
            valid = False
        if not self.start_end_time_validation(start_time, end_time):
            valid = False
        if not self.date_validation(date):
            valid = False
        
        if valid:
            if submit_type == "Add":
                add_task(self.creds, title, module_chosen, start_time, end_time, date)
                self.saved_states()
                self.construct_checklist()
                popup.destroy()
                main.deiconify()
            elif submit_type == "Edit":
                edit_task(self.creds, task_id, title, module_chosen, start_time, end_time, date)
                self.saved_states()
                self.construct_checklist()
                popup.destroy()
                main.deiconify()

    def on_assignment_submit(self, assignment_id, title, module_chosen, module_dropdown, due_date, due_time, submit_type, popup):
        valid = True

        if not self.entry_validation(title=title):
            valid = False
        if not self.dropdown_validation([("module", module_chosen, module_dropdown['values'])]):
            valid = False
        if not self.date_validation(due_date):
            valid = False
        if not self.time_validation("due", due_time):
            valid = False
        
        if valid:
            if submit_type == "Add":
                add_assignment(self.creds, title, module_chosen, due_date, due_time)
                self.saved_states()
                self.construct_checklist()
                popup.destroy()
                main.deiconify()
            elif submit_type == "Edit":
                edit_assignment(self.creds, assignment_id, title, module_chosen, due_date, due_time)
                self.saved_states()
                self.construct_checklist()
                popup.destroy()
                main.deiconify()

    def on_modules_submit(self, module_1, module_2, module_3, popup):
        valid = True

        if not self.entry_validation(module_1=module_1, module_2=module_2, module_3=module_3):
            valid = False

        if valid:
            add_modules(module_1, module_2, module_3)
            self.saved_states()
            self.construct_checklist()
            popup.destroy()
            main.deiconify()


    # Popup functions

    def add_task_popup(self):
        self.add_popup = tk.Toplevel(self.main)
        self.add_popup.title("Add Task")
        self.add_popup.geometry("360x430")
        self.add_popup.configure(bg="white")
        self.add_popup.resizable(False, False)
        self.add_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.add_popup: self.on_popup_close(arg))

        header = tk.Label(self.add_popup, text= "Add Task", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, pady=10, columnspan=2)

        title_label = tk.Label(self.add_popup, text="Title", font=('Arial', 15), bg="white", fg="black")
        title_label.grid(row=1, column=0, pady=15, padx=10)
        title_entry = tk.Entry(self.add_popup, font=('Arial', 15), bg="white", fg="black")
        title_entry.grid(row=1, column=1, pady=15, sticky='w')

        module_dropdown_label = tk.Label(self.add_popup, text="Module", font=('Arial', 15), bg="white", fg="black")
        module_dropdown_label.grid(row=2, column=0, pady=15, padx=10)
        module_var = tk.StringVar(self.add_popup)
        module_dropdown = ttk.Combobox(self.add_popup, width=19, textvariable=module_var)

        with open(working_modules_path, 'r') as file:
            modules = json.load(file)
            module_dropdown['values'] = (modules['10'], modules['9'], modules['6'], modules['8'])

        module_dropdown.grid(row=2, column=1, pady=15, sticky='w')

        date_label = tk.Label(self.add_popup, text="Date", font=('Arial', 15), bg="white", fg="black")
        date_label.grid(row=3, column=0, pady=15, padx=10)
        date_chooser = DateEntry(self.add_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        date_chooser.grid(row=3, column=1, pady=15, sticky='w')

        start_time_label = tk.Label(self.add_popup, text="Start Time", font=('Arial', 15), bg="white", fg="black")
        start_time_label.grid(row=4, column=0, pady=15, padx=10)

        start_time_picker = tk.Spinbox(self.add_popup, values=self.time_values(), wrap=True, repeatinterval=10, font=("Arial", 15), bg='white', fg="green", width=18)
        start_time_picker.grid(row=4, column=1, pady=15, sticky='w')

        end_time_label = tk.Label(self.add_popup, text="End Time", font=('Arial', 15), bg="white", fg="black")
        end_time_label.grid(row=5, column=0, pady=15, padx=10)

        end_time_picker = tk.Spinbox(self.add_popup, values=self.time_values(), wrap=True, repeatinterval=10, font=("Arial", 15), bg='white', fg="green", width=18)
        end_time_picker.grid(row=5, column=1, pady=15, sticky='w')

        add_task_button = ttk.Button(self.add_popup, text="Add", style="Green.TButton", command=lambda: self.on_task_submit(None, title_entry.get(), module_dropdown.get(), module_dropdown, start_time_picker.get(), end_time_picker.get(), date_chooser.get_date(), "Add", self.add_popup))
        add_task_button.grid(row=6, column=0, pady=15, columnspan=2)

    def edit_task_popup(self, events):

        def task_to_edit(event):
            task = task_chosen.get()
            task_id = next(x[0] for x in self.events if x[1] == task)
            details = retrieve_event_details(self.creds, task_id)
            edit_popup_specific(details, task_id)

        self.edit_popup = tk.Toplevel(self.main)
        self.edit_popup.title("Edit Task")
        self.edit_popup.geometry("360x480")
        self.edit_popup.configure(bg="white")
        self.edit_popup.resizable(False, False)
        self.edit_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.edit_popup: self.on_popup_close(arg))
        header = tk.Label(self.edit_popup, text= "Edit Task", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, columnspan=2, pady=10, padx=100)

        if events == []:
            no_events_label = tk.Label(self.edit_popup, text="No tasks to edit", font=('Arial', 15), bg="white", fg="black")
            no_events_label.grid(row=1, column=0)
        else:
            dropdown_label = tk.Label(self.edit_popup, text="Task", font=('Arial', 15), bg="white", fg="black")
            dropdown_label.grid(row=1, column=0, pady=15)
            task_var = tk.StringVar(self.edit_popup)
            task_chosen = ttk.Combobox(self.edit_popup, width=19, textvariable=task_var)
            task_chosen['values'] = [x[1] for x in self.events]
            task_chosen.grid(row=1, column=1, pady=15, sticky='w')
            task_chosen.bind("<<ComboboxSelected>>", task_to_edit)

        def edit_popup_specific(details, task_id):
            # Autofill fields with selected task details
            title_label = tk.Label(self.edit_popup, text="Title", font=('Arial', 15), bg="white", fg="black")
            title_label.grid(row=2, column=0, pady=15)
            title_entry = tk.Entry(self.edit_popup, font=('Arial', 15), bg="white", fg="black")
            title_entry.insert(0, str(details["summary"]))
            title_entry.grid(row=2, column=1, pady=15, sticky='w')

            module_dropdown_label = tk.Label(self.edit_popup, text="Module", font=('Arial', 15), bg="white", fg="black")
            module_dropdown_label.grid(row=3, column=0, pady=15)
            module_var = tk.StringVar(self.edit_popup)
            module_dropdown = ttk.Combobox(self.edit_popup, width=19, textvariable=module_var)

            with open(working_modules_path, "r") as f:
                modules = json.load(f)
                module = modules[f'{details["colorId"]}']
                module_dropdown['values'] = (modules['10'], modules['9'], modules['6'], modules['8'])

            values = module_dropdown['values']
            index = values.index(module)
            module_dropdown.current(index)
            module_dropdown.grid(row=3, column=1, pady=15, sticky='w')

            date_label = tk.Label(self.edit_popup, text="Date", font=('Arial', 15), bg="white", fg="black")
            date_label.grid(row=4, column=0, pady=15)
            date_chooser = DateEntry(self.edit_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            date_chooser.delete(0, "end")
            start_date_time = details["start"]
            end_date_time = details["end"]
            date_chooser.set_date(start_date_time[:-15])
            date_chooser.grid(row=4, column=1, pady=15, sticky='w')

            start_time_label = tk.Label(self.edit_popup, text="Start Time", font=('Arial', 15), bg="white", fg="black")
            start_time_label.grid(row=5, column=0, pady=15)

            all_times = self.time_values()

            for time in all_times:
                if (time[:-3]) == start_date_time[11:-9]:
                    start_time = time
                if (time[:-3]) == end_date_time[11:-9]:
                    end_time = time

            start_time_var = tk.StringVar(self.edit_popup)
            start_time_picker = tk.Spinbox(self.edit_popup, values=self.time_values(), wrap=True, repeatinterval=10, font=("Arial", 15), bg='white', fg="green", width=18, textvariable=start_time_var)
            start_time_picker.delete(0, tk.END)
            start_time_picker.insert(0, start_time)
            start_time_var.set(start_time)
            start_time_picker.grid(row=5, column=1, pady=15, sticky='w')

            end_time_label = tk.Label(self.edit_popup, text="End Time", font=('Arial', 15), bg="white", fg="black")
            end_time_label.grid(row=6, column=0, pady=15)

            end_time_var = tk.StringVar(self.edit_popup)
            end_time_picker = tk.Spinbox(self.edit_popup, values=self.time_values(), wrap=True, repeatinterval=10, font=("Arial", 15), bg='white', fg="green", width=18, textvariable=end_time_var)
            end_time_picker.delete(0, tk.END)
            end_time_picker.insert(0, end_time)
            end_time_var.set(end_time)
            end_time_picker.grid(row=6, column=1, pady=15, sticky='w')

            edit_task_button = ttk.Button(self.edit_popup, text="Save", style="Green.TButton", command=lambda: self.on_task_submit(task_id, title_entry.get(), module_dropdown.get(), module_dropdown, start_time_picker.get(), end_time_picker.get(), date_chooser.get_date(), "Edit", self.edit_popup))
            edit_task_button.grid(row=7, column=0, pady=8, columnspan=2)

    def delete_task_popup(self, specified_date):
        def get_task_id(task_title):
            for event in events:
                if event[1] == task_title:
                    task_id = event[0]
            delete_task(self.creds, task_id)
            self.saved_states()
            self.construct_checklist()
            main.deiconify()
            self.delete_popup.destroy()
            self.delete_date_popup.destroy()
        
        self.delete_popup = tk.Toplevel(self.main)
        self.delete_popup.title("Delete Task/Assignment")
        self.delete_popup.geometry("400x180")
        self.delete_popup.configure(bg="white")
        self.delete_popup.resizable(False, False)
        self.delete_popup.protocol("WM_DELETE_WINDOW", lambda: [self.delete_date_popup.deiconify(), self.delete_popup.destroy()])
        header = tk.Label(self.delete_popup, text= "Delete Task/Assignment", font=('Arial', 26), bg="white", fg="Green")
        header.grid(row=0, column=0, columnspan=2, padx=15, pady=10)

        events = get_event_by_date(self.creds, specified_date)
        event_to_delete = True
        for event in events:
            if event[1] == 'No tasks/assignments to delete':
                event_to_delete = False
        print([x[1] for x in events])

        dropdown_label = tk.Label(self.delete_popup, text="Task", font=('Arial', 15), bg="white", fg="black")
        dropdown_label.grid(row=1, column=0, pady=15)
        task_var = tk.StringVar(self.delete_popup)
        task_chosen = ttk.Combobox(self.delete_popup, width=19, textvariable=task_var, state='readonly')
        task_chosen['values'] = [x[1] for x in events]
        task_chosen.grid(row=1, column=1, pady=15, sticky='w')

        delete_task_button = ttk.Button(self.delete_popup, text="Delete", style="Green.TButton", state='disabled' if not event_to_delete else 'normal', command=lambda: get_task_id(task_chosen.get()))
        delete_task_button.grid(row=2, column=0, columnspan=2, pady=10)


    def delete_date(self):
        self.delete_date_popup = tk.Toplevel(self.main)
        self.delete_date_popup.title("Delete Task/Assignment")
        self.delete_date_popup.geometry("400x180")
        self.delete_date_popup.configure(bg="white")
        self.delete_date_popup.resizable(False, False)
        self.delete_date_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.delete_date_popup: self.on_popup_close(arg))
        header = tk.Label(self.delete_date_popup, text= "Delete Task/Assignment", font=('Arial', 26), bg="white", fg="Green")
        header.grid(row=0, column=0, columnspan=2, padx=15, pady=10)

        date_label = tk.Label(self.delete_date_popup, text="Select Date", font=('Arial', 15), bg="white", fg="black")
        date_label.grid(row=1, column=0, pady=15)
        date_chooser = DateEntry(self.delete_date_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        date_chooser.grid(row=1, column=1, pady=15, sticky='w')

        submit_date_button = ttk.Button(self.delete_date_popup, text="Continue", style="Green.TButton", command=lambda: [self.delete_task_popup(date_chooser.get_date()), self.delete_date_popup.iconify()])
        submit_date_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_assignment(self):
        self.add_assignment_popup = tk.Toplevel(self.main)
        self.add_assignment_popup.title("Add Assignment")
        self.add_assignment_popup.geometry("400x360")
        self.add_assignment_popup.configure(bg="white")
        self.add_assignment_popup.resizable(False, False)
        self.add_assignment_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.add_assignment_popup: self.on_popup_close(arg))
        header = tk.Label(self.add_assignment_popup, text= "Add Assignment", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, padx=65, pady=10, columnspan=2)

        title_label = tk.Label(self.add_assignment_popup, text="Title", font=('Arial', 15), bg="white", fg="black")
        title_label.grid(row=1, column=0, pady=15)
        title_entry = tk.Entry(self.add_assignment_popup, font=('Arial', 15), bg="white", fg="black")
        title_entry.grid(row=1, column=1, pady=15, sticky='w')

        module_dropdown_label = tk.Label(self.add_assignment_popup, text="Module", font=('Arial', 15), bg="white", fg="black")
        module_dropdown_label.grid(row=2, column=0, pady=15)
        module_var = tk.StringVar(self.add_assignment_popup)
        module_dropdown = ttk.Combobox(self.add_assignment_popup, width=19, textvariable=module_var)

        with open(working_modules_path, 'r') as file:
            modules = json.load(file)
            module_dropdown['values'] = (modules['10'], modules['9'], modules['6'], modules['8'])

        module_dropdown.grid(row=2, column=1, pady=15, sticky='w')

        date_label = tk.Label(self.add_assignment_popup, text="Date Due", font=('Arial', 15), bg="white", fg="black")
        date_label.grid(row=3, column=0, pady=15)
        date_chooser = DateEntry(self.add_assignment_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        date_chooser.grid(row=3, column=1, pady=15, sticky='w')

        time_label = tk.Label(self.add_assignment_popup, text="Time Due", font=('Arial', 15), bg="white", fg="black")
        time_label.grid(row=4, column=0, pady=15)

        time_picker = tk.Spinbox(self.add_assignment_popup, values=self.time_values(), wrap=True, repeatinterval=10, font=("Arial", 15), bg='white', fg="green", width=18)
        time_picker.grid(row=4, column=1, pady=15, sticky='w')

        add_assignment_button = ttk.Button(self.add_assignment_popup, text="Add", style="Green.TButton", command=lambda: self.on_assignment_submit(None, title_entry.get(), module_dropdown.get(), module_dropdown, date_chooser.get_date(), time_picker.get(), "Add", self.add_assignment_popup))
        add_assignment_button.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_assignment(self, assignments):
        def assignment_to_edit(event):
            assignment = assignment_chosen.get()
            assignment_id = next(x[0] for x in self.assignments if x[1] == assignment)
            details = retrieve_assignment_details(self.creds, assignment_id)
            edit_popup_specific(details, assignment_id)

        self.edit_assignment_popup = tk.Toplevel(self.main)
        self.edit_assignment_popup.title("Edit Assignment")
        self.edit_assignment_popup.geometry("400x420")
        self.edit_assignment_popup.configure(bg="white")
        self.edit_assignment_popup.resizable(False, False)
        self.edit_assignment_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.edit_assignment_popup: self.on_popup_close(arg))
        header = tk.Label(self.edit_assignment_popup, text= "Edit Assignment", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, columnspan=2, padx=70, pady=10)

        if assignments == []:
            no_events_label = tk.Label(self.edit_assignment_popup, text="No assignments to edit", font=('Arial', 15), bg="white", fg="black")
            no_events_label.grid(row=1, column=0, columnspan=2)
        else:
            dropdown_label = tk.Label(self.edit_assignment_popup, text="Assignment", font=('Arial', 15), bg="white", fg="black")
            dropdown_label.grid(row=1, column=0, pady=15)
            assignment_var = tk.StringVar(self.edit_assignment_popup)
            assignment_chosen = ttk.Combobox(self.edit_assignment_popup, width=19, textvariable=assignment_var)
            assignment_chosen['values'] = [x[1] for x in self.assignments]
            assignment_chosen.grid(row=1, column=1, pady=15, sticky='w')
            assignment_chosen.bind("<<ComboboxSelected>>", assignment_to_edit)

        def edit_popup_specific(details, assignment_id):
            title_label = tk.Label(self.edit_assignment_popup, text="Title", font=('Arial', 15), bg="white", fg="black")
            title_label.grid(row=2, column=0, pady=15)
            title_entry = tk.Entry(self.edit_assignment_popup, font=('Arial', 15), bg="white", fg="black")
            title_entry.insert(0, str(details["summary"]))
            title_entry.grid(row=2, column=1, pady=15, sticky='w')

            module_dropdown_label = tk.Label(self.edit_assignment_popup, text="Module", font=('Arial', 15), bg="white", fg="black")
            module_dropdown_label.grid(row=3, column=0, pady=15)
            module_var = tk.StringVar(self.edit_assignment_popup)
            module_dropdown = ttk.Combobox(self.edit_assignment_popup, width=19, textvariable=module_var)
            with open(working_modules_path, "r") as f:
                modules = json.load(f)
                module = modules[f'{details["colorId"]}']
                module_dropdown['values'] = (modules['10'], modules['9'], modules['6'], modules['8'])

            values = module_dropdown['values']
            index = values.index(module)
            module_dropdown.current(index)
            module_dropdown.grid(row=3, column=1, pady=15, sticky='w')

            due_date_label = tk.Label(self.edit_assignment_popup, text="Date Due", font=('Arial', 15), bg="white", fg="black")
            due_date_label.grid(row=4, column=0, pady=15)
            due_date_chooser = DateEntry(self.edit_assignment_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            due_date_chooser.delete(0, "end")
            due_date_time = details["start"]
            due_date_chooser.set_date(due_date_time[:-15])
            due_date_chooser.grid(row=4, column=1, pady=15, sticky='w')

            due_time_label = tk.Label(self.edit_assignment_popup, text="Time Due", font=('Arial', 15), bg="white", fg="black")
            due_time_label.grid(row=5, column=0, pady=15)

            all_times = self.time_values()

            for time in all_times:
                if (time[:-3]) == due_date_time[11:-9]:
                    due_time = time

            due_time_var = tk.StringVar(self.edit_assignment_popup)
            due_time_picker = tk.Spinbox(self.edit_assignment_popup, values=self.time_values(), wrap=True, repeatinterval=10, font=("Arial", 15), bg='white', fg="green", width=18, textvariable=due_time_var)
            due_time_picker.delete(0, tk.END)
            due_time_picker.insert(0, due_time)
            due_time_var.set(due_time)
            due_time_picker.grid(row=5, column=1, pady=15, sticky='w')

            edit_assignment_button = ttk.Button(self.edit_assignment_popup, text="Save", style="Green.TButton", command=lambda: self.on_assignment_submit(assignment_id, title_entry.get(), module_dropdown.get(), module_dropdown, due_date_chooser.get_date(), due_time_picker.get(), "Edit", self.edit_assignment_popup))
            edit_assignment_button.grid(row=7, column=0, pady=8, columnspan=2)


    def view_key(self):
        self.key_popup = tk.Toplevel(self.main)
        self.key_popup.title("View Key")
        self.key_popup.geometry("400x450")
        self.key_popup.configure(bg="white")
        self.key_popup.resizable(False, False)
        self.key_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.key_popup: self.on_popup_close(arg))
        header = tk.Label(self.key_popup, text= "Key", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, padx=170, pady=10)

        modules_frame = tk.Frame(self.key_popup, width=30, height=20, bg="white", highlightbackground="green", highlightthickness=1)
        modules_frame.grid(row=1, column=0, pady=15)

        i = 0
        if file_exists(working_modules_path):
            with open(working_modules_path, 'r') as file:
                modules_data = json.load(file)
                for module in modules_data.values():
                    module_label = tk.Label(modules_frame, text=module, font=('Arial', 15), bg="white", fg="black")
                    module_label.grid(row=i, column=0, padx=30, pady=20)
                    i += 1
                
                canvas = tk.Canvas(modules_frame, width=70, height=300, bg="white", highlightbackground="white", highlightthickness=1)
                canvas.grid(row=0, column=1, padx=20, pady=20, rowspan=4)
        
                # Draw ovals at different Y positions within the canvas
                canvas.create_oval(10, 15, 30, 35, fill="green", outline="dark green") 
                canvas.create_oval(10, 100, 30, 120, fill="blue", outline="blue")     
                canvas.create_oval(10, 185, 30, 205, fill="orange", outline="orange")
                canvas.create_oval(10, 270, 30, 290, fill="grey", outline="grey")

        else:
            no_modules_label = tk.Label(modules_frame, text="No modules added", font=('Arial', 15), bg="white", fg="black")
            no_modules_label.grid(row=0, column=0, padx=30, pady=20)





    def add_modules_popup(self, button_to_disable, button_to_enable_1, button_to_enable_2, button_to_enable_3, button_to_enable_4, button_to_enable_5):

        self.modules_popup = tk.Toplevel(self.main)
        self.modules_popup.title("Add Modules")
        self.modules_popup.geometry("400x325")
        self.modules_popup.configure(bg="white")
        self.modules_popup.resizable(False, False)
        self.modules_popup.protocol("WM_DELETE_WINDOW", lambda arg=self.modules_popup: self.on_popup_close(arg))
        header = tk.Label(self.modules_popup, text= "Add Modules", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, padx=90, pady=10, columnspan=2)

        module_1_label = tk.Label(self.modules_popup, text="Module 1", font=('Arial', 15), bg="white", fg="black")
        module_1_label.grid(row=1, column=0, pady=15)
        module_1_entry = tk.Entry(self.modules_popup, font=('Arial', 15), bg="white", fg="black")
        module_1_entry.grid(row=1, column=1, pady=15, sticky='w')

        module_2_label = tk.Label(self.modules_popup, text="Module 2", font=('Arial', 15), bg="white", fg="black")
        module_2_label.grid(row=2, column=0, pady=15)
        module_2_entry = tk.Entry(self.modules_popup, font=('Arial', 15), bg="white", fg="black")
        module_2_entry.grid(row=2, column=1, pady=15, sticky='w')

        module_3_label = tk.Label(self.modules_popup, text="Module 3", font=('Arial', 15), bg="white", fg="black")
        module_3_label.grid(row=3, column=0, pady=15)
        module_3_entry = tk.Entry(self.modules_popup, font=('Arial', 15), bg="white", fg="black")
        module_3_entry.grid(row=3, column=1, pady=15, sticky='w')

        def save_modules():
            self.on_modules_submit(module_1_entry.get(), module_2_entry.get(), module_3_entry.get(), self.modules_popup)
            button_to_disable.config(state="disabled")
            button_to_enable_1.config(state="normal")
            button_to_enable_2.config(state="normal")
            button_to_enable_3.config(state="normal")
            button_to_enable_4.config(state="normal")
            button_to_enable_5.config(state="normal")

        add_modules_button = ttk.Button(self.modules_popup, text="Save", style="Green.TButton", command=save_modules)
        add_modules_button.grid(row=4, column=0, pady=15, columnspan=2)

    def clear_modules(self, button_to_enable, button_to_disable_1, button_to_disable_2, button_to_disable_3, button_to_disable_4, button_to_disable_5):
        if file_exists(working_modules_path):
            os.remove(working_modules_path)
        else:
            messagebox.showerror(title='Error', message='There are no modules to delete')

        button_to_disable_1.config(state="disabled")
        button_to_disable_2.config(state="disabled")
        button_to_disable_3.config(state="disabled")
        button_to_disable_4.config(state="disabled")
        button_to_disable_5.config(state="disabled")
        button_to_enable.config(state="normal")

    # On close functions

    def saved_states(self):
        """
        Function to save the state of the main window when it is closed.
        """

        with open(working_checkbox_path, 'w') as file:
            states = {id : var.get() for id, var in zip([x[0] for x in self.events], self.task_vars)} # Pairs the summary with the variable, allowing to iterate through the lists simultaneously.
            json.dump(states, file)

    def on_main_close(self):
        """
        Function to handle the close event of the main window.
        """
        self.saved_states()
        main.destroy()
    
    def on_popup_close(self, popup):
        """
        Function to handle the close event of a popup window.
        """
        self.saved_states()
        popup.destroy()
        main.deiconify()

if __name__ == '__main__':
    main = tk.Tk()
    app = StudentPlannerApp(main)
    main.protocol("WM_DELETE_WINDOW", app.on_main_close)  # Set the close event handler
    main.mainloop()

