import datetime
import pickle
import os
from datetime import datetime


class Task:
    """Representation of a task
  
    Attributes:
                - created - date
                - completed - date
                - name - string
                - unique id - number
                - priority - int value of 1, 2, or 3; 1 is default
                - due date - date, this is optional
    """
    id_counter = 1

    def __init__(self, name, due_date=None, priority=1):
        self.created = datetime.now()
        self.completed = None
        self.name = name
        self.id = Task.id_counter
        Task.id_counter += 1
        self.priority = priority
        self.due_date = self.parse_due_date(due_date)
    
    def parse_due_date(self, due_date):
        if due_date:
            try:
                return datetime.strptime(due_date, '%m/%d/%Y')
            except ValueError:
                print("Invalid due date format. Due date set to None.")
        return None

class Tasks:
    """A list of `Task` objects."""

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self):
        """Read pickled tasks file into a list"""
        self.tasks = []
        if os.path.exists('.todo.pickle'):
            with open('.todo.pickle', 'rb') as f:
                self.tasks = pickle.load(f)

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open('.todo.pickle', 'wb') as f:
            pickle.dump(self.tasks, f)

    def list(self):
        tt = [task for task in self.tasks if task.completed is None]
        tt.sort(key=lambda task: (task.due_date or datetime.max, -task.priority))
        
        print("{:<4} {:<5} {:<12} {:<10} {}".format("ID", "Age", "Due Date", "Priority", "Task"))
        print("-" * 4 + " " + "-" * 5 + " " + "-" * 12 + " " + "-" * 10 + " " + "-" * 5)
        for task in tt:
            age = (datetime.now() - task.created).days
            if task.due_date:
                due_date_str = f"{task.due_date.month}/{task.due_date.day}/{task.due_date.year}"
            else:
                due_date_str = "-"
            print("{:<4} {:<5} {:<12} {:<10} {}".format(task.id, age, due_date_str, task.priority, task.name))
    
    def format_date(self, date):
        day_name = self.day_names[date.weekday()]
        month_name = self.month_names[date.month]
        formatted_date = (
            f"{day_name} {month_name} {date.day:02} "
            f"{date.hour:02}:{date.minute:02}:{date.second:02} CST {date.year}"
        )
        return formatted_date

    def report(self):
        print("{:<4} {:<5} {:<12} {:<10} {:<20} {:<30} {:<20} ".format("ID", "Age", "Due Date", "Priority", "Task", "Created", "Completed"))
        print("-" * 4 + " " + "-" * 5 + " " + "-" * 11 + " " + "-" * 10 + " " + "-" * 20 + " " + "-" * 30 + " " + "-" * 30)
        def sorting_key(task):
            return (task.due_date or datetime.max, -task.priority, task.created)
        for task in sorted(self.tasks, key=sorting_key):
            age = (datetime.now() - task.created).days
            if task.due_date:
                due_date_str = f"{task.due_date.month}/{task.due_date.day}/{task.due_date.year}"
            else:
                due_date_str = "-"
            created_str = self.format_date(task.created)
            completed_str = self.format_date(task.completed) if task.completed else "-"
            print("{:<4} {:<5} {:<12} {:<10} {:<20} {:<30} {:<20}".format(task.id, age, due_date_str, task.priority, task.name, created_str, completed_str))

    def done(self, id):
        for task in self.tasks:
            if task.id == id:
                task.completed = datetime.now()
                return f"Completed task {id}"

    def query(self, terms):
        result_tasks = [task for task in self.tasks if task.completed is None and any(term.lower() in task.name.lower() for term in terms)]
        result_tasks.sort(key=lambda task: (task.due_date or datetime.max, -task.priority))

        print("{:<4} {:<5} {:<12} {:<10} {}".format("ID", "Age", "Due Date", "Priority", "Task"))
        print("-" * 4 + " " + "-" * 5 + " " + "-" * 12 + " " + "-" * 10 + " " + "-" * 5)
        for task in result_tasks:
            age = (datetime.now() - task.created).days
            if task.due_date:
                due_date_str = f"{task.due_date.month}/{task.due_date.day}/{task.due_date.year}"
            else:
                due_date_str = "-"
            print("{:<4} {:<5} {:<12} {:<10} {}".format(task.id, age, due_date_str, task.priority, task.name))


    def add(self, name, due_date=None, priority=1):
        task = Task(name, due_date, priority)
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x.created)
        return f"Created task {task.id}"

    def delete(self, id):
        for task in self.tasks:
            if task.id == id:
                self.tasks.remove(task)
                return f"Deleted task {id}"


def main():
    tasks_manager = Tasks()
    
    while True:
        print("\nAvailable commands:")
        print("--add 'Task Name' [--due 'Due Date' --priority 'Priority']")
        print("--list")
        print("--report")
        print("--done 'Task ID'")
        print("--query 'Search Term'")
        print("--delete 'Task ID'")
        print("--exit")

        input2 = input("Enter command: ")
        input1 = input2.strip().split()
        def extract_content_between_quotes(input_string):
            start_quote = input_string.find('"')
            end_quote = input_string.find('"', start_quote + 1)

            if start_quote != -1 and end_quote != -1:
                content_between_quotes = input_string[start_quote + 1:end_quote]
                return content_between_quotes
            else:
                return None

        if not input1:
            continue

        command = input1[0].lower()

        if command == "--add":
            index_n = input1.index('--add') + 1
            name = extract_content_between_quotes(input2)
            index_d = input1.index('--due') + 1 if '--due' in input1 else None
            due_date = input1[index_d] if index_d is not None else None
            index_p = input1.index('--priority') + 1 if '--priority' in input1 else None
            priority = int(input1[index_p]) if index_p is not None else 1

            result = tasks_manager.add(name, due_date, priority)
            print(result)

        elif command == "--list":
            tasks_manager.list()

        elif command == "--report":
            tasks_manager.report()

        elif command == "--done":
            task_id_index = input1.index('--done') + 1
            task_id = int(input1[task_id_index])
            result = tasks_manager.done(task_id)
            print(result)

        elif command == "--query":
            search_term_index = input1.index('--query') + 1
            search_terms = input1[search_term_index:]
            tasks_manager.query(*search_terms)

        elif command == "--delete":
            task_id_index = input1.index('--delete') + 1
            task_id = int(input1[task_id_index])
            result = tasks_manager.delete(task_id)
            print(result)

        elif command == "--exit":
            tasks_manager.pickle_tasks()
            print("Exiting the task manager")
            break

        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()