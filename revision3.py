# Add status bar functionality
def create_window():
    root = tk.Tk()
    # ... (previous setup)
    
    status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status.pack(fill=tk.X)
    
    def refresh_with_status(tree, status):
        status.config(text="Refreshing...")
        tree.update()
        refresh(tree)
        status.config(text=f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}")
    
    # Update button command
    tk.Button(btn_frame, text="Refresh", 
             command=lambda: refresh_with_status(tree, status)).pack()