# gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, PhotoImage
from datetime import datetime
import requests
import pymysql
from mail_analyzer import analyze_email
from config import DB_CONFIG

MAILHOG_API = "http://localhost:8025/api/v2/messages"
seen_ids = set()

# Connect to MySQL
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# Fetch recent emails from MailHog
def fetch_emails():
    try:
        response = requests.get(MAILHOG_API)
        response.raise_for_status()
        return response.json().get("items", [])
    except Exception as e:
        print("❌ Error fetching emails:", e)
        return []

# Extract sender, subject, body, time
def extract_fields(item):
    sender = item['Content']['Headers'].get('From', ['unknown@example.com'])[0]
    subject = item['Content']['Headers'].get('Subject', [''])[0]
    body = item['Content']['Body']
    time_received = datetime.now()
    return sender, subject, body, time_received

# Populate output box with analysis results
def refresh_analysis():
    emails = fetch_emails()
    for item in emails:
        msg_id = item['ID']
        if msg_id not in seen_ids:
            seen_ids.add(msg_id)
            sender, subject, body, time_received = extract_fields(item)
            result = analyze_email(sender, subject, body, time_received)
            display = f"📨 From: {sender}\nSubject: {subject}\nTime: {time_received}\n\n🛡️ Analysis:\n" + "\n".join(result) + "\n" + "-"*80 + "\n"
            analysis_box.insert(tk.END, display)
            analysis_box.yview(tk.END)
    refresh_tables()

# Load table data from MySQL and display in the correct tab
def load_table_data(table_name, tree):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        tree.delete(*tree.get_children())  # Clear old rows
        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error loading {table_name}:", e)

# Load all tables
def refresh_tables():
    load_table_data("trusted", trusted_tree)
    load_table_data("untrusted", untrusted_tree)
    load_table_data("not_spoofed", not_spoofed_tree)
    load_table_data("link_files", link_tree)
    load_table_data("email_hash", hash_tree)
    load_table_data("spoofed", spoofed_tree)

# Build the GUI
def create_gui():
    global analysis_box, trusted_tree, untrusted_tree, not_spoofed_tree, spoofed_tree, link_tree, hash_tree

    root = tk.Tk()
    root.title("📧 Email Spoofing Detection System")
    root.geometry("1080x700")

    # Icon + Header
    try:
        icon = PhotoImage(file="📧.png")  # Replace with your actual icon if available
        root.iconphoto(False, icon)
    except:
        pass

    header = ttk.Label(root, text="📧 Email Spoofing & Threat Detection System", font=("Segoe UI", 18, "bold"))
    header.pack(pady=10)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Tab 1: Live Analysis
    analysis_tab = ttk.Frame(notebook)
    notebook.add(analysis_tab, text="🔍 Live Analysis")

    analysis_box = scrolledtext.ScrolledText(analysis_tab, wrap=tk.WORD, font=("Consolas", 10), width=130, height=30)
    analysis_box.pack(padx=10, pady=10)

    refresh_btn = ttk.Button(analysis_tab, text="🔄 Refresh & Analyze", command=refresh_analysis)
    refresh_btn.pack(pady=5)

    # Tab 2+: Database Tables
    def create_table_tab(name):
        tab = ttk.Frame(notebook)
        tree = ttk.Treeview(tab)
        tree.pack(expand=True, fill="both", padx=10, pady=10)
        notebook.add(tab, text=name)
        return tree

    trusted_tree = create_table_tab("✅ Trusted Emails")
    untrusted_tree = create_table_tab("⚠️ Untrusted Emails")
    not_spoofed_tree = create_table_tab("🔐 Not Spoofed")
    spoofed_tree = create_table_tab("🚨 Spoofed Emails")
    link_tree = create_table_tab("🔗 Link Files")
    hash_tree = create_table_tab("🔑 Email Hashes")

    refresh_tables()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
