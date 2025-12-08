# Vasu Test Case Builder and Runner

A modern GUI application for building, managing, and executing automated test cases with support for file operations, log validation, and database checks.

## Features

- **Visual Test Case Builder**: Create test cases with multiple steps using an intuitive GUI
- **Three Step Types**:
  - **Copy File**: Copy files from source to destination
  - **Check Log File**: Search and validate log entries with timestamp filtering
  - **Check Database Entry**: Query SQL Server databases and validate records
- **Modern UI**: Clean, responsive interface with optimized spacing and auto-hide scrollbar
- **Test Management**: 
  - Create, rename, delete, and organize multiple test cases
  - Copy/paste steps between test cases
  - Export/import test cases as JSON
  - Rename individual steps for better organization
- **Execution & Reporting**:
  - Run individual test cases or all cases sequentially
  - Real-time output console with toggle show/hide
  - Generate HTML and text reports in `TestReports/` folder
  - Combined test summary report
- **Advanced Features**:
  - Step delays for timing control
  - Log file timestamp parsing with multiple format support
  - Database queries with multiple column conditions
  - Search and filter steps within test cases

## Requirements

- Python 3.7+
- Windows OS (PowerShell)
- SQL Server (for database check steps)

## Installation

### 1. Clone or Download the Repository

```powershell
cd C:\Users\YourUsername\Downloads
# Extract or clone the repository
```

### 2. Create Virtual Environment

```powershell
cd test_case_manager_real
python -m venv .venv
```

### 3. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If you encounter execution policy errors, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

Required packages:
- `sqlalchemy~=2.0.41`
- `psycopg2-binary`
- `python-dotenv~=1.1.0`
- `ttkbootstrap~=1.13.11`
- `pyodbc~=5.1.0`

### 5. Configure Database (Optional)

If using database check steps, create `autotestgui/db_config.json`:

```json
{
  "server": "your-server-name",
  "database": "your-database-name",
  "username": "your-username",
  "password": "your-password"
}
```

## Running the Application

### From Command Line

```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Run the application
python autotestgui\version8.py
```

### Using VS Code

1. Open the project folder in VS Code
2. Select Python interpreter: `.venv\Scripts\python.exe`
3. Run `autotestgui/version8.py`

## Usage Guide

### Creating a Test Case

1. Click **➕ New Case** to create a new test case
2. Click **➕ Add Step** to add test steps
3. Select step type from dropdown:
   - **Copy File**: Choose source and destination files
   - **Check Log File**: Specify log path, type, search text, and time range
   - **Check Database Entry**: Configure table, columns, operators, and values
4. Configure step delays if needed
5. Click **▶ Run** to execute the test case

### Managing Test Cases

- **Rename**: Select test case from dropdown, click **✏️ Rename**
- **Delete**: Click **🗑️ Delete** to remove current test case
- **Export All**: Save all test cases to JSON file
- **Import All**: Load test cases from JSON file
- **Run All Cases**: Execute all test cases sequentially

### Working with Steps

- **Copy Step**: Select a step (click on it), then click **📋 Copy**
- **Paste Step**: Click **📋 Paste** to paste copied steps
- **Delete Step**: Select step, click **🗑 Delete**
- **Rename Step**: Select step, click **✏ Rename Step**
- **Search Steps**: Use search bar to filter steps by type
- **Toggle Output**: Click **📊 Show Output** to view execution logs

### Reports

After execution, reports are saved in `TestReports/`:
- `log_TestCaseName.txt` - Detailed execution log
- `report_TestCaseName.html` - HTML report for individual test case
- `Combined_Test_Summary.html` - Summary of all test runs

## Project Structure

```
test_case_manager_real/
├── autotestgui/
│   ├── version8.py          # Main application
│   ├── test_step.py         # Test step widget
│   ├── db_config.json       # Database configuration (optional)
│   └── TestReports/         # Generated reports
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .venv/                  # Virtual environment
```

## Troubleshooting

### Import Error: pyodbc

If you see "pyodbc is not installed":
```powershell
pip install pyodbc
```

### Database Connection Issues

- Verify SQL Server is running
- Check `db_config.json` credentials
- Ensure SQL Server allows remote connections

### Log File Not Found

- Use absolute paths for log files
- Verify file permissions
- Check if file exists before running test

## License

This project is for internal use.