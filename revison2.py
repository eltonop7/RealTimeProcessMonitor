
def refresh(tree):
    for row in tree.get_children():
        tree.delete(row)
    update_process_list(tree)

# Modify create_window()
def create_window():
    root = tk.Tk()
    # ... (previous tree setup)
    
    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame, text="Refresh", command=lambda: refresh(tree)).pack()
    
    update_process_list(tree)
    root.mainloop()