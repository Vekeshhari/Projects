import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import hashlib

# Class to handle MySQL connection and basic utility methods
class DBConnection:
    @staticmethod
    def create_connection():
        return mysql.connector.connect(
            host='',
            database='task_management00',
            user='root',  # Replace with your MySQL username
            password=''  # Replace with your MySQL password
        )

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

# Base class for both Admin and User
class Person:
    def __init__(self, username):  # Fixed constructor name
        self.username = username

    @staticmethod
    def authenticate_user(username, password):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        hashed_password = DBConnection.hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                       (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user

# User class inheriting from Person
class User(Person):
    def __init__(self, username):  # Fixed constructor name
        super().__init__(username)

    def fetch_tasks(self):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT id, title, description, deadline, status, points FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()
        cursor.close()
        connection.close()
        return tasks

    def mark_as_complete(self, task_id):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        
        # Fetch the points associated with the task
        cursor.execute("SELECT points FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        
        if task:
            points = task[0]
            # Update task status
            cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = %s", (task_id,))
            # Add points to the leaderboard
            cursor.execute(""" 
                UPDATE leaderboard 
                SET points = points + %s 
                WHERE username = %s
            """, (points, self.username))
            
            connection.commit()
            cursor.close()
            connection.close()
            return points  # Return points added
        else:
            cursor.close()
            connection.close()
            return 0  # Return 0 if task not found

    def update_leaderboard(self):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute(""" 
            UPDATE leaderboard 
            SET points = (
                SELECT COALESCE(SUM(points), 0) 
                FROM tasks 
                WHERE user_id = (SELECT id FROM users WHERE username = %s)
            ) 
            WHERE username = %s
        """, (self.username, self.username))
        connection.commit()
        cursor.close()
        connection.close()

    def view_leaderboard(self):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT username, points FROM leaderboard ORDER BY points DESC")
        leaderboard = cursor.fetchall()
        cursor.close()
        connection.close()
        return leaderboard
    
    def update_badges(self):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT points FROM leaderboard WHERE username = %s", (self.username,))
        total_points = cursor.fetchone()[0]
        
        # Fetch all badges that meet the user's points threshold
        cursor.execute("SELECT b.id FROM badges b WHERE b.points_threshold <= %s", (total_points,))
        badges_to_award = cursor.fetchall()

        # Add badges for the user if they don't already have them
        for badge in badges_to_award:
            cursor.execute("SELECT * FROM user_badges WHERE user_id = (SELECT id FROM users WHERE username = %s) AND badge_id = %s", (self.username, badge[0]))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO user_badges (user_id, badge_id) VALUES ((SELECT id FROM users WHERE username = %s), %s)", (self.username, badge[0]))
        
        connection.commit()
        cursor.close()
        connection.close()

    def fetch_badges(self):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT b.badge_name 
            FROM badges b 
            JOIN user_badges ub ON b.id = ub.badge_id 
            JOIN users u ON ub.user_id = u.id 
            WHERE u.username = %s
        """, (self.username,))
        badges = cursor.fetchall()
        cursor.close()
        connection.close()
        return [badge[0] for badge in badges]

# Admin class inheriting from Person
class Admin(Person):
    def __init__(self, username):  # Fixed constructor name
        super().__init__(username)

    def assign_task(self, user_id, task):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:
            messagebox.showerror("User Not Found", f"User with ID {user_id} does not exist.")
            cursor.close()
            connection.close()
            return
        cursor.execute("""INSERT INTO tasks (user_id, title, description, deadline, points, status) 
                          VALUES (%s, %s, %s, %s, %s, 'Pending')""",
                       (user_id, task['title'], task['description'], task['deadline'], task['points']))
        connection.commit()
        cursor.close()
        connection.close()

    def view_progress(self):
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT u.username, COALESCE(SUM(t.points), 0) 
            FROM users u 
            LEFT JOIN tasks t ON u.id = t.user_id AND t.status = 'Completed' 
            GROUP BY u.username
        """)
        progress = cursor.fetchall()
        cursor.close()
        connection.close()
        return progress


# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    user_data = Person.authenticate_user(username, password)

    if user_data:
        role = user_data[3]  # Assuming role is the 4th column in users table (0-indexed)
        if role == 'admin':
            admin = Admin(username)
            messagebox.showinfo("Login Success", f"Welcome , {username}!")
            open_admin_window(admin)
        else:
            user = User(username)
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            open_user_window(user)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to display Admin window
def open_admin_window(admin):
    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")

    tk.Label(admin_window, text="Assign Task to User").grid(row=0, column=0)

    tk.Label(admin_window, text="User ID:").grid(row=1, column=0)
    entry_user_id = tk.Entry(admin_window)
    entry_user_id.grid(row=1, column=1)

    tk.Label(admin_window, text="Task Title:").grid(row=2, column=0)
    entry_title = tk.Entry(admin_window)
    entry_title.grid(row=2, column=1)

    tk.Label(admin_window, text="Task Description:").grid(row=3, column=0)
    entry_desc = tk.Entry(admin_window)
    entry_desc.grid(row=3, column=1)

    tk.Label(admin_window, text="Deadline (YYYY-MM-DD):").grid(row=4, column=0)
    entry_deadline = tk.Entry(admin_window)
    entry_deadline.grid(row=4, column=1)

    tk.Label(admin_window, text="Points:").grid(row=5, column=0)
    entry_points = tk.Entry(admin_window)
    entry_points.grid(row=5, column=1)

    def assign_task():
        user_id = entry_user_id.get()
        task = {
            'title': entry_title.get(),
            'description': entry_desc.get(),
            'deadline': entry_deadline.get(),
            'points': int(entry_points.get())
        }
        admin.assign_task(user_id, task)
        messagebox.showinfo("Task Assigned", "Task successfully assigned!")

    tk.Button(admin_window, text="Assign Task", command=assign_task).grid(row=6, column=1)

    def view_leaderboard():
        progress = admin.view_progress()
        leaderboard_window = tk.Toplevel(admin_window)
        leaderboard_window.title("Leaderboard")
        for idx, (username, points) in enumerate(progress):
            tk.Label(leaderboard_window, text=f"{idx + 1}. {username}: {points} points").grid(row=idx, column=0)

    tk.Button(admin_window, text="View Leaderboard", command=view_leaderboard).grid(row=7, column=1)

    def view_user_badges():
        connection = DBConnection.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()

        badges_window = tk.Toplevel(admin_window)
        badges_window.title("View User Badges")

        for idx, (username,) in enumerate(users):
            user = User(username)
            badges = user.fetch_badges()
            tk.Label(badges_window, text=f"{username}: {', '.join(badges)}").grid(row=idx, column=0)

    tk.Button(admin_window, text="View User Badges", command=view_user_badges).grid(row=8, column=1)

# Function to display User window
def open_user_window(user):
    user_window = tk.Toplevel()
    user_window.title("User Dashboard")

    tk.Label(user_window, text="Your Tasks").grid(row=0, column=0)

    tree = ttk.Treeview(user_window, columns=("ID", "Title", "Status", "Points"))
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Status", text="Status")
    tree.heading("Points", text="Points")
    tree.grid(row=1, column=0, columnspan=4)

    tasks = user.fetch_tasks()
    for task in tasks:
        tree.insert("", "end", values=task)

    def complete_task():
        selected_item = tree.selection()[0]
        task_id = tree.item(selected_item, "values")[0]
        points = user.mark_as_complete(task_id)
        if points > 0:
            messagebox.showinfo("Task Completed", f"Task completed! You earned {points} points.")
            tree.delete(selected_item)  # Removes task from UI
        else:
            messagebox.showerror("Task Error", "Task not found.")

    tk.Button(user_window, text="Complete Task", command=complete_task).grid(row=2, column=0)

    def view_leaderboard():
        leaderboard = user.view_leaderboard()
        leaderboard_window = tk.Toplevel(user_window)
        leaderboard_window.title("Leaderboard")
        for idx, (username, points) in enumerate(leaderboard):
            tk.Label(leaderboard_window, text=f"{idx + 1}. {username}: {points} points").grid(row=idx, column=0)

    tk.Button(user_window, text="View Leaderboard", command=view_leaderboard).grid(row=3, column=0)

    def update_badges():
        user.update_badges()
        messagebox.showinfo("Badges Updated", "Your badges have been updated.")

    tk.Button(user_window, text="Update Badges", command=update_badges).grid(row=4, column=0)

# Main Login Window
root = tk.Tk()
root.title("Login")
tk.Label(root, text="Username:").grid(row=0, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)

tk.Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2)

root.mainloop()
