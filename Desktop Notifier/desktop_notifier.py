import tkinter as tk
from tkinter import ttk
import threading
import time
from plyer import notification
import json
import os

class NotifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Notifier")
        self.root.geometry("250x130")
        
        # Variables
        self.interval = tk.IntVar(value=30)
        self.is_running = False
        self.notification_thread = None
        
        self.setup_gui()
        self.load_settings()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Interval setting
        ttk.Label(main_frame, text="Reminder Interval (minutes):").grid(row=0, column=0, pady=5)
        ttk.Entry(main_frame, textvariable=self.interval, width=10).grid(row=0, column=1, pady=5)

        # Start/Stop button
        self.toggle_button = ttk.Button(main_frame, text="Start", command=self.toggle_notifications)
        self.toggle_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Stopped")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.interval.set(settings.get('interval', 30))
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        try:
            settings = {
                'interval': self.interval.get()
            }
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def show_notification(self):
        while self.is_running:
            notification.notify(
                title="Drink Water Reminder",
                message="It's time to drink water! Stay hydrated!",
                app_icon=None,  # e.g. 'icon.ico'
                timeout=10,
            )
            time.sleep(self.interval.get() * 60)  # Convert minutes to seconds

    def toggle_notifications(self):
        if not self.is_running:
            try:
                interval = self.interval.get()
                if interval <= 0:
                    raise ValueError("Interval must be positive")
                
                self.is_running = True
                self.toggle_button.config(text="Stop")
                self.status_label.config(text="Status: Running")
                self.save_settings()
                
                self.notification_thread = threading.Thread(target=self.show_notification)
                self.notification_thread.daemon = True
                self.notification_thread.start()
            
            except ValueError as e:
                tk.messagebox.showerror("Error", str(e))
        else:
            self.is_running = False
            self.toggle_button.config(text="Start")
            self.status_label.config(text="Status: Stopped")
            if self.notification_thread:
                self.notification_thread.join(0)

    def on_closing(self):
        self.is_running = False
        if self.notification_thread:
            self.notification_thread.join(0)
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotifierApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()