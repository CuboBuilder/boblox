import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import json
import sys

class MungusLauncherV3:
    def __init__(self, root):
        self.root = root
        self.root.title("RFD Launcher: Mungus Edition")
        self.root.geometry("600x550")
        self.config_file = "mungus_config.json"

        # Дефолтные настройки
        self.settings = {
            "nickname": "Player",
            "host": "127.0.0.1",
            "port": "2005",
            "rfd_path": "RFD.exe",
            "mode": "exe" # или "source"
        }
        self.load_settings()

        # Tkinter переменные
        self.nick_var = tk.StringVar(value=self.settings["nickname"])
        self.host_var = tk.StringVar(value=self.settings["host"])
        self.port_var = tk.StringVar(value=self.settings["port"])
        self.rfd_path_var = tk.StringVar(value=self.settings["rfd_path"])
        self.mode_var = tk.StringVar(value=self.settings["mode"])
        self.config_path = tk.StringVar()

        self.setup_ui()

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.settings.update(json.load(f))
            except: pass

    def save_settings(self):
        self.settings.update({
            "nickname": self.nick_var.get(),
            "host": self.host_var.get(),
            "port": self.port_var.get(),
            "rfd_path": self.rfd_path_var.get(),
            "mode": self.mode_var.get()
        })
        with open(self.config_file, "w") as f:
            json.dump(self.settings, f)

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_player = ttk.Frame(self.notebook); self.notebook.add(self.tab_player, text="  PLAYER  ")
        self.tab_server = ttk.Frame(self.notebook); self.notebook.add(self.tab_server, text="  SERVER  ")
        self.tab_studio = ttk.Frame(self.notebook); self.notebook.add(self.tab_studio, text="  STUDIO  ")
        self.tab_settings = ttk.Frame(self.notebook); self.notebook.add(self.tab_settings, text="  SETTINGS  ")

        self.setup_player_tab()
        self.setup_server_tab()
        self.setup_studio_tab()
        self.setup_settings_tab()

    def setup_player_tab(self):
        f = ttk.LabelFrame(self.tab_player, text=" Join ")
        f.pack(fill="both", expand=True, padx=20, pady=20)
        ttk.Label(f, text="Nick:").grid(row=0, column=0, pady=10, padx=5)
        ttk.Entry(f, textvariable=self.nick_var).grid(row=0, column=1)
        ttk.Label(f, text="Host:").grid(row=1, column=0, pady=10, padx=5)
        ttk.Entry(f, textvariable=self.host_var).grid(row=1, column=1)
        ttk.Label(f, text="Port:").grid(row=2, column=0, pady=10, padx=5)
        ttk.Entry(f, textvariable=self.port_var).grid(row=2, column=1)
        tk.Button(self.tab_player, text="LAUNCH PLAYER", bg="#3498db", fg="white", command=lambda: self.launch("player")).pack(pady=10, fill="x", padx=50)

    def setup_server_tab(self):
        f = ttk.LabelFrame(self.tab_server, text=" Hosting ")
        f.pack(fill="both", expand=True, padx=20, pady=20)
        ttk.Label(f, text="Port:").grid(row=0, column=0, pady=10, padx=5)
        ttk.Entry(f, textvariable=self.port_var).grid(row=0, column=1)
        ttk.Button(f, text="Select Place/Config", command=self.browse_file).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(f, textvariable=self.config_path, wraplength=300).grid(row=2, column=0, columnspan=2)
        tk.Button(self.tab_server, text="START SERVER", bg="#2ecc71", fg="white", command=lambda: self.launch("server")).pack(pady=10, fill="x", padx=50)

    def setup_studio_tab(self):
        f = ttk.Frame(self.tab_studio)
        f.pack(pady=50)
        ttk.Button(f, text="Select .rbxl to Edit", command=self.browse_file).pack()
        tk.Button(self.tab_studio, text="OPEN STUDIO", bg="#f1c40f", command=lambda: self.launch("studio")).pack(pady=20, fill="x", padx=50)

    def setup_settings_tab(self):
        f = ttk.LabelFrame(self.tab_settings, text=" Launcher Configuration ")
        f.pack(fill="both", expand=True, padx=20, pady=20)

        # Режим запуска
        ttk.Label(f, text="Launch Mode:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(f, text="RFD.exe", variable=self.mode_var, value="exe").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(f, text="Source (_main.py)", variable=self.mode_var, value="source").grid(row=0, column=2, sticky="w")

        # Путь к EXE
        ttk.Label(f, text="Path to RFD.exe:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(f, textvariable=self.rfd_path_var, width=30).grid(row=1, column=1, columnspan=2)
        ttk.Button(f, text="...", width=3, command=self.browse_exe).grid(row=1, column=3, padx=5)

        tk.Button(self.tab_settings, text="SAVE SETTINGS", bg="#95a5a6", command=self.save_settings).pack(pady=10)
        ttk.Label(self.tab_settings, text="Baser is watching you...", font=("Arial", 8, "italic")).pack()

    def browse_file(self):
        p = filedialog.askopenfilename(); self.config_path.set(p) if p else None
    
    def browse_exe(self):
        p = filedialog.askopenfilename(filetypes=[("Executables", "*.exe")])
        if p: self.rfd_path_var.set(p)

    def launch(self, mode):
        self.save_settings()
        
        if self.mode_var.get() == "exe":
            exe_path = os.path.abspath(self.rfd_path_var.get())
            if not os.path.exists(exe_path):
                messagebox.showerror("Хуйня!", "RFD.exe не найден по этому пути!"); return
            cmd = [exe_path]
        else:
            cmd = [sys.executable, "_main.py"]

        cmd.append(mode)
        nick, host, port, path = self.nick_var.get(), self.host_var.get(), self.port_var.get(), self.config_path.get()

        if mode == "player":
            cmd.extend(["-h", host, "-p", port, "-u", nick])
        elif mode == "server":
            cmd.extend(["-p", port])
            if path: cmd.extend(["--config" if path.endswith(".toml") else "--place", path])
        elif mode == "studio":
            if path: cmd.extend(["--place", path])

        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk(); style = ttk.Style(); style.theme_use('clam')

    MungusLauncherV3(root); root.mainloop()
