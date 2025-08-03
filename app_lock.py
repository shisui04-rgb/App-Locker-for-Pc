import os
import sys
import psutil
import ctypes
import time
from getpass import getpass
import hashlib
import json
from threading import Thread
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import filedialog

#Configuration file path
CONFIG_FILE = os.path.join(os.getenv('APPDATA'), 'AppLocker', 'config.json')

class AppLocker:
    def __init__(self):
        self.locked_apps = []
        self.password_hash = None
        self.running = True
        self.load_config()

    def hash_password(self, password):
        """Create SHA-256 hash of the password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.locked_apps = config.get('locked_apps', [])
                    self.password_hash = config.get('password_hash')
        except Exception as e:
            print(f"Error loding config: {e}")

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({
                    'locked_apps': self.locked_apps,
                    'password_hash': self.password_hash
                },f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def is_admin(self):
        """Check if running as admin"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def check_processes(self):
        """Monitor and terminate locked applications"""
        while self.running:
            for proc in psutil.process_iter(['name', 'exe']):
                for app in self.locked_apps:
                    app_name = os.path.basename(app).lower()
                    if proc.info['name'].lower() == app_name or (proc.info['exe']and os.path.basename(proc.info['exe']).lower() == app_name):
                        try:
                            proc.kill()
                        except:
                            pass
            time.sleep(1)
    
    def run(self):
        """Start the application"""
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

        #Start monitoring thread
        monitor = Thread(target=self.check_processes)
        monitor.daemon = True
        monitor.start()

        #start GUI
        self.create_gui()

    def create_gui(self):
        """Create the configuration interface"""
        root = tk.Tk()
        root.title("App Locker")
        root.geometry("400x300")
        root.resizable(False, False)

        if not self.password_hash:
            password = simpledialog.askstring("setup", "Set a new password:", show='*', parent=root)
            if password:
                self.password_hash = self.hash_password(password)
                self.save_config()  
            else:
                sys.exit()

        def validate_password():
            password = simpledialog.askstring("Authentication", "Enter password:", show='*', parent=root)
            if password and self.hash_password(password) == self.password_hash:
                return True
            messagebox.showerror("Error", "Incorrect password")
            return False
    
        def add_app():
            if not validate_password():
                return
        
            app_path = filedialog.askopenfilename(
                title="Select Application to Lock",
                filetypes=[("Executable files", "*.exe")]
            )

            if app_path and app_path not in self.locked_apps:
                self.locked_apps.append(app_path)
                self.save_config()
                update_list()

        def remove_app():
            if not validate_password():
                return
        
            selected = listbox.curselection()
            if selected:
                self.locked_apps.pop(selected[0])
                self.save_config()
                update_list()

        def update_list():
            listbox.delete(0, tk.END)
            for app in self.locked_apps:
                listbox.insert(tk.END, os.path.basename(app))

         #GUI Elements
        tk.Label(root, text="Locked Applications", font=('Bookman Old Style', 12)).pack(pady=10)

        listbox = tk.Listbox(root, height=8)
        listbox.pack(fill=tk.BOTH, padx=20, pady=5)

        btn_Frame = tk.Frame(root)
        btn_Frame.pack(pady=10)

        tk.Button(btn_Frame, text="Add Application", command=add_app).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_Frame,text="remove selected", command=remove_app).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

        update_list()
        root.mainloop()
        self.running = False

if __name__ == "__main__":
    locker = AppLocker()
    locker.run()
    
    
