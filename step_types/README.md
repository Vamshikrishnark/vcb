# Step Types Module

Modular test automation step types for the Vasu Test Case Builder.

## Structure

```
step_types/
├── __init__.py              # Module initialization
├── file_operations.py       # File and directory operations
├── system_operations.py     # System and process operations
├── step_ui_builder.py       # UI builders for each step type
├── step_executor.py         # Execution logic for all step types
├── requirements.txt         # Additional dependencies
└── README.md               # This file
```

## Installation

Install additional dependencies:
```bash
pip install -r step_types/requirements.txt
```

## Available Step Types

### File & Directory Operations

#### 1. **Move File**
Move files or directories from source to destination.
- **Fields**: From Path, To Path
- **Use Case**: Reorganize files, move completed files to archive

#### 2. **Delete File/Folder**
Delete files or directories (with recursive option).
- **Fields**: Path to Delete, Recursive checkbox
- **Use Case**: Clean up temporary files, remove test data

#### 3. **Rename File**
Rename files or directories.
- **Fields**: Old Path, New Path
- **Use Case**: Version control, standardize naming

#### 4. **Create Directory**
Create new directories (with parent creation option).
- **Fields**: Directory Path, Create Parents checkbox
- **Use Case**: Set up test environment structure

#### 5. **Check File Exists**
Verify if a file or directory exists (or doesn't exist).
- **Fields**: Path to Check, Should Exist (Yes/No)
- **Use Case**: Validate file creation, ensure cleanup

#### 6. **Compare Files**
Compare two files by checksum, content, or size.
- **Fields**: First File, Second File, Compare Method (checksum/content/size)
- **Use Case**: Verify file copies, check data integrity

#### 7. **Extract Archive**
Extract compressed archives (ZIP, TAR, TAR.GZ).
- **Fields**: Archive Path, Extract To, Archive Type
- **Use Case**: Unpack deployment files, extract test data

#### 8. **Wait for File**
Wait for a file to appear or disappear (with timeout).
- **Fields**: File Path, Wait For (Appear/Disappear), Timeout (seconds)
- **Use Case**: Wait for file generation, monitor file deletion

### System & Process Operations

#### 9. **Run Command**
Execute shell or PowerShell commands.
- **Fields**: Command (multi-line), Working Directory, Timeout
- **Use Case**: Run build scripts, execute system commands

#### 10. **Start Process**
Launch applications or processes.
- **Fields**: Executable Path, Arguments, Wait for Completion checkbox
- **Use Case**: Start services, launch applications

#### 11. **Stop Process**
Stop or kill running processes by name or PID.
- **Fields**: Process Name, Process ID (PID), Force Kill checkbox
- **Use Case**: Stop services, clean up processes

#### 12. **Check Process Running**
Verify if a process is running (or not running).
- **Fields**: Process Name, Should Be Running (Yes/No)
- **Use Case**: Validate service startup, ensure process termination

#### 13. **Check Disk Space**
Check available disk space on a drive or path.
- **Fields**: Path/Drive, Required Space (GB)
- **Use Case**: Pre-deployment validation, space monitoring

#### 14. **Check Memory**
Check available system memory.
- **Fields**: Required Memory (MB)
- **Use Case**: System resource validation, performance testing

## Usage Example

### In Python Code:
```python
from step_types.file_operations import FileOperations
from step_types.system_operations import SystemOperations

# Move a file
success, message = FileOperations.move_file(
    "C:/source/file.txt",
    "C:/destination/file.txt"
)

# Run a command
success, message, output = SystemOperations.run_command(
    "dir",
    timeout=30
)
```

### In GUI:
1. Select step type from dropdown
2. Fill in required fields
3. Configure run conditions and category
4. Run the test case

## Adding New Step Types

To add a new step type:

1. **Add operation logic** in appropriate module (`file_operations.py` or `system_operations.py`)
2. **Create UI builder** in `step_ui_builder.py`
3. **Add executor logic** in `step_executor.py`
4. **Update step type list** in `test_step.py`

Example:
```python
# In file_operations.py
@staticmethod
def new_operation(param1, param2):
    try:
        # Implementation
        return True, "Success message"
    except Exception as e:
        return False, f"Error: {str(e)}"

# In step_ui_builder.py
@staticmethod
def build_new_operation_ui(fields_frame, details, row):
    ttk.Label(fields_frame, text="Param1:").grid(row=row, column=0)
    details["param1"] = tk.Entry(fields_frame, width=50)
    details["param1"].grid(row=row, column=1)
    return row + 1

# In step_executor.py
elif step_type == "New Operation":
    success, msg = FileOperations.new_operation(
        details.get("param1", ""),
        details.get("param2", "")
    )
    return success, msg, msg
```

## Error Handling

All operations return tuple format:
- `(success: bool, message: str)` - For most operations
- `(success: bool, message: str, output: str)` - For commands with output

## Dependencies

- **psutil**: Process and system information
- **Standard library**: os, shutil, subprocess, hashlib, zipfile, tarfile, time, pathlib

## License

Part of the Vasu Test Case Builder and Runner project.
