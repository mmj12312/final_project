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
        self.due_date = due_date

class Tasks:
    """A list of `Task` objects."""

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
        incomplete_tasks = [task for task in self.tasks if task.completed is None]
        incomplete_tasks.sort(key=lambda task: (task.due_date or datetime.max, -task.priority))
        
        print("\nID   Age  Due Date   Priority   Task")
        print("--   ---  --------   --------   ----")
        for task in incomplete_tasks:
            age = (datetime.now() - task.created).days
            print(f"{task.id}  {age}   {task.due_date}   {task.priority}   {task.name}")

    def report(self):
        print("\nID   Age  Due Date   Priority   Task                Created                       Completed")
        print("--   ---  --------   --------   ----                ---------------------------   -------------------------")
        for task in sorted(self.tasks, key=lambda x: (x.due_date, -x.priority)):
            age = (datetime.now() - task.created).days
            print(f"{task.id}  {age}   {task.due_date}   {task.priority}   {task.name}     {task.created}        {task.completed}")

    def done(self, id):
        for task in self.tasks:
            if task.id == id:
                task.completed = datetime.now()
                return f"Completed task {id}"

    def query(self, terms):
        result_tasks = [task for task in self.tasks if task.completed is None and any(term.lower() in task.name.lower() for term in terms)]
        result_tasks.sort(key=lambda task: (task.due_date or datetime.max, -task.priority))

        print("\nID   Age  Due Date   Priority   Task")
        print("--   ---  --------   --------   ----")
        for task in result_tasks:
            age = (datetime.now() - task.created).days
            print(f"{task.id}  {age}   {task.due_date}   {task.priority}   {task.name}")


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

        input = input("Enter command: ").strip().split()

        if not input:
            continue

        command = input[0].lower()

        if command == "--add":
            index_n = input.index('--add') + 1
            name = input[index_n]
            index_d = input.index('--due') + 1 if '--due' in input else None
            due_date = input[index_d] if index_d is not None else None
            index_p = input.index('--priority') + 1 if '--priority' in input else None
            priority = int(input[index_p]) if index_p is not None else 1

            result = tasks_manager.add(name, due_date, priority)
            print(result)

        elif command == "--list":
            tasks_manager.list()

        elif command == "--report":
            tasks_manager.report()

        elif command == "--done":
            task_id_index = input.index('--done') + 1
            task_id = int(input[task_id_index])
            result = tasks_manager.done(task_id)
            print(result)

        elif command == "--query":
            search_term_index = input.index('--query') + 1
            search_terms = input[search_term_index:]
            tasks_manager.query(*search_terms)

        elif command == "--delete":
            task_id_index = input.index('--delete') + 1
            task_id = int(input[task_id_index])
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