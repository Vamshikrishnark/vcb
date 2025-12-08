import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil, os, datetime, json, time, threading
import pyodbc  # For MSSQL only


class TestStep:
    def __init__(self, parent, step_num):
        self.step_name = f"Step {step_num}"
        self.frame = ttk.LabelFrame(parent, text=self.step_name)
        self.step_type = tk.StringVar()
        self.details = {}
        self.column_entries = []

        self.type_dropdown = ttk.Combobox(self.frame, values=[
            "Copy File", "Check Log File", "Check Database Entry"
        ], state="readonly", textvariable=self.step_type, style="Step.TCombobox")
        self.type_dropdown.grid(row=0, column=0, padx=5, pady=5)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.show_fields)

        self.fields_frame = ttk.Frame(self.frame, style="StepInner.TFrame")
        self.fields_frame.grid(row=1, column=0, padx=5, pady=5)

    def show_fields(self, event=None):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        self.details.clear()
        self.column_entries.clear()

        step_type = self.step_type.get()

        ttk.Label(self.fields_frame, text="Step Delay (secs):", style="Step.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.details["step_delay"] = tk.Entry(self.fields_frame, width=10)
        self.details["step_delay"].insert(0, "0")
        self.details["step_delay"].grid(row=0, column=1, sticky='w', padx=5, pady=2)

        row = 1
        if step_type == "Copy File":
            self.details["from_files"] = []
            ttk.Label(self.fields_frame, text="From Files:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            from_files_entry = tk.Entry(self.fields_frame, width=50)
            from_files_entry.grid(row=row, column=1, sticky='w', padx=5, pady=2)
            self.details["from"] = from_files_entry
            ttk.Button(self.fields_frame, text="Browse Files", command=self.browse_files, style="Ghost.TButton").grid(row=row, column=2)
            row += 1

            ttk.Label(self.fields_frame, text="To Path:", style="Step.TLabel").grid(row=row, column=0)
            self.details["to"] = tk.Entry(self.fields_frame, width=50)
            self.details["to"].grid(row=row, column=1, sticky='w', padx=5, pady=2)

        elif step_type == "Check Log File":
            ttk.Label(self.fields_frame, text="Log Type:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            self.details["log_type"] = ttk.Combobox(
                self.fields_frame, values=["", "L", "M", "H", "DEBUG", "ERROR", "INFO"], state="readonly", style="Step.TCombobox")
            self.details["log_type"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            row += 1

            ttk.Label(self.fields_frame, text="Search String:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            self.details["search"] = tk.Entry(self.fields_frame, width=100)
            self.details["search"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            row += 1

            ttk.Label(self.fields_frame, text="Duration (mins):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            self.details["duration"] = tk.Entry(self.fields_frame)
            self.details["duration"].insert(0, "60")
            self.details["duration"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            row += 1

            ttk.Label(self.fields_frame, text="Wait Before Search (secs):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            self.details["delay"] = tk.Entry(self.fields_frame)
            self.details["delay"].insert(0, "0")
            self.details["delay"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            row += 1

            ttk.Label(self.fields_frame, text="Log File Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            self.details["log_file_path"] = tk.Entry(self.fields_frame, width=50)
            self.details["log_file_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)

        elif step_type == "Check Database Entry":
            labels = [("Table Name", "table")]
            for label, key in labels:
                ttk.Label(self.fields_frame, text=label + ":", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
                self.details[key] = tk.Entry(self.fields_frame, width=40)
                self.details[key].grid(row=row, column=1, sticky='w', padx=5, pady=2)
                row += 1

            self.columns_frame = ttk.LabelFrame(self.fields_frame, text="Columns to Check", style="Step.TLabelframe")
            self.columns_frame.grid(row=row, column=0, columnspan=2, pady=5)
            self.add_column_entry()

            row += 1
            add_col_btn = ttk.Button(self.fields_frame, text="Add Column", command=self.add_column_entry, style="Ghost.TButton")
            add_col_btn.grid(row=row, column=0, columnspan=2)

    def browse_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.details["from_files"] = files
            self.details["from"].delete(0, tk.END)
            self.details["from"].insert(0, ", ".join(files))

    def add_column_entry(self):
        row = len(self.column_entries)
        col_name = tk.Entry(self.columns_frame, width=15)
        operator = ttk.Combobox(self.columns_frame, values=["=", "LIKE", ">=", "<=", "<", ">", "!="], width=5, style="Step.TCombobox")
        operator.set("=")
        col_value = tk.Entry(self.columns_frame, width=15)

        col_name.grid(row=row, column=0, padx=2, pady=2)
        operator.grid(row=row, column=1, padx=2, pady=2)
        col_value.grid(row=row, column=2, padx=2, pady=2)

        self.column_entries.append((col_name, operator, col_value))

    def get_step_data(self):
        step = {"name": self.step_name, "type": self.step_type.get(), "details": {}}
        for key, widget in self.details.items():
            step["details"][key] = widget.get() if hasattr(widget, "get") else widget

        if self.step_type.get() == "Copy File":
            step["details"]["from_files"] = self.details.get("from_files", [])

        if self.step_type.get() == "Check Database Entry":
            step["details"]["columns"] = []
            for name_entry, op_entry, val_entry in self.column_entries:
                if name_entry.get():
                    step["details"]["columns"].append({
                        "column": name_entry.get(),
                        "operator": op_entry.get(),
                        "value": val_entry.get()
                    })
        return step

def load_db_config():
    try:
        with open("db_config.json") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("DB Config Error", f"Failed to load DB config: {e}")
    return None