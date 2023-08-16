import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import os
from playsound import playsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer Tool")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.time_label = ttk.Label(root, text="Time: 00:00", font=("Helvetica", 24))
        self.time_label.pack(pady=20)

        self.time_input = ttk.Entry(root, font=("Helvetica", 16))
        self.time_input.pack()

        self.start_button = ttk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(pady=10)

        self.pause_button = ttk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(pady=10)

        self.resume_button = ttk.Button(root, text="Resume", command=self.resume_timer)
        self.resume_button.pack(pady=10)

        self.select_sound_button = ttk.Button(root, text="Select Notification Sound", command=self.select_notification_sound)
        self.select_sound_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", pady=10)

        self.running = False
        self.paused = False
        self.target_time = 0
        self.seconds = 0
        self.start_time = 0
        self.notification_sound = "default_notification.wav"

    def update_timer(self):
        while self.running and self.seconds < self.target_time:
            if not self.paused:
                self.seconds = int(time.time() - self.start_time)
                remaining_seconds = self.target_time - self.seconds
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60
                time_str = f"Time: {minutes:02d}:{seconds:02d}"
                self.time_label.config(text=time_str)
                self.progress_bar["value"] = (self.seconds / self.target_time) * 100
            time.sleep(1)

        if self.running:
            self.running = False
            self.paused = False
            self.time_label.config(text="Time: 00:00")
            self.progress_bar["value"] = 0
            messagebox.showinfo("Timer Completed", "Timer has completed!")
            playsound(self.notification_sound)

    def start_timer(self):
        if not self.running:
            try:
                self.target_time = int(self.time_input.get()) * 60
                self.running = True
                self.start_time = time.time()
                self.timer_thread = threading.Thread(target=self.update_timer)
                self.timer_thread.start()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for time in minutes.")

    def stop_timer(self):
        if self.running:
            self.running = False
            self.paused = False
            self.timer_thread.join()
            self.time_label.config(text="Time: 00:00")
            self.progress_bar["value"] = 0
            messagebox.showinfo("Timer Stopped", "Timer has been stopped.")

    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True

    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False
            self.start_time = time.time() - self.seconds

    def select_notification_sound(self):
        self.notification_sound = simpledialog.askstring("Notification Sound", "Enter the path to a sound file for notifications:")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    app.run()
