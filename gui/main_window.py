
import tkinter as tk
from tkinter import ttk
from gui.test_case_form import TestCaseForm
from gui.log_viewer import LogViewer
from gui.step_executor import StepExecutor

def run_app():
    root = tk.Tk()
    root.title("Test Case Manager")
    root.geometry("800x600")

    tab_control = ttk.Notebook(root)

    form_tab = ttk.Frame(tab_control)
    tab_control.add(form_tab, text="Test Case Form")
    TestCaseForm(form_tab)

    log_tab = ttk.Frame(tab_control)
    tab_control.add(log_tab, text="Log Viewer")
    LogViewer(log_tab)

    exec_tab = ttk.Frame(tab_control)
    tab_control.add(exec_tab, text="Step Executor")
    StepExecutor(exec_tab)

    tab_control.pack(expand=1, fill="both")
    root.mainloop()

if __name__ == "__main__":
    run_app()
