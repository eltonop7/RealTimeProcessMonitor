# Add kill process function
def kill_process(tree, status):
    selected = tree.selection()
    if not selected:
        return
        
    pid = tree.item(selected[0], 'values')[0]
    try:
        psutil.Process(int(pid)).terminate()
        status.config(text=f"Process {pid} terminated")
    except Exception as e:
        status.config(text=f"Error: {str(e)}")

# Add kill button to create_window()
    tk.Button(btn_frame, text="Kill Process",
             command=lambda: kill_process(tree, status)).pack(side=tk.LEFT)