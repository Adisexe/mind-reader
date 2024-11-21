import tkinter as tk
from tkinter import ttk
import time
from threading import Thread

# [FUNCTIONS]

def validate_input(text):
    if text.isdigit() and 1 <= int(text) <= 10:
        return True
    return False

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_left = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_left}+{position_top}')

def on_submit():
    value = input_var.get()
    if validate_input(value):
        error_label.config(text="")
        input_entry.config(state='disabled')
        show_progress_window(value)
    else:
        error_label.config(text="Enter a number from 1 to 10!")


# [WINDOWS]

# Progress bar window
def show_progress_window(value):
    progress_window = tk.Toplevel(root)
    progress_window.title("Mind reader")
    center_window(progress_window, 400, 150)
    progress_window.resizable(False, False)
    progress_window.grab_set()

    def on_close():
        input_entry.config(state='normal')
        progress_window.destroy()

    progress_window.protocol("WM_DELETE_WINDOW", on_close)

    descriptions = ["Deciphering thoughts...", "Scanning memory...", "Calculating probabilities...", "Analyzing collected data..."]
    description_label = tk.Label(progress_window, text=descriptions[0], font=("Arial", 12))
    description_label.pack(pady=10)

    progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)
    progress["maximum"] = 100

    def update_progress():
        total_time = 8
        steps = 100
        step_time = total_time / steps
        for i in range(steps):
            time.sleep(step_time)
            
            if not progress_window.winfo_exists() or not progress.winfo_exists():
                return  

            progress["value"] = i + 1

            if i == 25:
                description_label.config(text=descriptions[1])
            elif i == 50:
                description_label.config(text=descriptions[2])
            elif i == 75:
                description_label.config(text=descriptions[3])

            progress_window.update_idletasks()

        if progress_window.winfo_exists():
            progress_window.destroy()
            show_final_window(value)

    Thread(target=update_progress, daemon=True).start()


# Result window
def show_final_window(value):
    final_window = tk.Toplevel(root)
    final_window.title("Result")
    center_window(final_window, 300, 150)
    final_window.grab_set()
  
    final_text = f"You are thinking of the number {value}"
    final_label = tk.Label(final_window, text=final_text, font=("Arial", 12))
    final_label.pack(pady=20, padx=20)

    close_button = tk.Button(final_window, text="Close", command=final_window.destroy, font=("Arial", 12))
    close_button.pack(pady=10)

    final_window.wait_window(final_window)

    input_entry.config(state='normal')

# [MAIN WINDOW]
root = tk.Tk()
root.title("Mind reader")

center_window(root, 300, 150)
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

description_label = tk.Label(frame, text="Enter a number from 1 to 10:", font=("Arial", 12))
description_label.grid(row=0, column=0, columnspan=2, pady=5)

input_var = tk.StringVar()
input_entry = tk.Entry(frame, textvariable=input_var, font=("Arial", 12))
input_entry.grid(row=1, column=0, columnspan=2, pady=5)

submit_button = tk.Button(frame, text="Read my mind", command=on_submit, font=("Arial", 12))
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

error_label = tk.Label(frame, text="", font=("Arial", 10), fg="red")
error_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
