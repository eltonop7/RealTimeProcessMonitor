import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from datetime import datetime

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Monitor")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Segoe UI', 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))
        self.style.map("Treeview", background=[('selected', '#0078D7')])
        
        self.setup_ui()
        self.update_process_list()
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.header_frame, text="Process Monitor", font=('Segoe UI', 14, 'bold')).pack(side=tk.LEFT)
        
        # Stats frame
        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.cpu_label = ttk.Label(self.stats_frame, text="CPU: --%")
        self.cpu_label.pack(side=tk.LEFT, padx=10)
        
        self.mem_label = ttk.Label(self.stats_frame, text="Memory: --%")
        self.mem_label.pack(side=tk.LEFT, padx=10)
        
        self.process_count_label = ttk.Label(self.stats_frame, text="Processes: --")
        self.process_count_label.pack(side=tk.LEFT, padx=10)
        
        self.last_update_label = ttk.Label(self.stats_frame, text="Last update: --")
        self.last_update_label.pack(side=tk.RIGHT)
        
        # Treeview with scrollbars
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("PID", "Name", "Status", "CPU%", "Memory"), show="headings")
        
        # Configure headings
        headings = [
            ("PID", "PID", 70),
            ("Name", "Name", 250),
            ("Status", "Status", 100),
            ("CPU%", "CPU %", 80),
            ("Memory", "Memory (MB)", 100)
        ]
        
        for col, text, width in headings:
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=width, anchor=tk.CENTER if col in ["PID", "CPU%", "Memory"] else tk.W)
        
        # Add scrollbars
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")
        
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.refresh_btn = ttk.Button(self.button_frame, text="🔄 Refresh", command=self.refresh)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.kill_btn = ttk.Button(self.button_frame, text="⛔ End Process", command=self.kill_process)
        self.kill_btn.pack(side=tk.LEFT, padx=5)
        
        self.search_frame = ttk.Frame(self.button_frame)
        self.search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(self.search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_process)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X)
        
        # Configure auto-refresh
        self.auto_refresh_var = tk.IntVar()
        self.auto_refresh_cb = ttk.Checkbutton(
            self.button_frame, 
            text="Auto-refresh (5s)", 
            variable=self.auto_refresh_var, 
            command=self.toggle_auto_refresh
        )
        self.auto_refresh_cb.pack(side=tk.LEFT, padx=20)
        self.auto_refresh_id = None
    
    def update_process_list(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Get system stats
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        process_count = 0
        
        # Update process list
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
            try:
                self.tree.insert("", "end", values=(
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['status'],
                    f"{proc.info['cpu_percent']:.1f}",
                    f"{proc.info['memory_info'].rss / (1024 * 1024):.1f}"  # Convert to MB
                ))
                process_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Update stats
        self.cpu_label.config(text=f"CPU: {cpu_percent:.1f}%")
        self.mem_label.config(text=f"Memory: {mem_percent:.1f}%")
        self.process_count_label.config(text=f"Processes: {process_count}")
        self.last_update_label.config(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        self.status_bar.config(text=f"Loaded {process_count} processes")
    
    def refresh(self):
        self.status_bar.config(text="Refreshing...")
        self.root.update()  # Force UI update
        self.update_process_list()
        self.status_bar.config(text="Refresh completed")
    
    def kill_process(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a process to end")
            return
            
        pid = self.tree.item(selected[0], 'values')[0]
        try:
            process = psutil.Process(pid)
            process.terminate()
            self.refresh()
            self.status_bar.config(text=f"Process {pid} terminated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate process: {e}")
    
    def search_process(self, event=None):
        query = self.search_var.get().lower()
        if not query:
            for child in self.tree.get_children():
                self.tree.item(child, tags=())
            return
            
        for child in self.tree.get_children():
            values = self.tree.item(child, 'values')
            if any(query in str(value).lower() for value in values):
                self.tree.item(child, tags=('match',))
                self.tree.tag_configure('match', background='#FFF2CC')
            else:
                self.tree.item(child, tags=())
    
    def sort_column(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children()]
        
        # Try to convert to float for numeric columns
        try:
            data.sort(key=lambda x: float(x[0] if x[0] else 0), reverse=self.sort_reverse)
        except ValueError:
            data.sort(reverse=self.sort_reverse)
        
        for index, (_, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.sort_reverse = not self.sort_reverse
    
    def toggle_auto_refresh(self):
        if self.auto_refresh_var.get():
            self.auto_refresh()
        elif self.auto_refresh_id:
            self.root.after_cancel(self.auto_refresh_id)
            self.auto_refresh_id = None
    
    def auto_refresh(self):
        self.refresh()
        self.auto_refresh_id = self.root.after(5000, self.auto_refresh)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()