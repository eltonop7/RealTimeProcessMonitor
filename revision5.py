# Add search function
def search_process(tree, search_term):
    for child in tree.get_children():
        if search_term.lower() in str(tree.item(child, 'values')).lower():
            tree.item(child, tags=('match',))
        else:
            tree.item(child, tags=('no-match',))
    tree.tag_configure('match', background='yellow')

# Add search entry to UI
    search_frame = tk.Frame(root)
    search_frame.pack()
    tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT)
    search_entry.bind('<KeyRelease>', 
                    lambda e: search_process(tree, search_var.get()))