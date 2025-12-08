
import tkinter as tk
from tkinter import ttk
from db.models import Session, Log

class LogViewer:
    def __init__(self, master):
        self.master = master
        self.session = Session()
        self.build()

    def build(self):
        self.tree = ttk.Treeview(self.master, columns=("type", "msg", "time"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=1, fill="both")
        self.load_logs()

    def load_logs(self):
        logs = self.session.query(Log).order_by(Log.created_at.desc()).limit(50).all()
        for log in logs:
            self.tree.insert("", "end", values=(log.log_type, log.message, log.created_at))
