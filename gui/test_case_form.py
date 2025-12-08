
import tkinter as tk
from tkinter import messagebox
from db.models import TestCase
from db.database import Session

class TestCaseForm:
    def __init__(self, master):
        self.master = master
        self.session = Session()
        self.build()

    def build(self):
        tk.Label(self.master, text="Test Case Name").pack()
        self.name_entry = tk.Entry(self.master)
        self.name_entry.pack()

        tk.Label(self.master, text="Description").pack()
        self.desc_entry = tk.Entry(self.master)
        self.desc_entry.pack()

        tk.Button(self.master, text="Add", command=self.add_case).pack(pady=5)

    def add_case(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        if not name:
            messagebox.showerror("Error", "Name required")
            return
        new_case = TestCase(name=name, description=desc)
        self.session.add(new_case)
        self.session.commit()
        messagebox.showinfo("Success", "Test case added")
