import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import dateutil.parser
import customtkinter as ctk
from PIL import Image, ImageTk

# Constants
MEDICATION_FILE = 'medication.csv'

# Track reminders that have been shown today
shown_reminders = set()

# Ensure medication file exists
def ensure_medication_file_exists():
    try:
        with open(MEDICATION_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Medication Name", "Dosage", "Frequency", "Schedule Time"])
    except FileExistsError:
        pass

# Function to load medication data from CSV
def load_medication_data():
    medication_data = []
    try:
        with open(MEDICATION_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                medication_data.append(row)
    except FileNotFoundError:
        print(f"File {MEDICATION_FILE} not found.")
    return medication_data

# Function to display medication information
def display_medication_info():
    medication_data = load_medication_data()
    for row in medication_data:
        label_medication_name = ctk.CTkLabel(scrollable_frame, text=row, font=("Arial", 12))
        label_medication_name.pack(pady=10, anchor="w")

# Function to set reminders for medication
def set_medication_reminders():
    print("Setting medication reminders...")
    medication_data = load_medication_data()
    current_time = datetime.datetime.now().strftime("%H:%M")

    for row in medication_data:
        medication_name = row[0]
        schedule_time_str = row[3]

        # Parse the schedule time string to a datetime object
        try:
            schedule_time = dateutil.parser.parse(schedule_time_str).strftime("%H:%M")
        except ValueError:
            print(f"Invalid time format for {medication_name}: {schedule_time_str}")
            continue

        reminder_id = f"{medication_name}-{schedule_time}"

        print(f"Checking reminder for {medication_name} at {schedule_time}, current time is {current_time}")

        if current_time == schedule_time and reminder_id not in shown_reminders:
            messagebox.showinfo("Medication Reminder", f"It's time to take {medication_name}.")
            print(f"Reminder: Take {medication_name}!")
            shown_reminders.add(reminder_id)

    # Schedule the next reminder check in one minute
    window.after(60000, set_medication_reminders)

# Function to reset reminders at midnight
def reset_reminders():
    global shown_reminders
    shown_reminders = set()
    print("Reset reminders for a new day.")
    # Schedule the next reset at midnight
    now = datetime.datetime.now()
    next_reset = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    delay = (next_reset - now).total_seconds() * 1000  # milliseconds
    window.after(int(delay), reset_reminders)

# Function to add medication to the schedule
def add_medication_schedule():
    medication_name = entry_medication_name.get()
    dosage = entry_dosage.get()
    frequency = entry_frequency.get()
    schedule_time = entry_schedule_time.get()

    # Append the medication schedule to the CSV file
    with open(MEDICATION_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([medication_name, dosage, frequency, schedule_time])
    messagebox.showinfo("Success", "Medication schedule added successfully.")
    top1.destroy()  # Close the add medication window after adding

def add_medication():
    global top1, entry_medication_name, entry_dosage, entry_frequency, entry_schedule_time

    top1 = ctk.CTkToplevel()
    top1.title("Add Medication")
    top1.geometry("155x300")
    top1.resizable(False, False)  # Prevent maximizing the window

    # Add scrollable frame
    container = ctk.CTkFrame(top1)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="lightgray")
    scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Medication Schedule Form
    ctk.CTkLabel(scrollable_frame, text="Medication Name:", text_color="#FFFFFF", font=("Arial Bold", 14)).pack(anchor="w", padx=(10, 0), pady=(5, 0))
    entry_medication_name = ctk.CTkEntry(scrollable_frame, font=("Arial", 12))
    entry_medication_name.pack(anchor="w", padx=(10, 0), pady=(5, 0))

    ctk.CTkLabel(scrollable_frame, text="Dosage:", text_color="#FFFFFF", font=("Arial Bold", 14)).pack(anchor="w", padx=(10, 0), pady=(5, 0))
    entry_dosage = ctk.CTkEntry(scrollable_frame, font=("Arial", 12))
    entry_dosage.pack(anchor="w", padx=(10, 0), pady=(5, 0))

    ctk.CTkLabel(scrollable_frame, text="Frequency:", text_color="#FFFFFF", font=("Arial Bold", 14)).pack(anchor="w", padx=(10, 0), pady=(5, 0))
    entry_frequency = ctk.CTkEntry(scrollable_frame, font=("Arial", 12))
    entry_frequency.pack(anchor="w", padx=(10, 0), pady=(5, 0))

    ctk.CTkLabel(scrollable_frame, text="Schedule Time:", text_color="#FFFFFF", font=("Arial Bold", 14)).pack(anchor="w", padx=(10, 0), pady=(5, 0))
    entry_schedule_time = ctk.CTkEntry(scrollable_frame, font=("Arial", 12))
    entry_schedule_time.pack(anchor="w", padx=(10, 0), pady=(5, 0))

    ctk.CTkButton(scrollable_frame, text="Add Medication", command=add_medication_schedule, fg_color="#a9b8c4", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff").pack(anchor="w", padx=(10, 0), pady=(5, 10))

def display_medication():
    global top, scrollable_frame
    top = ctk.CTkToplevel()
    top.title("Display Medication Reminder")
    top.geometry("170x400")
    top.resizable(False, False)  # Prevent maximizing the window

    # Add scrollable frame
    canvas = tk.Canvas(top)
    scrollbar = ctk.CTkScrollbar(top, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Medication Schedule Form
    ctk.CTkLabel(scrollable_frame, text='Display Medication', font=("Arial Bold", 16), text_color="#601E88").pack(pady=10)

    ctk.CTkButton(scrollable_frame, text='Click to view Medication', command=display_medication_info, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff").pack(pady=10)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def close():
    window.destroy()

# Create the main window
ctk.set_appearance_mode("dark")  # Use customtkinter dark mode
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("Medication Reminder")
window.geometry("400x500")
window.resizable(False, False)  # Prevent maximizing the window

# Ensure medication file exists
ensure_medication_file_exists()

# Load images
image1 = Image.open("elder2.jpg")
image1 = image1.resize((100, 100), Image.LANCZOS)
photo1 = ctk.CTkImage(dark_image=image1, size=(100, 100))

image2 = Image.open("eldercare.jpg")
image2 = image2.resize((100, 100), Image.LANCZOS)
photo2 = ctk.CTkImage(dark_image=image2, size=(100, 100))

# Create a label with custom styling
label = ctk.CTkLabel(window, text="Medication Reminder", font=("Arial Bold", 20), pady=20, text_color="#601E88")
label.pack()

# Display images
image_label1 = ctk.CTkLabel(window, image=photo1, text="")
image_label1.pack(pady=10)
image_label2 = ctk.CTkLabel(window, image=photo2, text="")
image_label2.pack(pady=10)

# Create a styled frame for buttons
button_frame = ctk.CTkFrame(window)
button_frame.pack(padx=20, pady=20)

# Create three styled buttons vertically aligned
ctk.CTkButton(button_frame, text="Add Medication", command=add_medication, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(pady=10)
ctk.CTkButton(button_frame, text="Display Medication", command=display_medication, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(pady=10)
ctk.CTkButton(button_frame, text="Set Reminder", command=set_medication_reminders, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(pady=10)
ctk.CTkButton(button_frame, text="Exit/Close", command=close, font=("Arial Bold", 12), text_color="#ffffff", width=225, fg_color="#601E88", hover_color="#E44982").pack(pady=10)

# Start the reminder checking loop
set_medication_reminders()

# Reset reminders at midnight
reset_reminders()

# Start the main loop
window.mainloop()
