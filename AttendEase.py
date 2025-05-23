# Logical imports
from datetime import datetime
import smtplib
import time
import sys
import csv
import os
import platform

# UI imports
import tkinter as tk
from tkinter import filedialog, Text, messagebox

# --------------------------------------------------------------------------------------------------------------
# Logical Code

def send_mail(day, curr_time, link):
    # NOTE: Replace EMAIL_HERE and PASSWORD_HERE with your credentials or better, use environment variables.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('EMAIL_HERE', 'PASSWORD_HERE')

    sent_from = 'EMAIL_HERE'
    to = ['ANOTHER_EMAIL_HERE']  # You can add multiple recipients here.
    subject = f"{day} Class Reminder for {curr_time}"
    body = f"User is attending online class at {link}. Join if you are having a class with him."

    email_text = f"Subject: {subject}\n\n{body}"

    server.sendmail(sent_from, to, email_text)
    server.quit()

def find_next_class(timetable_location, day):
    current_time = datetime.now().strftime("%H:%M")
    curr_time = time.strptime(current_time, "%H:%M")

    with open(timetable_location, 'r') as timetable:
        reader = csv.reader(timetable)
        for row in reader:
            if not row or len(row) <= day + 1:
                continue  # Skip empty or malformed rows

            try:
                class_time = time.strptime(row[0], "%H:%M")
            except ValueError:
                continue  # Skip header or invalid time rows

            if class_time >= curr_time and row[day + 1].strip().lower() == "exit":
                print("No more classes for today.")
                sys.exit()
            elif class_time >= curr_time and row[day + 1].strip() != "":
                print("Next Class at " + row[0])
                return class_time, row[day + 1].strip()

    print("Classes already over.")
    sys.exit()

def open_link(link):
    system = platform.system()
    if system == "Darwin":  # macOS
        os.system(f'open "{link}"')
    elif system == "Windows":
        os.system(f'start "" "{link}"')
    else:  # Linux and others
        os.system(f'xdg-open "{link}"')

def attend_class(timetable_location):
    Weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    day = datetime.today().weekday()
    print(Weekdays[day])

    while True:
        class_time, link = find_next_class(timetable_location, day)
        while True:
            current_time = datetime.now().strftime("%H:%M")
            curr_time = time.strptime(current_time, "%H:%M")
            print("Current Time : " + current_time)

            if class_time == curr_time:
                print("Class at " + current_time)
                open_link(link)
                print("Joined class at link : " + link)
                # send_mail(Weekdays[day], current_time, link)  # Uncomment if you want email notifications
                time.sleep(60)
                break

            time.sleep(60)

# --------------------------------------------------------------------------------------------------------------
# UI Code

root = tk.Tk()
root.title("Class Attendance Automation")
root.geometry("600x200")

apps = []

if os.path.isfile('save.txt'):
    with open('save.txt', 'r') as f:
        temp = f.read().strip()
        if temp:
            apps = temp.split(',')
        else:
            apps = []

def addApp(type_desc, extension):
    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=[(type_desc, extension), ("All files", "*.*")])
    if filename:
        if len(apps) > 0:
            apps[0] = filename
        else:
            apps.append(filename)
    show()

def open_file(path):
    if not os.path.isfile(path):
        messagebox.showerror("Error", "File does not exist.")
        return
    system = platform.system()
    if system == "Darwin":  # Darwin is the internal name for macOS 
        os.system(f'open "{path}"')
    elif system == "Windows":
        os.startfile(path)
    else:
        os.system(f'xdg-open "{path}"')

def showCSV():
    if apps and apps[0] != "":
        open_file(apps[0])
    else:
        messagebox.showinfo("Info", "No timetable file selected.")

def final():
    saveFile()
    root.destroy()
    if apps and apps[0] != "":
        attend_class(apps[0])
    else:
        print("No timetable file selected.")

def saveFile():
    with open('save.txt', 'w') as f:
        f.write(','.join(apps))

canvas = tk.Canvas(root, height=100, width=600, bg="#ccccff")
canvas.pack()

frame = tk.Frame(root, bg="#e6e6ff")
frame.place(relwidth=0.8, relheight=0.3, relx=0.1, rely=0.1)

CSV_File = tk.Button(root, text="Add Timetable", padx=5, pady=2, fg="white", bg="#263D42", command=lambda: addApp("CSV file", "*.csv"))
CSV_File.pack(pady=(10, 5))

CSV_check = tk.Button(root, text="Check CSV", padx=5, pady=2, fg="white", bg="#263D42", command=showCSV)
CSV_check.pack()

Proceed = tk.Button(root, text="Automate", padx=5, pady=2, fg="white", bg="#263D42", command=final)
Proceed.pack(pady=(10, 0))

def show():
    for widget in frame.winfo_children():
        widget.destroy()
    if not apps or apps[0] == "":
        info = tk.Label(frame, text="Please add a timetable", bg="red", fg="black")
        info.pack()
    else:
        for app in apps:
            label = tk.Label(frame, text=app, bg="#b3ffb3")
            label.pack()

show()
root.resizable(False, False)
root.mainloop()

saveFile()
