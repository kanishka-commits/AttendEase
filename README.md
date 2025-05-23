# AttendEase

A simple automation tool for managing and joining scheduled online classes.

## Features

* Automatically launches your online class links based on a timetable stored in a CSV file.  
* Optional email alerts can notify you when a class starts and you join.  
* Cross-platform support: works on macOS, Windows, and Linux.

## Setup

1. Ensure Python 3 is installed on your system.  
2. Prepare your timetable CSV file with class times and corresponding links for each weekday.

## Usage

* Run `AttendEase.py`.  
* Use the GUI to select your timetable CSV file.  
* Click **Automate** to start the script which will monitor the time and open your classes accordingly.

## CSV Format

* The first column must contain class start times in `HH:MM` format.  
* Columns 2 to 7 correspond to Monday through Sunday, with each cell containing the class link or `exit` if the schedule ends for that day.  
* The script skips past classes and exits if no more remain for the current day.

## Notes

* For best experience, be logged into Zoom (or your preferred platform) to avoid login prompts when the meeting opens.  
* Email notification code is included but disabled by default for privacy and simplicity—enable it by filling in your email credentials and uncommenting the related lines.  
* The app remembers your last timetable file selection for convenience.

## Future Plans

* Add support for more meeting platforms and enhanced scheduling options.  
* Implement more robust error handling and UI improvements.

