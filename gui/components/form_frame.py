import tkinter as tk

class FormFrame(tk.Frame):
    def __init__(self, master, title, fields, on_submit, submit_text="Guardar"):
        super().__init__(master, bg="#f5f5f5", padx=20, pady=20)
        tk.Label(self, text=title, font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=(0, 15))

        self.entries = {}
        for field in fields:
            frame = tk.Frame(self, bg="#f5f5f5")
            frame.pack(fill="x", pady=5)
            tk.Label(frame, text=field, width=15, anchor="w", bg="#f5f5f5", font=("Arial", 11)).pack(side="left")
            entry = tk.Entry(frame, font=("Arial", 11))
            entry.pack(side="left", fill="x", expand=True)
            self.entries[field] = entry

        tk.Button(self, text=submit_text, command=self._submit, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=15)
        self.on_submit = on_submit

    def _submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        self.on_submit(data)