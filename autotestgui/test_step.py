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
        self.is_checked = tk.BooleanVar(value=False)
        
        # Conditional execution settings
        self.run_condition = tk.StringVar(value="Always")
        self.category = tk.StringVar(value="General")
        self.target_step = tk.StringVar(value="")
        self.execution_time = 0
        self.last_result = None
        
        # Top row with checkbox and controls
        top_frame = ttk.Frame(self.frame, style="StepInner.TFrame")
        top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=5, pady=(5, 10))
        
        # Add checkbox
        self.checkbox = ttk.Checkbutton(top_frame, text="Select", variable=self.is_checked, style="Step.TCheckbutton")
        self.checkbox.pack(side='left', padx=(5, 15))
        
        # Add category dropdown with label
        ttk.Label(top_frame, text="Category:", style="Step.TLabel").pack(side='left', padx=(0, 5))
        self.category_dropdown = ttk.Combobox(top_frame, textvariable=self.category, 
                                               values=["General", "Setup", "Validation", "Cleanup", "Critical"],
                                               width=12, state="readonly", style="Step.TCombobox")
        self.category_dropdown.pack(side='left', padx=(0, 20))
        
        # Add condition dropdown with label
        ttk.Label(top_frame, text="Run Condition:", style="Step.TLabel").pack(side='left', padx=(0, 5))
        from condition_handler import ConditionHandler
        self.condition_dropdown = ttk.Combobox(top_frame, textvariable=self.run_condition,
                                                values=ConditionHandler.CONDITIONS,
                                                width=25, state="readonly", style="Step.TCombobox")
        self.condition_dropdown.pack(side='left', padx=(0, 5))
        self.condition_dropdown.bind("<<ComboboxSelected>>", self.on_condition_change)
        
        # Add target step entry (initially hidden)
        ttk.Label(top_frame, text="Target Step #:", style="Step.TLabel").pack(side='left', padx=(0, 5))
        self.target_step_entry = ttk.Entry(top_frame, textvariable=self.target_step, width=5)
        self.target_step_entry.pack(side='left', padx=(0, 5))
        self.target_step_entry.pack_forget()  # Hide initially
        
        # Second row with step type dropdown and label
        type_frame = ttk.Frame(self.frame, style="StepInner.TFrame")
        type_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=5, pady=(0, 5))
        
        ttk.Label(type_frame, text="Step Type:", style="Step.TLabel").pack(side='left', padx=(5, 5))
        self.type_dropdown = ttk.Combobox(type_frame, values=[
            "Copy File", "Move File", "Delete File/Folder", "Rename File", "Create Directory",
            "Check File Exists", "Compare Files", "Extract Archive", "Wait for File",
            "Run Command", "Start Process", "Stop Process", "Check Process Running",
            "Check Disk Space", "Check Memory",
            "Check Log File", "Check Database Entry"
        ], state="readonly", textvariable=self.step_type, style="Step.TCombobox", width=25)
        self.type_dropdown.pack(side='left', padx=(0, 5))
        self.type_dropdown.bind("<<ComboboxSelected>>", self.show_fields)

        self.fields_frame = ttk.Frame(self.frame, style="StepInner.TFrame")
        self.fields_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

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
        
        # Import and use the modular UI builders
        else:
            try:
                import sys
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from step_types.step_ui_builder import StepTypeUI
                
                ui_map = {
                    "Move File": StepTypeUI.build_move_file_ui,
                    "Delete File/Folder": StepTypeUI.build_delete_path_ui,
                    "Rename File": StepTypeUI.build_rename_path_ui,
                    "Create Directory": StepTypeUI.build_create_directory_ui,
                    "Check File Exists": StepTypeUI.build_check_path_exists_ui,
                    "Compare Files": StepTypeUI.build_compare_files_ui,
                    "Extract Archive": StepTypeUI.build_extract_archive_ui,
                    "Wait for File": StepTypeUI.build_wait_for_file_ui,
                    "Run Command": StepTypeUI.build_run_command_ui,
                    "Start Process": StepTypeUI.build_start_process_ui,
                    "Stop Process": StepTypeUI.build_stop_process_ui,
                    "Check Process Running": StepTypeUI.build_check_process_ui,
                    "Check Disk Space": StepTypeUI.build_check_disk_space_ui,
                    "Check Memory": StepTypeUI.build_check_memory_ui,
                }
                
                if step_type in ui_map:
                    ui_map[step_type](self.fields_frame, self.details, row)
            except Exception as e:
                ttk.Label(self.fields_frame, text=f"Error loading UI: {str(e)}", style="Step.TLabel").grid(row=row, column=0, columnspan=3)

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

    def on_condition_change(self, event=None):
        """Show/hide target step entry based on condition"""
        condition = self.run_condition.get()
        if condition in ["If Specific Step Passed", "If Specific Step Failed"]:
            self.target_step_entry.pack(side='left', padx=(0, 5))
        else:
            self.target_step_entry.pack_forget()
    
    def get_step_data(self):
        step = {
            "name": self.step_name, 
            "type": self.step_type.get(), 
            "details": {},
            "run_condition": self.run_condition.get(),
            "category": self.category.get(),
            "target_step": self.target_step.get()
        }
        for key, widget in self.details.items():
            # Handle different widget types properly
            if hasattr(widget, "get"):
                # Text widgets need get("1.0", "end-1c"), Entry widgets just need get()
                if isinstance(widget, tk.Text):
                    step["details"][key] = widget.get("1.0", "end-1c")
                else:
                    step["details"][key] = widget.get()
            else:
                step["details"][key] = widget

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