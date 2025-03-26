# Add auto-refresh toggle
def toggle_auto_refresh(var, tree, status, root):
    if var.get():
        auto_refresh(tree, status, root)

def auto_refresh(tree, status, root):
    refresh_with_status(tree, status)
    root.after(5000, lambda: auto_refresh(tree, status, root))

# Add checkbox to UI
    auto_refresh_var = tk.IntVar()
    tk.Checkbutton(btn_frame, text="Auto-refresh", 
                 variable=auto_refresh_var,
                 command=lambda: toggle_auto_refresh(
                     auto_refresh_var, tree, status, root)).pack()