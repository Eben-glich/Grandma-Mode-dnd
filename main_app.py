#!/usr/bin/env python3
"""
Grandma Mode - Do Not Disturb Main Application
Allows up to 7 remote devices to temporarily disable DND for 10 minutes
"""

import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
from datetime import datetime, timedelta
import uuid
import threading
import socket
from pathlib import Path

CONFIG_DIR = Path.home() / ".grandma_mode_dnd"
CONFIG_FILE = CONFIG_DIR / "config.json"
DB_FILE = CONFIG_DIR / "grandma_mode.db"
FIRST_LAUNCH_FILE = CONFIG_DIR / "first_launch_complete"


class GrandmaModeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grandma Mode - DND Manager")
        self.root.geometry("600x400")
        self.setup_config()
        
        if not FIRST_LAUNCH_FILE.exists():
            self.first_launch_setup()
        else:
            self.show_main_interface()
    
    def setup_config(self):
        """Initialize configuration directory and database"""
        CONFIG_DIR.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing device info and DND status"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Devices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                access_code TEXT NOT NULL,
                added_date TEXT NOT NULL,
                device_number INTEGER
            )
        ''')
        
        # DND status table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dnd_status (
                id INTEGER PRIMARY KEY,
                is_active INTEGER DEFAULT 1,
                deactivated_until TEXT,
                deactivated_by TEXT,
                last_modified TEXT
            )
        ''')
        
        # Activity log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                device_name TEXT,
                action TEXT,
                duration_minutes INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def first_launch_setup(self):
        """Setup GUI for first launch - add 7 remote devices"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(frame, text="Grandma Mode - First Time Setup", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        subtitle = tk.Label(frame, text="Add up to 7 remote devices\n(These can deactivate DND for 10 minutes)",
                           font=("Arial", 10), justify=tk.CENTER)
        subtitle.pack(pady=10)
        
        self.device_entries = []
        devices_frame = tk.Frame(frame)
        devices_frame.pack(fill=tk.BOTH, expand=True)
        
        for i in range(7):
            device_frame = tk.Frame(devices_frame)
            device_frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(device_frame, text=f"Device {i+1}:")
            label.pack(side=tk.LEFT, width=10)
            
            entry = tk.Entry(device_frame, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.device_entries.append(entry)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        next_btn = tk.Button(button_frame, text="Save Devices", 
                            command=self.save_devices)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        skip_btn = tk.Button(button_frame, text="Skip", 
                            command=self.complete_first_launch)
        skip_btn.pack(side=tk.LEFT, padx=5)
    
    def save_devices(self):
        """Save device names and generate access codes"""
        device_names = [entry.get().strip() for entry in self.device_entries if entry.get().strip()]
        
        if len(device_names) == 0:
            messagebox.showwarning("No Devices", "Please enter at least one device name")
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for i, name in enumerate(device_names, 1):
            device_id = str(uuid.uuid4())
            access_code = self.generate_access_code()
            
            cursor.execute('''
                INSERT INTO devices (id, name, access_code, added_date, device_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (device_id, name, access_code, datetime.now().isoformat(), i))
        
        # Initialize DND status
        cursor.execute('''
            INSERT INTO dnd_status (is_active, last_modified)
            VALUES (1, ?)
        ''', (datetime.now().isoformat(),))
        
        conn.commit()
        conn.close()
        
        self.save_config()
        self.complete_first_launch()
        messagebox.showinfo("Success", f"Added {len(device_names)} devices!\n\nCheck the remote app to see access codes.")
    
    def generate_access_code(self):
        """Generate a random access code for remote device"""
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def save_config(self):
        """Save application configuration"""
        config = {
            "version": "1.0",
            "setup_completed": True,
            "created_at": datetime.now().isoformat()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    def complete_first_launch(self):
        """Mark first launch as complete"""
        FIRST_LAUNCH_FILE.touch()
        self.show_main_interface()
    
    def show_main_interface(self):
        """Display main application interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(frame, text="Grandma Mode - DND Manager", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Status display
        status_frame = tk.LabelFrame(frame, text="DND Status", padx=10, pady=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(status_frame, text=self.get_dnd_status(),
                                     font=("Arial", 12), fg="green")
        self.status_label.pack(pady=5)
        
        # Devices display
        devices_frame = tk.LabelFrame(frame, text="Registered Devices", padx=10, pady=10)
        devices_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.refresh_devices_display(devices_frame)
        
        # Controls
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="View Activity Log", 
                 command=self.show_activity_log).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Settings", 
                 command=self.show_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", 
                 command=lambda: self.show_main_interface()).pack(side=tk.LEFT, padx=5)
        
        # Start server
        self.start_server()
    
    def refresh_devices_display(self, frame):
        """Display all registered devices"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT name, access_code, device_number FROM devices ORDER BY device_number')
        devices = cursor.fetchall()
        conn.close()
        
        if not devices:
            tk.Label(frame, text="No devices configured", font=("Arial", 10)).pack()
        else:
            for name, code, num in devices:
                device_label = tk.Label(frame, text=f"{num}. {name} - Code: {code}",
                                       font=("Arial", 10), fg="blue")
                device_label.pack(anchor=tk.W, pady=3)
    
    def get_dnd_status(self):
        """Get current DND status"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT is_active, deactivated_until FROM dnd_status LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            is_active, deactivated_until = result
            if is_active and deactivated_until:
                return f"DND Active (Disabled until: {deactivated_until})"
            elif is_active:
                return "DND Active"
            else:
                return "DND Inactive"
        return "DND Status Unknown"
    
    def show_activity_log(self):
        """Display activity log in new window"""
        log_window = tk.Toplevel(self.root)
        log_window.title("Activity Log")
        log_window.geometry("500x300")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp, device_name, action FROM activity_log ORDER BY timestamp DESC LIMIT 20')
        logs = cursor.fetchall()
        conn.close()
        
        text_widget = tk.Text(log_window, font=("Courier", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for timestamp, device, action in logs:
            text_widget.insert(tk.END, f"{timestamp} - {device}: {action}\n")
        
        text_widget.config(state=tk.DISABLED)
    
    def show_settings(self):
        """Show settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x200")
        
        tk.Label(settings_window, text="DND Settings", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Button(settings_window, text="Reset Devices", 
                 command=self.reset_devices).pack(pady=5)
        tk.Button(settings_window, text="Clear Activity Log", 
                 command=self.clear_log).pack(pady=5)
    
    def reset_devices(self):
        """Reset all devices"""
        if messagebox.askyesno("Confirm", "Reset all devices? You'll need to reconfigure them."):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM devices')
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Devices reset. Restart the app for setup.")
    
    def clear_log(self):
        """Clear activity log"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM activity_log')
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Activity log cleared")
    
    def start_server(self):
        """Start background server for remote device access"""
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        server_thread.start()
    
    def run_server(self):
        """Server listening for remote device requests"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', 5555))
            server_socket.listen(1)
            
            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    request = client_socket.recv(1024).decode('utf-8')
                    self.handle_remote_request(request, client_socket)
                except:
                    pass
        except:
            pass
    
    def handle_remote_request(self, request, client_socket):
        """Handle incoming requests from remote devices"""
        try:
            data = json.loads(request)
            access_code = data.get('access_code')
            action = data.get('action')
            
            if action == 'deactivate_dnd':
                if self.verify_access_code(access_code):
                    device_name = self.get_device_name(access_code)
                    self.deactivate_dnd_for_10min(device_name)
                    response = json.dumps({"status": "success", "message": "DND disabled for 10 minutes"})
                    self.log_activity(device_name, "Disabled DND for 10 minutes")
                else:
                    response = json.dumps({"status": "error", "message": "Invalid access code"})
            else:
                response = json.dumps({"status": "error", "message": "Unknown action"})
            
            client_socket.send(response.encode('utf-8'))
        except:
            pass
        finally:
            client_socket.close()
    
    def verify_access_code(self, code):
        """Verify if access code is valid"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM devices WHERE access_code = ?', (code,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def get_device_name(self, code):
        """Get device name from access code"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM devices WHERE access_code = ?', (code,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Unknown"
    
    def deactivate_dnd_for_10min(self, device_name):
        """Deactivate DND for 10 minutes"""
        deactivated_until = (datetime.now() + timedelta(minutes=10)).isoformat()
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE dnd_status 
            SET is_active = 0, deactivated_until = ?, deactivated_by = ?, last_modified = ?
        ''', (deactivated_until, device_name, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def log_activity(self, device_name, action):
        """Log device activity"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activity_log (timestamp, device_name, action, duration_minutes)
            VALUES (?, ?, ?, 10)
        ''', (datetime.now().isoformat(), device_name, action))
        conn.commit()
        conn.close()


def main():
    root = tk.Tk()
    app = GrandmaModeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
