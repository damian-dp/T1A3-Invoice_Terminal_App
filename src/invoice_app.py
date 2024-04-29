import os
import csv
import subprocess
import datetime
from jinja2 import Template                 # type: ignore
from xhtml2pdf import pisa                  # type: ignore


def clear_terminal():
    # Clear terminal command for different operating systems
    clear_command = ""
    if os.name == "posix":  # Unix/Linux/MacOS
        clear_command = "clear"
    elif os.name == "nt":   # Windows
        clear_command = "cls"
    else:
        # Unsupported operating system
        print("Unsupported operating system. Terminal cannot be cleared.")
        return

    # Execute the clear command
    subprocess.run(clear_command, shell=True)


def main():
    clear_terminal()
    # Check onboarding status at the start of the main menu
    skip_onboarding()
    clear_terminal()
    
    while True:
        print("\n========== Invoice App Menu ==========")
        print("\n")
        
        print("1. Create a new invoice")
        print("2. View past invoices")
        print("3. View company profile")
        print("4. Exit")
        
        print("\n")
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            create_new_invoice()
        elif choice == '2':
            view_past_invoices()
        elif choice == '3':
            view_and_update_company_profile()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice, please enter 1, 2, 3, or 4.")