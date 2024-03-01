import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from customtkinter import CTk, CTkButton
from random import choice
import winsound

class NotepadTab(tk.Frame):
    def __init__(self, master=None, notebook=None):
        super().__init__(master)
        self.notebook = notebook

        self.text_widget = tk.Text(self)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.set_font()
        self.default_bgc()

    def set_font(self):
        self.text_widget.config(font=("Helvetica", 12))

    def default_bgc(self):
        self.text_widget.config(bg="white")

class Notepad(CTk):
    def __init__(self):
        super().__init__()
        self.title("Notepad")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.tabs = []
        self.create_menu()
        self.add_tab()

        self.tip_button = CTkButton(self, text="Tip", command=self.show_random_tip)
        self.tip_button.pack()

        self.switch_frame = tk.Frame(self)
        self.switch_frame.pack()
        self.switch_frame.config(bg="white")

        self.add_color_button("Default", "white")
        self.add_color_button("Red", "#ff9999")
        self.add_color_button("Blue", "#99ccff")
        self.add_color_button("Green", "#99ff99")
        self.add_color_button("Black", "#333333")

    def create_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Tab", command=self.add_tab)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_command(label="Find", command=self.find)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menu_bar)

    def add_tab(self):
        tab_number = len(self.tabs) + 1
        tab_name = f"Tab {tab_number}"
        tab = NotepadTab(self.notebook)
        self.notebook.add(tab, text=tab_name)
        self.tabs.append(tab)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                self.get_current_tab().text_widget.delete("1.0", tk.END)
                self.get_current_tab().text_widget.insert("1.0", text)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                text = self.get_current_tab().text_widget.get("1.0", tk.END)
                file.write(text)
            messagebox.showinfo("Info", "File saved successfully!")

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                text = self.get_current_tab().text_widget.get("1.0", tk.END)
                file.write(text)
            messagebox.showinfo("Info", "File saved successfully!")

    def cut(self):
        self.get_current_tab().text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.get_current_tab().text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.get_current_tab().text_widget.event_generate("<<Paste>>")

    def find(self):
        find_dialog = tk.Toplevel(self)
        find_dialog.title("Find")

        find_label = tk.Label(find_dialog, text="Find:")
        find_label.grid(row=0, column=0)

        find_entry = tk.Entry(find_dialog)
        find_entry.grid(row=0, column=1)

        find_button = tk.Button(find_dialog, text="Find", command=lambda: self.find_in_text(find_entry.get()))
        find_button.grid(row=0, column=2)

    def find_in_text(self, text_to_find):
        text_widget = self.get_current_tab().text_widget
        start_index = "1.0"
        while True:
            start_index = text_widget.search(text_to_find, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(text_to_find)}c"
            text_widget.tag_add("found", start_index, end_index)
            start_index = end_index
        text_widget.tag_config("found", background="white")

    def get_current_tab(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        return self.tabs[current_tab_index]

    def play_sound(self):
        winsound.PlaySound('tip_sound.wav', winsound.SND_FILENAME)

    def show_random_tip(self):
        tips = [
            "To open an existing text file, click on 'File' in the menu bar and select 'Open.' "
            "Then, choose the file from your system.",
            "To create a new tab, click on 'File' in the menu bar and select 'New Tab.'",
            "To save the current tab's content, click on 'File' and select 'Save' or 'Save As' to specify a new file name.",
            "To find specific text within the current tab, click on 'Edit' in the menu bar and select 'Find.' "
            "Enter the text you want to find in the dialog box and click 'Find.'"
        ]
        messagebox.showinfo("Tip", choice(tips))
        self.play_sound()

    def add_color_button(self, color_name, color_code):
        button = CTkButton(self.switch_frame, text=f"Switch to {color_name}", command=lambda: self.switch_background_color(color_code))
        button.pack(side="left", padx=5, pady=5)

    def switch_background_color(self, color_code):
        self.play_sound()

        for tab in self.tabs:
            tab.text_widget.config(bg=color_code)

        if color_code == "#333333":
            self.set_text_color("white")
        else:
            self.set_text_color("black")

    def set_text_color(self, color):
        for tab in self.tabs:
            tab.text_widget.config(fg=color)

window = Notepad()
window.title('Notepad')
window.geometry('800x500')
window.mainloop()