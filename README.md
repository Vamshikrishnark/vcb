# Vasu Test Case Builder and Runner

A modern, feature-rich GUI application for building, managing, and executing automated test cases with advanced conditional execution, parallel processing, and comprehensive reporting capabilities.

## Features

### Core Functionality
- **Visual Test Case Builder**: Create test cases with multiple steps using an intuitive GUI
- **Three Step Types**:
  - **Copy File**: Copy files from source to destination with validation
  - **Check Log File**: Search and validate log entries with timestamp filtering
  - **Check Database Entry**: Query SQL Server databases and validate records
- **Modern UI**: Clean, responsive interface with optimized spacing and category-based organization

### Advanced Test Management
- **Conditional Execution**: 
  - Run steps based on previous step results
  - Options: Always, If Previous Passed, If Previous Failed, Skip
  - Smart step skipping with detailed reporting
- **Step Categories**: 
  - Organize steps by type: General, Setup, Validation, Cleanup, Critical
  - Filter and view steps by category
  - Visual category indicators in step labels
- **Flexible Step Selection**:
  - Checkbox-based multi-step selection
  - Copy multiple selected steps at once
  - Select All / Unselect All functionality
  - Rename steps with custom names

### Execution Options
- **Sequential Execution**: Run all test cases one after another
- **Parallel Execution**: Run multiple test cases simultaneously for faster execution
- **Real-time Monitoring**: Live output console with toggle show/hide
- **Step-by-Step Tracking**: Monitor execution progress with detailed status updates

### Enhanced Reporting
- **Performance Metrics**: 
  - Execution time tracked for each step
  - Total execution time per test case
  - Execution summary with statistics
- **Multiple Report Formats**:
  - Text logs with timestamps
  - HTML reports with color-coded results
  - Excel export with detailed metrics
  - Combined summary reports
- **Detailed Statistics**:
  - Total steps, executed, and skipped counts
  - Pass/fail rates
  - Category-wise breakdown
  - Custom step names in all reports

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
- `openpyxl~=3.1.2` (for Excel export)

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
3. Configure each step:
   - **Category**: Choose from General, Setup, Validation, Cleanup, Critical
   - **Run Condition**: Set to Always, If Previous Passed, If Previous Failed, or Skip
   - **Step Type**: Select Copy File, Check Log File, or Check Database Entry
   - **Step Details**: Configure specific parameters for the step type
   - **Step Delay**: Add wait time before executing the step (optional)
4. Click **▶ Run** to execute the test case

### Managing Test Cases

- **Rename**: Select test case from dropdown, click **✏️ Rename**
- **Delete**: Click **🗑️ Delete** to remove current test case
- **Export All**: Save all test cases to JSON file
- **Import All**: Load test cases from JSON file
- **Run All Sequential**: Execute all test cases one after another
- **Run All Parallel**: Execute all test cases simultaneously (faster)
- **Export to Excel**: Generate detailed Excel reports with metrics

### Working with Steps

- **Select Steps**: Check the "Select" checkbox on steps you want to copy
- **Copy Checked**: Click **📋 Copy Checked** to copy selected steps
- **Paste Steps**: Click **📋 Paste** to paste copied steps
- **Delete Step**: Select a step (click on it), then click **🗑 Delete**
- **Rename Step**: Select step, click **✏ Rename Step** for custom names
- **Select All**: Click **☑ Select All** to check all step checkboxes
- **Unselect All**: Click **☐ Unselect All** to uncheck all checkboxes
- **Filter by Category**: Use category filter buttons (All, Setup, Validation, Cleanup, Critical)
- **Search Steps**: Use search bar to filter steps by type
- **Toggle Output**: Click **📊 Show Output** to view execution logs

### Understanding Conditional Execution

Steps can be configured to run conditionally:
- **Always**: Step always executes (default)
- **If Previous Passed**: Only runs if the previous step succeeded
- **If Previous Failed**: Only runs if the previous step failed
- **Skip**: Step is skipped entirely

This allows you to create dynamic test flows that adapt based on results.

### Reports

After execution, reports are automatically generated in `TestReports/`:
- `log_TestCaseName.txt` - Detailed execution log with timestamps
- `report_TestCaseName.html` - Color-coded HTML report with execution summary
- `Combined_Test_Summary.html` - Summary of all test runs
- `test_summary.txt` - Sequential execution summary
- `test_summary_parallel.txt` - Parallel execution summary

**Excel Reports** (via Export button):
- Summary sheet with all test cases
- Individual sheets per test case
- Detailed step information with categories, conditions, and execution times
- Color-coded pass/fail status
- Performance metrics and statistics

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