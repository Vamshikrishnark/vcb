
import tkinter as tk
from tkinter import messagebox
from db.models import Session, TestStep

class StepExecutor:
    def __init__(self, master):
        self.master = master
        self.session = Session()
        self.build()

    def build(self):
        tk.Label(self.master, text="Execute All Steps").pack(pady=10)
        tk.Button(self.master, text="Run", command=self.run_steps).pack()

    def run_steps(self):
        steps = self.session.query(TestStep).all()
        for step in steps:
            if not step.action:
                continue
            print(f"Executing Step: {step.action}")
        messagebox.showinfo("Done", "Steps executed.")
