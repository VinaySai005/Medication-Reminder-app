import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

# Load the custom theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("custom_theme.json")

# Function to handle registration
def register():
    first_name = reg_first_name_entry.get()
    last_name = reg_last_name_entry.get()
    email = reg_email_entry.get()
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    mobile_number = reg_mobile_number_entry.get()
    age = reg_age_entry.get()
    gender = reg_gender_var.get()
    previous_medical_issues = reg_previous_medical_issues_entry.get("1.0", tk.END).strip()
    emergency_contact_name = reg_emergency_contact_name_entry.get()
    emergency_contact_number = reg_emergency_contact_number_entry.get()

    # Validate the inputs
    if not first_name or not last_name or not email or not username or not password or not mobile_number or not age or not gender or not emergency_contact_name or not emergency_contact_number:
        messagebox.showerror("Error", "All fields are required except previous medical issues.")
        return

    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        messagebox.showerror("Error", "Invalid email address.")
        return

    if not re.match(r"^[0-9]{10}$", mobile_number):
        messagebox.showerror("Error", "Invalid mobile number. It should be 10 digits.")
        return

    if not re.match(r"^[0-9]{10}$", emergency_contact_number):
        messagebox.showerror("Error", "Invalid emergency contact number. It should be 10 digits.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    # Insert data into the database
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ASdbG12K90vGnM",
            database="ElderlyCare"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO registration (
                first_name, last_name, email, username, password, mobile_number, age, gender, previous_medical_issues, emergency_contact_name, emergency_contact_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, username, password, mobile_number, age, gender, previous_medical_issues, emergency_contact_name, emergency_contact_number))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        if conn:
            conn.close()

# Function to handle login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    # Validate the inputs
    if not username or not password:
        messagebox.showerror("Error", "Both fields are required.")
        return

    # Check credentials in the database
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ASdbG12K90vGnM",
            database="ElderlyCare"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM registration WHERE username=%s AND password=%s
        """, (username, password))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Success", "Login successful.")
            show_user_options()
        else:
            messagebox.showerror("Error", "Invalid credentials.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        if conn:
            conn.close()

# Function to handle adding medication
def add_medication(username, medication_name, dosage, frequency, reminder_time):
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ASdbG12K90vGnM",
            database="ElderlyCare"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medications (username, medication_name, dosage, frequency, reminder_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, medication_name, dosage, frequency, reminder_time))
        conn.commit()
        messagebox.showinfo("Success", "Medication added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        if conn:
            conn.close()

# Function to show the registration frame
def show_registration_frame():
    login_frame.pack_forget()
    registration_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Function to show the login frame
def show_login_frame():
    registration_frame.pack_forget()
    login_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Function to show user options after successful login
def show_user_options():
    login_frame.pack_forget()
    user_options_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Function to show the add medication frame
def show_add_medication_frame():
    user_options_frame.pack_forget()
    add_medication_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Function to handle adding medication
def handle_add_medication():
    username = add_med_username_entry.get()
    medication_name = add_med_medication_name_entry.get()
    dosage = add_med_dosage_entry.get()
    frequency = add_med_frequency_entry.get()
    reminder_time = add_med_reminder_time_entry.get()

    # Validate the inputs
    if not username or not medication_name or not dosage or not frequency or not reminder_time:
        messagebox.showerror("Error", "All fields are required.")
        return

    add_medication(username, medication_name, dosage, frequency, reminder_time)

# Set up the main window
root = ctk.CTk()
root.title("Elderly Healthcare Registration and Login")
root.geometry("1000x500")
root.resizable(False, False)  # Disable window maximization

# Set up the login frame
login_frame = ctk.CTkFrame(root)
login_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Load the image
image = tk.PhotoImage(file="side-img.png")
image_label = tk.Label(login_frame, image=image)
image_label.pack(side="left", padx=(0, 10))

ctk.CTkLabel(login_frame, text="Login", font=("Arial Bold", 24), text_color="#FFFFFF").pack(pady=10)

ctk.CTkLabel(login_frame, text="  Username:", text_color="#FFFFFF", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
login_username_entry = ctk.CTkEntry(login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
login_username_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(login_frame, text="  Password:", text_color="#FFFFFF", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
login_password_entry = ctk.CTkEntry(login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
login_password_entry.pack(anchor="w", padx=(25, 0), pady=(5, 20))

ctk.CTkButton(login_frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=login).pack(anchor="w", padx=(25, 0), pady=(5, 10))
ctk.CTkButton(login_frame, text="Register", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 12), text_color="#601E88", width=225, command=show_registration_frame).pack(anchor="w", padx=(25, 0), pady=(5, 10))

# Set up the registration frame
registration_frame = ctk.CTkScrollableFrame(root)  # Changed to CTkScrollableFrame

ctk.CTkLabel(registration_frame, text="Register", font=("Arial Bold", 24), text_color="#FFFFFF").pack(pady=10)

ctk.CTkLabel(registration_frame, text="  First Name:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_first_name_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_first_name_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Last Name:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_last_name_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_last_name_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Email:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_email_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_email_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Username:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_username_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_username_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Password:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_password_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
reg_password_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Mobile Number:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_mobile_number_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_mobile_number_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Age:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_age_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_age_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Gender:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_gender_var = tk.StringVar()
ctk.CTkRadioButton(registration_frame, text="Male", variable=reg_gender_var, value="Male", text_color="#FFFFFF", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0), pady=(5, 2))
ctk.CTkRadioButton(registration_frame, text="Female", variable=reg_gender_var, value="Female", text_color="#FFFFFF", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0), pady=(5, 2))
ctk.CTkRadioButton(registration_frame, text="Other", variable=reg_gender_var, value="Other", text_color="#FFFFFF", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0), pady=(5, 2))

ctk.CTkLabel(registration_frame, text="  Previous Medical Issues:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_previous_medical_issues_entry = ctk.CTkTextbox(registration_frame, height=5, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_previous_medical_issues_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Emergency Contact Name:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_emergency_contact_name_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_emergency_contact_name_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(registration_frame, text="  Emergency Contact Number:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
reg_emergency_contact_number_entry = ctk.CTkEntry(registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
reg_emergency_contact_number_entry.pack(anchor="w", padx=(25, 0), pady=(5, 20))

ctk.CTkButton(registration_frame, text="Register", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=register).pack(anchor="w", padx=(25, 0), pady=(5, 10))
ctk.CTkButton(registration_frame, text="Back to Login", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 12), text_color="#601E88", width=225, command=show_login_frame).pack(anchor="w", padx=(25, 0), pady=(5, 10))

# Set up the user options frame
user_options_frame = ctk.CTkFrame(root)

ctk.CTkLabel(user_options_frame, text="User Options", font=("Arial Bold", 24), text_color="#601E88").pack(pady=10)

ctk.CTkButton(user_options_frame, text="Add Medication", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=show_add_medication_frame).pack(pady=5)
ctk.CTkButton(user_options_frame, text="Display Medication", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(pady=5)
ctk.CTkButton(user_options_frame, text="Set Reminder", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(pady=5)

# Set up the add medication frame
add_medication_frame = ctk.CTkFrame(root)

ctk.CTkLabel(add_medication_frame, text="Add Medication", font=("Arial Bold", 24), text_color="#FFFFFF").pack(pady=10)

ctk.CTkLabel(add_medication_frame, text="  Username:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
add_med_username_entry = ctk.CTkEntry(add_medication_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
add_med_username_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(add_medication_frame, text="  Medication Name:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
add_med_medication_name_entry = ctk.CTkEntry(add_medication_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
add_med_medication_name_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(add_medication_frame, text="  Dosage:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
add_med_dosage_entry = ctk.CTkEntry(add_medication_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
add_med_dosage_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(add_medication_frame, text="  Frequency:", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
add_med_frequency_entry = ctk.CTkEntry(add_medication_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
add_med_frequency_entry.pack(anchor="w", padx=(25, 0), pady=(5, 10))

ctk.CTkLabel(add_medication_frame, text="  Reminder Time (HH:MM:SS):", text_color="#66FCF1", font=("Arial Bold", 14)).pack(anchor="w", padx=(25, 0))
add_med_reminder_time_entry = ctk.CTkEntry(add_medication_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
add_med_reminder_time_entry.pack(anchor="w", padx=(25, 0), pady=(5, 20))

ctk.CTkButton(add_medication_frame, text="Add Medication", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=handle_add_medication).pack(anchor="w", padx=(25, 0), pady=(5, 10))
ctk.CTkButton(add_medication_frame, text="Back to User Options", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 12), text_color="#601E88", width=225, command=show_user_options).pack(anchor="w", padx=(25, 0), pady=(5, 10))

# Start with the login frame
show_login_frame()

root.mainloop()
