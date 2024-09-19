# Medication-Reminder-app
"Elderly Healthcare Registration and Medication Management System" developed using Python's customtkinter for the graphical user interface (GUI) and MySQL as the database backend. The primary aim is to assist elderly individuals with medication management, including user registration, login, and reminder features.

# Elderly Healthcare Registration and Medication Management System

This is a Python-based application designed to help elderly individuals manage their medications, set reminders, and store personal health information securely. The system includes user registration, login, and medication tracking functionalities, with a modern graphical user interface built using `customtkinter`.

## Features

- **User Registration**: Allows new users to register by providing personal information such as name, email, mobile number, and emergency contact details.
- **User Login**: Registered users can log in using their credentials, which are stored securely in a MySQL database.
- **Medication Management**: After login, users can add medications by specifying the medication name, dosage, and reminder times.
- **GUI with `customtkinter`**: Modern and user-friendly interface for ease of use, especially for elderly users.
- **MySQL Database Integration**: User and medication data are stored securely in a MySQL database.

## Technologies Used

- **Python**: Core programming language.
- **customtkinter**: For creating the graphical user interface (GUI).
- **MySQL**: For storing user and medication data.
- **PIL (Pillow)**: For handling image-related functionalities.
- **tkinter**: For the main window management.

## Installation

### Prerequisites
- Python 3.x
- MySQL Server
- Required Python libraries: `customtkinter`, `mysql-connector-python`, `PIL`

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/elderly-healthcare-system.git
    cd elderly-healthcare-system
    ```

2. Install the required libraries:
    ```bash
    pip install customtkinter mysql-connector-python pillow
    ```

3. Set up the MySQL database:
   - Create a database and the required tables (`users`, `medications`).
   - Update the `db_config.py` file with your MySQL credentials.

4. Run the application:
    ```bash
    python main.py
    ```

## Database Schema

### Users Table:
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    mobile VARCHAR(15),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    emergency_contact VARCHAR(50),
    password VARCHAR(255)
);

Usage
Register: Enter your personal details to create an account.
Login: Use your credentials to log in.
Add Medications: Once logged in, you can add medications and set reminders for each medication.
View/Manage Medications: View your added medications and modify or delete them as needed.
Contributing
Fork the repository.
Create your feature branch: git checkout -b feature/YourFeature.
Commit your changes: git commit -m 'Add some feature'.
Push to the branch: git push origin feature/YourFeature.
Open a pull request.


Acknowledgments
customtkinter for the modern GUI framework.
MySQL for the database management.
All contributors and libraries used in the development of this project.
