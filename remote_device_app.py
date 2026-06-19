#!/usr/bin/env python3
"""
Grandma Mode - Remote Device App
Allows remote devices to deactivate DND for 10 minutes
Includes location tracking
"""

import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading
from datetime import datetime
from pathlib import Path
import os
from PIL import Image, ImageDraw, ImageTk
import sys

try:
    from geolite2 import geolite2
    import geocoder
except ImportError:
    pass


class MyGrandmaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Grandma")
        self.root.geometry("500x600")
        self.server_ip = "localhost"
        self.server_port = 5555
        self.access_code = None
        self.latitude = None
        self.longitude = None
        self.accuracy = 0
        
        # Create and set icon
        self.create_icon()
        
        self.show_login_interface()
    
    def create_icon(self):
        """Create light blue icon with white capital G"""
        # Create a 256x256 image with light blue background
        size = 256
        image = Image.new('RGB', (size, size), color='#87CEEB')  # Light blue
        draw = ImageDraw.Draw(image)
        
        # Draw white capital G in the center
        try:
            # Try to use a larger font if available
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 180)
            except:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Draw "G" in white
        text = "G"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        # Convert to PhotoImage
        self.icon_image = ImageTk.PhotoImage(image)
        self.root.iconphoto(False, self.icon_image)
    
    def get_location(self):
        """Get device's GPS location"""
        try:
            import geocoder
            g = geocoder.ip('me')
            if g.ok:
                self.latitude = g.lat
                self.longitude = g.lng
                self.accuracy = int(g.accuracy) if hasattr(g, 'accuracy') else 50
                return True
        except:
            pass
        return False
    
    def show_login_interface(self):
        """Display login interface to enter access code"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon display
        try:
            icon_frame = tk.Frame(frame)
            icon_frame.pack(pady=20)
            icon_label = tk.Label(icon_frame, image=self.icon_image)
            icon_label.pack()
        except:
            pass
        
        title = tk.Label(frame, text="My Grandma", 
                        font=("Arial", 20, "bold"), fg="#4169E1")
        title.pack(pady=10)
        
        subtitle = tk.Label(frame, text="Emergency DND Deactivation", 
                           font=("Arial", 12), fg="gray")
        subtitle.pack(pady=5)
        
        # Server connection info
        conn_frame = tk.LabelFrame(frame, text="Server Settings", padx=15, pady=10)
        conn_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(conn_frame, text="Server IP:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        self.ip_entry = tk.Entry(conn_frame, width=30)
        self.ip_entry.insert(0, self.server_ip)
        self.ip_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(conn_frame, text="Server Port:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        self.port_entry = tk.Entry(conn_frame, width=30)
        self.port_entry.insert(0, str(self.server_port))
        self.port_entry.pack(fill=tk.X, pady=5)
        
        # Access code entry
        code_frame = tk.LabelFrame(frame, text="Access Code (8-digit)", padx=15, pady=10)
        code_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(code_frame, text="Enter your device's 8-digit code:", 
                font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        
        self.code_entry = tk.Entry(code_frame, width=30, font=("Arial", 14), 
                                   justify=tk.CENTER)
        self.code_entry.pack(fill=tk.X, pady=10)
        self.code_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(button_frame, text="Login", 
                             command=self.login, bg="#87CEEB", fg="white",
                             font=("Arial", 12, "bold"), padx=20, pady=10)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        help_btn = tk.Button(button_frame, text="Help", 
                            command=self.show_help)
        help_btn.pack(side=tk.LEFT, padx=5)
    
    def login(self):
        """Validate access code"""
        code = self.code_entry.get().strip()
        
        if not code:
            messagebox.showwarning("Input Error", "Please enter the 8-digit access code")
            return
        
        if len(code) != 8 or not code.isdigit():
            messagebox.showerror("Invalid Code", "Access code must be exactly 8 digits")
            return
        
        try:
            self.server_ip = self.ip_entry.get().strip()
            self.server_port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Port", "Port must be a number")
            return
        
        self.access_code = code
        
        # Get location in background
        threading.Thread(target=self.get_location, daemon=True).start()
        
        self.show_main_interface()
    
    def show_main_interface(self):
        """Display main control interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon
        try:
            icon_frame = tk.Frame(frame)
            icon_frame.pack(pady=15)
            icon_label = tk.Label(icon_frame, image=self.icon_image)
            icon_label.pack()
        except:
            pass
        
        title = tk.Label(frame, text="My Grandma", 
                        font=("Arial", 24, "bold"), fg="#4169E1")
        title.pack(pady=10)
        
        # Status info
        status_frame = tk.LabelFrame(frame, text="Status", padx=15, pady=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        status_text = "✓ Connected to Grandma's Phone\n"
        status_text += f"Access Code: {'*' * 8}\n"
        if self.latitude and self.longitude:
            status_text += f"Location: {self.latitude:.4f}, {self.longitude:.4f}\n"
            status_text += f"Accuracy: ±{self.accuracy}m"
        else:
            status_text += "Location: Detecting..."
        
        status_label = tk.Label(status_frame, text=status_text, 
                               font=("Arial", 10), justify=tk.LEFT)
        status_label.pack(anchor=tk.W)
        
        # Emergency deactivation button
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.BOTH, expand=True, pady=30)
        
        deactivate_btn = tk.Button(button_frame, text="DISABLE DND\nFOR 10 MINUTES", 
                                   command=self.deactivate_dnd,
                                   bg="#FF6B6B", fg="white",
                                   font=("Arial", 16, "bold"),
                                   padx=30, pady=40,
                                   relief=tk.RAISED, bd=4)
        deactivate_btn.pack(fill=tk.BOTH, expand=True)
        
        # Info section
        info_frame = tk.LabelFrame(frame, text="Information", padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Label(info_frame, 
                            text="This app allows you to temporarily disable\nDo Not Disturb mode for 10 minutes.\n\nYour location will be recorded.",
                            font=("Arial", 9), justify=tk.CENTER, fg="gray")
        info_text.pack()
        
        # Control buttons
        control_frame = tk.Frame(frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(control_frame, text="Logout", 
                 command=self.logout).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Settings", 
                 command=self.show_settings).pack(side=tk.LEFT, padx=5)
    
    def deactivate_dnd(self):
        """Send deactivation request to server"""
        if not self.access_code:
            messagebox.showerror("Error", "Not logged in")
            return
        
        # Confirm action
        if not messagebox.askyesno("Confirm", "Disable Grandma's DND for 10 minutes?"):
            return
        
        # Get current location
        self.get_location()
        
        try:
            # Create socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.server_ip, self.server_port))
            
            # Send request
            request = {
                "access_code": self.access_code,
                "action": "deactivate_dnd",
                "latitude": self.latitude,
                "longitude": self.longitude,
                "accuracy_meters": self.accuracy
            }
            
            sock.send(json.dumps(request).encode('utf-8'))
            
            # Receive response
            response_data = sock.recv(1024).decode('utf-8')
            response = json.loads(response_data)
            
            sock.close()
            
            if response.get('status') == 'success':
                messagebox.showinfo("Success", 
                    f"{response.get('message')}\n\nGrandma's phone will accept calls for 10 minutes.")
            else:
                messagebox.showerror("Error", response.get('message', 'Unknown error'))
        
        except socket.timeout:
            messagebox.showerror("Connection Error", 
                "Could not reach Grandma's phone.\nMake sure it's connected to the same network.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def logout(self):
        """Logout and return to login screen"""
        self.access_code = None
        self.show_login_interface()
        self.code_entry.delete(0, tk.END)
    
    def show_settings(self):
        """Show settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        
        frame = tk.Frame(settings_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Device info
        info_frame = tk.LabelFrame(frame, text="Device Information", padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        if self.latitude and self.longitude:
            info_text = f"Current Location:\n{self.latitude:.6f}, {self.longitude:.6f}\nAccuracy: ±{self.accuracy}m"
        else:
            info_text = "Location not yet detected"
        
        tk.Label(info_frame, text=info_text, font=("Arial", 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # About
        about_frame = tk.LabelFrame(frame, text="About", padx=10, pady=10)
        about_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(about_frame, text="My Grandma v1.0\nGrandma Mode Emergency DND Control\n\nDeveloped by Eben-glich",
                font=("Arial", 9), justify=tk.CENTER, fg="gray").pack()
    
    def show_help(self):
        """Show help window"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("450x400")
        
        text_widget = tk.Text(help_window, font=("Courier", 9), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_text = """MY GRANDMA - HELP GUIDE

HOW TO USE:
1. Enter the 8-digit access code provided by Grandma
2. Configure the server IP and port if needed
3. Click "Login" to connect
4. Press "DISABLE DND FOR 10 MINUTES" when you need to reach Grandma

SERVER SETTINGS:
- Default Server IP: localhost (or your Grandma's computer IP)
- Default Server Port: 5555
- Make sure both devices are on the same network

LOCATION TRACKING:
- Your location will be recorded with each action
- Accuracy depends on your device's GPS/network capabilities
- Location accuracy is typically ±50-100 meters for network location

SECURITY:
- Never share your 8-digit access code with others
- Only authorized devices should have this app
- Your location data is stored on Grandma's computer

TROUBLESHOOTING:
- If connection fails, check the server IP and port
- Make sure Grandma's DND app is running
- Verify both devices are on the same network
- Try restarting both applications

For more help, contact the app developer."""
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = MyGrandmaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
