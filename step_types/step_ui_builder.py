"""
Step Type UI Builder
Creates UI fields for different step types
"""
import tkinter as tk
from tkinter import ttk


class StepTypeUI:
    """Builds UI components for each step type"""
    
    @staticmethod
    def build_move_file_ui(fields_frame, details, row):
        """Build UI for Move File step"""
        ttk.Label(fields_frame, text="From Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["from_path"] = tk.Entry(fields_frame, width=50)
        details["from_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="To Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["to_path"] = tk.Entry(fields_frame, width=50)
        details["to_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_delete_path_ui(fields_frame, details, row):
        """Build UI for Delete File/Folder step"""
        ttk.Label(fields_frame, text="Path to Delete:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["path"] = tk.Entry(fields_frame, width=50)
        details["path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        details["recursive_var"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(fields_frame, text="Recursive (delete non-empty directories)", 
                       variable=details["recursive_var"]).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_rename_path_ui(fields_frame, details, row):
        """Build UI for Rename File step"""
        ttk.Label(fields_frame, text="Old Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["old_path"] = tk.Entry(fields_frame, width=50)
        details["old_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="New Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["new_path"] = tk.Entry(fields_frame, width=50)
        details["new_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_create_directory_ui(fields_frame, details, row):
        """Build UI for Create Directory step"""
        ttk.Label(fields_frame, text="Directory Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["path"] = tk.Entry(fields_frame, width=50)
        details["path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        details["create_parents_var"] = tk.BooleanVar(value=True)
        ttk.Checkbutton(fields_frame, text="Create parent directories if needed", 
                       variable=details["create_parents_var"]).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_check_path_exists_ui(fields_frame, details, row):
        """Build UI for Check Path Exists step"""
        ttk.Label(fields_frame, text="Path to Check:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["path"] = tk.Entry(fields_frame, width=50)
        details["path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Should Exist:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["should_exist"] = ttk.Combobox(fields_frame, values=["Yes", "No"], state="readonly", width=10, style="Step.TCombobox")
        details["should_exist"].set("Yes")
        details["should_exist"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_compare_files_ui(fields_frame, details, row):
        """Build UI for Compare Files step"""
        ttk.Label(fields_frame, text="First File:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["file1"] = tk.Entry(fields_frame, width=50)
        details["file1"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Second File:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["file2"] = tk.Entry(fields_frame, width=50)
        details["file2"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Compare Method:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["method"] = ttk.Combobox(fields_frame, values=["checksum", "content", "size"], 
                                        state="readonly", width=15, style="Step.TCombobox")
        details["method"].set("checksum")
        details["method"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_extract_archive_ui(fields_frame, details, row):
        """Build UI for Extract Archive step"""
        ttk.Label(fields_frame, text="Archive Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["archive_path"] = tk.Entry(fields_frame, width=50)
        details["archive_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Extract To:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["extract_to"] = tk.Entry(fields_frame, width=50)
        details["extract_to"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Archive Type:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["archive_type"] = ttk.Combobox(fields_frame, values=["auto", "zip", "tar", "tar.gz"], 
                                              state="readonly", width=15, style="Step.TCombobox")
        details["archive_type"].set("auto")
        details["archive_type"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_wait_for_file_ui(fields_frame, details, row):
        """Build UI for Wait for File step"""
        ttk.Label(fields_frame, text="File Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["file_path"] = tk.Entry(fields_frame, width=50)
        details["file_path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Wait For:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["should_exist"] = ttk.Combobox(fields_frame, values=["File to Appear", "File to Disappear"], 
                                              state="readonly", width=20, style="Step.TCombobox")
        details["should_exist"].set("File to Appear")
        details["should_exist"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Timeout (seconds):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["timeout"] = tk.Entry(fields_frame, width=10)
        details["timeout"].insert(0, "60")
        details["timeout"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_run_command_ui(fields_frame, details, row):
        """Build UI for Run Command step"""
        ttk.Label(fields_frame, text="Command:", style="Step.TLabel").grid(row=row, column=0, sticky='nw', padx=5, pady=2)
        details["command"] = tk.Text(fields_frame, width=50, height=4)
        details["command"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Working Directory:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["working_dir"] = tk.Entry(fields_frame, width=50)
        details["working_dir"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Timeout (seconds):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["timeout"] = tk.Entry(fields_frame, width=10)
        details["timeout"].insert(0, "30")
        details["timeout"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_start_process_ui(fields_frame, details, row):
        """Build UI for Start Process step"""
        ttk.Label(fields_frame, text="Executable Path:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["executable"] = tk.Entry(fields_frame, width=50)
        details["executable"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Arguments:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["arguments"] = tk.Entry(fields_frame, width=50)
        details["arguments"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        details["wait_var"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(fields_frame, text="Wait for process to complete", 
                       variable=details["wait_var"]).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_stop_process_ui(fields_frame, details, row):
        """Build UI for Stop Process step"""
        ttk.Label(fields_frame, text="Process Name:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["process_name"] = tk.Entry(fields_frame, width=30)
        details["process_name"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        ttk.Label(fields_frame, text="(e.g., notepad.exe)", style="Step.TLabel").grid(row=row, column=2, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="OR Process ID (PID):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["pid"] = tk.Entry(fields_frame, width=10)
        details["pid"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        details["force_var"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(fields_frame, text="Force kill (terminate immediately)", 
                       variable=details["force_var"]).grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_check_process_ui(fields_frame, details, row):
        """Build UI for Check Process Running step"""
        ttk.Label(fields_frame, text="Process Name:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["process_name"] = tk.Entry(fields_frame, width=30)
        details["process_name"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Should Be Running:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["should_run"] = ttk.Combobox(fields_frame, values=["Yes", "No"], state="readonly", width=10, style="Step.TCombobox")
        details["should_run"].set("Yes")
        details["should_run"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_check_disk_space_ui(fields_frame, details, row):
        """Build UI for Check Disk Space step"""
        ttk.Label(fields_frame, text="Path/Drive:", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["path"] = tk.Entry(fields_frame, width=30)
        details["path"].insert(0, "C:/")
        details["path"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        row += 1
        
        ttk.Label(fields_frame, text="Required Space (GB):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["required_gb"] = tk.Entry(fields_frame, width=10)
        details["required_gb"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        ttk.Label(fields_frame, text="(leave empty to just report)", style="Step.TLabel").grid(row=row, column=2, sticky='w', padx=5, pady=2)
        return row + 1
    
    @staticmethod
    def build_check_memory_ui(fields_frame, details, row):
        """Build UI for Check Memory step"""
        ttk.Label(fields_frame, text="Required Memory (MB):", style="Step.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        details["required_mb"] = tk.Entry(fields_frame, width=10)
        details["required_mb"].grid(row=row, column=1, sticky='w', padx=5, pady=2)
        ttk.Label(fields_frame, text="(leave empty to just report)", style="Step.TLabel").grid(row=row, column=2, sticky='w', padx=5, pady=2)
        return row + 1
