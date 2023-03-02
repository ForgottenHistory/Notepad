import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import tkinter.font as tkFont

class NotepadApp:
    def __init__(self, master):
        
        self.master = master
        self.master.title("Notepad App")
        
        # Set the default font for the app
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)
        
        # Create the tab widget
        self.tabs = ttk.Notebook(self.master)
        self.tabs.pack(fill=tk.BOTH, expand=1)
        self.tabs.bind("<Button-3>", self.on_tab_close)

        # Add the initial tab
        self.add_tab()

        # Create the menu bar
        self.menu_bar = tk.Menu(self.master)

        # Create the File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Tab", command=self.add_tab)
        file_menu.add_command(label="Close Tab", command=self.close_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Create the Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        edit_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Set the menu bar
        self.master.config(menu=self.menu_bar)

    def add_tab(self):
        text_widget = tk.Text(self.tabs)
        text_widget.configure(font=("Arial", 12))
        self.tabs.add(text_widget, text="Untitled")
        self.tabs.select(text_widget)

    def close_tab(self):
        if len(self.tabs.tabs()) > 1:
            self.tabs.forget(self.tabs.select())

    def on_tab_close(self, event):
        tab_id = event.widget.select()
        tab_text = event.widget.tab(tab_id, "text")
        close_tab_menu = tk.Menu(self.master, tearoff=0)
        close_tab_menu.add_command(label="Close", command=lambda: self.tabs.forget(tab_id))
        close_tab_menu.add_command(label="Cancel")
        close_tab_menu.tk_popup(event.x_root, event.y_root)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
            text_widget = tk.Text(self.tabs)
            text_widget.insert("1.0", text)
            text_widget.file_path = file_path
            file_name = os.path.basename(file_path)
            self.tabs.add(text_widget, text=file_name)
            self.tabs.select(text_widget)

    def save_file(self):
        current_tab = self.tabs.select()
        text_widget = self.tabs.nametowidget(current_tab)
        if hasattr(text_widget, "file_path"):
            with open(text_widget.file_path, "w") as file:
                text = text_widget.get("1.0", "end-1c")
                file.write(text)
        else:
            self.save_file_as()

    def save_file_as(self):
        current_tab = self.tabs.select()
        text_widget = self.tabs.nametowidget(current_tab)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                text = text_widget.get("1.0", "end-1c")
                file.write(text)
            text_widget.file_path = file_path
            self.tabs.tab(current_tab, text=file.name)
    
    def increase_font_size(self):
        current_tab = self.tabs.select()
        text_widget = self.tabs.nametowidget(current_tab)
        font_tuple = tkFont.Font(font=text_widget['font'])
        new_font_size = font_tuple.actual()["size"] + 1
        text_widget.configure(font=(font_tuple.actual()["family"], new_font_size))

    def decrease_font_size(self):
        current_tab = self.tabs.select()
        text_widget = self.tabs.nametowidget(current_tab)
        font_tuple = tkFont.Font(font=text_widget['font'])
        new_font_size = max(font_tuple.actual()["size"] - 1, 1)
        text_widget.configure(font=(font_tuple.actual()["family"], new_font_size))



    
def main():
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
