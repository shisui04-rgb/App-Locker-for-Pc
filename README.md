AppLocker 🔒
A simple Python-based GUI utility to lock and restrict access to specific applications on Windows. AppLocker runs with administrator privileges and continuously monitors running processes, terminating any that match the locked list.

📌 Features
✅ Lock any .exe application from running

🔐 Password protection for changes to locked apps

💾 Configuration is saved in a JSON file under %APPDATA%\AppLocker

🧠 Automatically relaunches with admin privileges if not already

🪟 Simple and lightweight Tkinter GUI

📁 Project Structure
bash
Copy
Edit
AppLocker/
│
├── app_locker.py       # Main application code
├── config.json         # Configuration (auto-generated in %APPDATA%\AppLocker)
└── README.md           # Project documentation
🚀 How It Works
On the first run, it prompts to set a password.

The user can add/remove .exe files to a list of locked apps.

AppLocker monitors all running processes and kills any locked app.

All modifications to the locked list require password authentication.

🧰 Requirements
Python 3.6+

Required Python packages:

psutil

tkinter (usually included with Python)

Install requirements via pip (if needed):

bash
Copy
Edit
pip install psutil
⚙️ How to Use
Run the script as administrator (or it will auto-request elevation):

bash
Copy
Edit
python app_locker.py
Set a password on first launch.

Use the GUI to:

Add applications (.exe) to the lock list.

Remove them with password verification.

Close the window to stop the monitor.

🛑 Important Notes
This tool is for Windows only.

Killing protected processes might require elevated privileges.

This tool does not prevent the app from being launched — it monitors and kills the process after detection.

Password is stored as a SHA-256 hash in the config file (not plaintext).

🧪 Example Use Case
Want to prevent games like game.exe or tools like notepad.exe from running without your permission? Add them to AppLocker's locked list, and it will quietly terminate them if launched.

📂 Config File Location
arduino
Copy
Edit
%APPDATA%\AppLocker\config.json
This file stores:

locked_apps: List of locked .exe paths

password_hash: SHA-256 hash of your set password

👨‍💻 Author
Developed by Akarshak Srivastav

