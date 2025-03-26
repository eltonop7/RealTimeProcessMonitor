import tkinter as tk
from tkinter import ttk
import psutil

def update_process_list():
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
        tree.insert("", "end", values=(
            proc.info['pid'],
            proc.info['name'],
            proc.info['status'],
            proc.info['cpu_percent'],
            proc.info['memory_info'].rss // 1024  
        ))

def refresh():
    for row in tree.get_children():
        tree.delete(row)
    update_process_list()

root = tk.Tk()
root.title("Real-Time Process Monitoring Dashboard")


tree = ttk.Treeview(root, columns=("PID", "Name", "Status", "CPU%", "Memory"), show="headings")
tree.heading("PID", text="PID")
tree.heading("Name", text="Name")
tree.heading("Status", text="Status")
tree.heading("CPU%", text="CPU%")
tree.heading("Memory", text="Memory (KB)")
tree.pack()


refresh_button = tk.Button(root, text="Refresh", command=refresh)
refresh_button.pack()


update_process_list()

root.mainloop()