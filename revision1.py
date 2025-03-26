import tkinter as tk
from tkinter import ttk
import psutil

def update_process_list(tree):
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
        tree.insert("", "end", values=(
            proc.info['pid'],
            proc.info['name'],
            proc.info['status'],
            proc.info['cpu_percent'],
            proc.info['memory_info'].rss // 1024
        ))

def create_window():
    root = tk.Tk()
    root.title("Process Monitor")
    
    tree = ttk.Treeview(root, columns=("PID", "Name", "Status", "CPU%", "Memory"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack()
    
    update_process_list(tree)
    root.mainloop()

if __name__ == "__main__":
    create_window()