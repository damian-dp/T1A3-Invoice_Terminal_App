import os
import time
import csv
import subprocess
import curses
import datetime
import shutil
from jinja2 import Environment, FileSystemLoader      # type: ignore
from xhtml2pdf import pisa                            # type: ignore
from colored import Fore, Back, Style                 # type: ignore

from utils.ui_screens import *

COMPANY_PROFILE_PATH = '../src/data/company_profile.csv'
PAST_INVOICES_PATH = '../src/data/past_invoices.csv'


# Terminal Management Logic
def resize_terminal_window():
    # The command to resize the terminal window
    resize_command = 'printf "\\e[8;35;125t"'

    # Execute the resize command
    subprocess.run(resize_command, shell=True)

    # Initialize curses
    stdscr = curses.initscr()

    # Attempt to resize the terminal
    try:
        curses.resizeterm(35, 125)
    except curses.error:
        # The terminal size could not be changed
        pass

    # End curses
    curses.endwin()

def clear_terminal():
    clear_command = "clear" if os.name == "posix" else "cls" if os.name == "nt" else None
    if clear_command:
        subprocess.run(clear_command, shell=True)
    else:
        print("Unsupported operating system. Terminal cannot be cleared.")


# Onboarding Logic
def check_onboarding():
    if os.path.exists(COMPANY_PROFILE_PATH):
        print("Onboarding already completed.")
        with open(COMPANY_PROFILE_PATH, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return next(reader)
    else:
        return perform_onboarding()
    
def perform_onboarding():
    clear_terminal()
    
    onboarding_screen()
    company_name = input("Enter your company name: ")
    clear_terminal()
    
    onboarding_screen(company_name=company_name)
    company_email = input("Enter your company email: ")
    clear_terminal()
    
    onboarding_screen(company_name=company_name, company_email=company_email)
    company_phone = input("Enter your company phone number: ")
    clear_terminal()
    
    onboarding_screen(company_name=company_name, company_email=company_email, company_phone=company_phone)
    company_address = input("Enter your company address: ")
    clear_terminal()
    
    onboarding_screen(company_name=company_name, company_email=company_email, company_phone=company_phone, company_address=company_address)
    company_payment_details = input("Enter payment details and instructions that will be displayed on your invoices: ")
    
    # Check if the file exists
    if not os.path.isfile(COMPANY_PROFILE_PATH):
        # If not, create the directories leading to the file
        os.makedirs(os.path.dirname(COMPANY_PROFILE_PATH), exist_ok=True)

    try:
        with open(COMPANY_PROFILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name', 'Address', 'Phone', 'Email', 'Payment Details'])
            writer.writerow([company_name, company_address, company_phone, company_email, company_payment_details])
        
        clear_terminal()
        onboarding_success_screen()
        
    except IOError as e:
        clear_terminal()
        onboarding_failure_screen(error_code=e)


# Invoice Management Logic
def get_invoice_input():
    resize_terminal_window()
    time.sleep(0.5)
    clear_terminal()
    
    items = []

    create_invoice_screen_header()
    create_invoice_screen_body(items=items)
    customer_company_name = input("Enter customer company name: ")
    clear_terminal()
    
    create_invoice_screen_header()
    create_invoice_screen_body(customer_company_name=customer_company_name, items=items)
    customer_contact_name = input("Enter customer contact name: ")
    clear_terminal()
    
    create_invoice_screen_header()
    create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, items=items)
    customer_phone = input("Enter customer phone number: ")
    clear_terminal()
    
    create_invoice_screen_header()
    create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, items=items)
    customer_email = input("Enter customer email: ")
    clear_terminal()
    time.sleep(0.1)
    
    create_invoice_screen_header()
    create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, items=items)
    customer_address = input("Enter customer address: ")
    clear_terminal()
    time.sleep(0.1)
   
    create_invoice_screen_header()
    create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, customer_address=customer_address, items=items)
    invoice_number = input("Enter invoice number: ")
    clear_terminal()
    
    create_invoice_screen_header()
    create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, customer_address=customer_address, invoice_number=invoice_number, items=items)
    invoice_due = input("Enter invoice due date (DD/MM/YY): ")
    clear_terminal()
    
    while True:
        item = {'name': '', 'price': '', 'description': ''}
        create_invoice_screen_header()
        create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, customer_address=customer_address, invoice_number=invoice_number, invoice_due=invoice_due, items=items)
        item_name = input("Enter item name: ")
        clear_terminal()
        item['name'] = item_name
        items.append(item)  # Add the item to the items list

        create_invoice_screen_header()
        create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, customer_address=customer_address, invoice_number=invoice_number, invoice_due=invoice_due, items=items)
        item_description = input("Enter item description: ")
        clear_terminal()
        item['description'] = item_description
        items[-1] = item  # Update the last item in the items list

        while True:
            try:
                create_invoice_screen_header()
                create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, customer_address=customer_address, invoice_number=invoice_number, invoice_due=invoice_due, items=items)
                item_price = float(input("Enter item price: "))
                item['price'] = item_price
                items[-1] = item  # Update the last item in the items list
                break  # Exit the inner loop if the price is correctly entered
            except ValueError:
                print("Invalid price. Please enter a valid number.")

        create_invoice_screen_header()
        create_invoice_screen_body(customer_company_name=customer_company_name, customer_contact_name=customer_contact_name, customer_phone=customer_phone, customer_email=customer_email, customer_address=customer_address, invoice_number=invoice_number, invoice_due=invoice_due, items=items)
        continue_adding = input(f"{Fore.light_gray}Would you like to add another item? (yes/no): {Style.reset}")
        if continue_adding.lower() == 'yes':
            clear_terminal()  # Clear the terminal before adding another item
        else:
            break  # Exit the outer loop if the user is done adding items

    total_price = sum(item['price'] for item in items)
    return {
        'customer_company_name': customer_company_name,
        'customer_contact_name': customer_contact_name,
        'customer_phone': customer_phone,
        'customer_email': customer_email,
        'customer_address': customer_address,
        'invoice_number': invoice_number,
        'invoice_due': invoice_due,
        'items': items,
        'total_price': total_price
    }

def create_new_invoice():
    
    def read_company_profile():
        try:
            with open(COMPANY_PROFILE_PATH, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                return next(reader)  # Return the first row with actual data
        except FileNotFoundError:
            print("No company profile found. Please complete onboarding first.")
            return None
        except Exception as e:
            print(f"Failed to read company profile: {str(e)}")
            return None     
    
    company_profile = read_company_profile()
    
    if company_profile is None:
        perform_onboarding()
        company_profile = read_company_profile()

    invoice_data = get_invoice_input()
    
    customer_company_name = invoice_data['customer_company_name']
    customer_contact_name = invoice_data['customer_contact_name']
    customer_phone = invoice_data['customer_phone']
    customer_email = invoice_data['customer_email']
    customer_address = invoice_data['customer_address']
    invoice_number = invoice_data['invoice_number']
    invoice_due = invoice_data['invoice_due']
    items = invoice_data['items']
    total_price = sum(item['price'] for item in items)
        
    company_name, company_address, company_phone, company_email, company_payment_details = read_company_profile()
                
    html_content = generate_html_invoice(
        company_name, company_address, company_phone, company_email, company_payment_details,
        customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address,
        invoice_number, invoice_due, items, total_price
    )
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_company_name = "".join(c for c in customer_company_name if c.isalnum() or c in (' ', '_')).rstrip()
    pdf_filename = f"{invoice_number}_{safe_company_name}_{current_date}.pdf"
    
    save_html_to_file("temp_invoice.html", html_content)

    
    if convert_html_to_pdf("temp_invoice.html", pdf_filename):
        save_invoice_record(customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items, total_price)
        clear_terminal()
        export_success_screen(pdf_filename=pdf_filename)
    else:
        clear_terminal()
        export_failure_screen()
    
    return pdf_filename

def generate_html_invoice(company_name, company_address, company_phone, company_email, company_payment_details, customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items, total_price):
    # Get the absolute path of the directory where the script is located
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Set up the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader(os.path.join(dir_path, 'utils/html_templates')))
    template = env.get_template('invoice_template.html')

    return template.render(
        company_name=company_name,
        company_address=company_address,
        company_phone=company_phone,
        company_email=company_email,
        company_payment_details=company_payment_details,
        customer_company_name=customer_company_name,
        customer_contact_name=customer_contact_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        customer_address=customer_address,
        invoice_number=invoice_number,
        invoice_due=invoice_due,
        items=items,
        total_price=total_price
    )

def save_html_to_file(html_filename, html_content):
    # Check if the directory exists, if not, create it
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Join the temp directory with the HTML filename
    html_path = os.path.join(temp_dir, html_filename)

    with open(html_path, "w") as html_file:
        html_file.write(html_content)

    return html_path  # Return the full path to the HTML file

def convert_html_to_pdf(html_filename, pdf_filename):
    try:
        # Save the HTML content to a file in the temp directory
        html_path = os.path.join("temp", html_filename)

        # Check if the directory exists, if not, create it
        output_dir = os.path.join("..", "src", "Invoice Exports")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Join the output directory with the PDF filename
        pdf_path = os.path.join(output_dir, pdf_filename)

        with open(html_path, "r") as html_file, open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_file, dest=pdf_file)
            return pisa_status.err == 0
    except Exception as e:
        print(f"Error during PDF conversion: {str(e)}")
        return False
    finally:
        # Remove the temp directory and all its contents
        shutil.rmtree("temp")
        
def save_invoice_record(customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items, total_price):
    file_exists = os.path.isfile(PAST_INVOICES_PATH)
    
    with open(PAST_INVOICES_PATH, 'a', newline='') as csvfile:
        fieldnames = ['Invoice Number', 'Customer Company Name', 'Customer Contact Name', 'Customer Phone', 'Customer Email', 'Customer Address', 'Invoice Due Date', 'Items', 'Total Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
                
        writer.writerow({
            'Invoice Number': str(invoice_number),  # Convert to string
            'Customer Company Name': customer_company_name,
            'Customer Contact Name': customer_contact_name,
            'Customer Phone': customer_phone,
            'Customer Email': customer_email,
            'Customer Address': customer_address,
            'Invoice Due Date': invoice_due,
            'Items': "; ".join([f"{item['name']}: {item['description']}: {item['price']}" for item in items]),
            'Total Price': total_price
        })

def view_past_invoices():
    while True:
        clear_terminal()
        try:
            with open(PAST_INVOICES_PATH, 'r') as file:
                reader = csv.DictReader(file)
                invoices = list(reader)
                
                past_invoice_screen_header()
                
                for idx, row in enumerate(invoices):
                    print(f"{Style.BOLD}                               {idx + 1}.{Style.reset}  INV# {Fore.dark_gray}{row['Invoice Number']:<10}    {Style.reset}Customer: {Fore.dark_gray}{row['Customer Company Name']:<15}  {Style.reset}Due: {Fore.dark_gray}{row['Invoice Due Date']}")
                    print(f"{Fore.dark_gray}                               ───────────────────────────────────────────────────────────────{Style.reset}")

            num_invoices = len(invoices)
            if num_invoices == 1:
                print("\n" * 7)
            elif num_invoices == 2:
                print("\n" * 4)
                print("")
            elif num_invoices == 3:
                print("\n" * 3)
            elif num_invoices == 4:
                print("\n")
            elif num_invoices == 5:
                print("")
            else:
                print("")

            print(centre_align_text(f"{Fore.dark_gray}Enter the line number of the invoice you would like to manage.{Style.reset}"))
            
            if num_invoices <= 4:
                print("")
            elif num_invoices == 5:
                pass
            else:
                print("")
            
            print_full_width_line(Fore.dark_gray)
            
            choice = input("Line number or 'back': ")
            
            if choice.lower() == 'back':
                return
            else:
                invoice_index = int(choice) - 1  # Adjusting for zero-based indexing
                if 0 <= invoice_index < len(invoices):
                    
                    with open(PAST_INVOICES_PATH, 'r') as file:
                        reader = csv.DictReader(file)
                        invoices = list(reader)
                        
                        past_invoice_screen_header()
                        
                        for idx, row in enumerate(invoices):
                            print(f"{Style.BOLD}                               {idx + 1}.{Style.reset}  INV# {Fore.dark_gray}{row['Invoice Number']:<10}    {Style.reset}Customer: {Fore.dark_gray}{row['Customer Company Name']:<15}  {Style.reset}Due: {Fore.dark_gray}{row['Invoice Due Date']}")
                            print(f"{Fore.dark_gray}                               ───────────────────────────────────────────────────────────────{Style.reset}")

                    num_invoices = len(invoices)
                    if num_invoices == 1:
                        print("\n" * 7)
                    elif num_invoices == 2:
                        print("\n" * 4)
                        print("")
                    elif num_invoices == 3:
                        print("\n" * 3)
                    elif num_invoices == 4:
                        print("\n")
                    elif num_invoices == 5:
                        print("")
                    else:
                        print("")

                    print(centre_align_text(f"Line number {Fore.light_gray}{choice}. {Style.reset}selected. Enter {Fore.red}1 to delete{Style.reset} or {Fore.green}2 to re-export.{Style.reset}"))
                    
                    if num_invoices <= 4:
                        print("")
                    elif num_invoices == 5:
                        pass
                    else:
                        print("")
                    
                    print_full_width_line(Fore.dark_gray)

                    action_choice = input("Choose an action (1-2): ")
                    
                    if action_choice == '1':
                        with open(PAST_INVOICES_PATH, 'r') as file:
                            reader = csv.DictReader(file)
                            invoices = list(reader)
                            
                            past_invoice_screen_header()
                            
                            for idx, row in enumerate(invoices):
                                print(f"{Style.BOLD}                               {idx + 1}.{Style.reset}  INV# {Fore.dark_gray}{row['Invoice Number']:<10}    {Style.reset}Customer: {Fore.dark_gray}{row['Customer Company Name']:<15}  {Style.reset}Due: {Fore.dark_gray}{row['Invoice Due Date']}")
                                print(f"{Fore.dark_gray}                               ───────────────────────────────────────────────────────────────{Style.reset}")

                        num_invoices = len(invoices)
                        if num_invoices == 1:
                            print("\n" * 7)
                        elif num_invoices == 2:
                            print("\n" * 4)
                            print("")
                        elif num_invoices == 3:
                            print("\n" * 3)
                        elif num_invoices == 4:
                            print("\n")
                        elif num_invoices == 5:
                            print("")
                        else:
                            print("")

                        print(centre_align_text(f"{Style.BOLD}{Back.red}{Fore.white}You're about to DELETE an invoice. (Line number {choice}.){Style.reset}"))
                        
                        if num_invoices <= 4:
                            print("")
                        elif num_invoices == 5:
                            pass
                        else:
                            print("")
                        
                        print_full_width_line(Fore.dark_gray)
                        
                        confirm = input(f"Are you sure you want to delete this invoice? ({Fore.red}yes{Style.reset}/{Fore.green}no{Style.reset}): ")
                        if confirm.lower() == 'yes':
                            clear_terminal()
                            delete_invoice_record(invoices[invoice_index]['Invoice Number'])
                            deletion_success_screen()
                        else:
                            print("Deletion cancelled.")
                    elif action_choice == '2':
                        re_export_to_pdf(invoices[invoice_index])
                        export_success_screen(pdf_filename=f"re_export_{invoices[invoice_index]['Invoice Number']}.pdf", return_menu="past invoices")
                    else:
                        print("Invalid choice.")
                else:
                    print("Invalid choice.")
        except FileNotFoundError:
            clear_terminal()
            no_past_invoices_screen()
            break 
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def re_export_to_pdf(invoice):
    try:
        items = []
        total_price = 0.0  # Initialize total_price
        item_details = invoice['Items'].split('; ')
        for item in item_details:
            item_components = item.split(': ')
            item_name = item_components[0]
            item_description = ': '.join(item_components[1:-1])  # Avoid including the price in the description
            item_price = float(item_components[-1])  # Last component is the price
            items.append({'name': item_name, 'description': item_description, 'price': item_price})
            total_price += item_price  # Add the item price to the total price
        
        
        def read_company_profile():
            try:
                with open(COMPANY_PROFILE_PATH, 'r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    return next(reader)  # Return the first row with actual data
            except FileNotFoundError:
                print("No company profile found. Please complete onboarding first.")
                return None
            except Exception as e:
                print(f"Failed to read company profile: {str(e)}")
                return None     
            
        company_name, company_address, company_phone, company_email, company_payment_details = read_company_profile()
        
        html_content = generate_html_invoice(
            company_name=company_name,
            company_address=company_address,
            company_phone=company_phone,
            company_email=company_email,
            company_payment_details=company_payment_details,
            customer_company_name=invoice['Customer Company Name'],
            customer_contact_name=invoice['Customer Contact Name'],
            customer_phone=invoice['Customer Phone'],
            customer_email=invoice['Customer Email'],
            customer_address=invoice['Customer Address'],
            invoice_number=invoice['Invoice Number'],
            invoice_due=invoice['Invoice Due Date'],
            items=items,
            total_price=total_price  # Pass total_price to create_html_invoice
        )
        
        # Create the Invoice Exports directory if it doesn't exist
        output_dir = "Invoice Exports"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directory created: {output_dir}")

        html_filename = f"temp_{invoice['Invoice Number']}.html"
        pdf_filename = f"re_export_{invoice['Invoice Number']}.pdf"
        
        # Save the HTML content to file in the root directory
        save_html_to_file(html_filename, html_content)
        
        # Correctly use paths based on how the convert_html_to_pdf handles paths
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        print(f"HTML path: {html_filename}")  # Debug print
        print(f"PDF path: {pdf_path}")    # Debug print
        
        # Correcting the PDF path input to match the internal handling in convert_html_to_pdf
        if convert_html_to_pdf(html_filename, pdf_filename):  # Pass filenames only if that's how convert_html_to_pdf expects it
            print(f"PDF exported successfully: {pdf_path}")
        else:
            print("PDF export failed.")

    except Exception as e:
        print(f"An error occurred during PDF export: {str(e)}")

def delete_invoice_record(invoice_number):
    try:
        with open(PAST_INVOICES_PATH, 'r') as file:
            invoices = list(csv.DictReader(file))
        
        with open(PAST_INVOICES_PATH, 'w', newline='') as file:
            fieldnames = invoices[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for invoice in invoices:
                if invoice['Invoice Number'] != invoice_number:
                    writer.writerow(invoice)
                    
        print("Invoice deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the invoice: {str(e)}")


# Company Profile Management Logic
def view_and_update_company_profile():
        
    # Check if the company profile file exists
    if not os.path.exists(COMPANY_PROFILE_PATH):
        print("No company profile found. Please create a new one.")
        perform_onboarding()

    # Reading the current company profile data
    try:
        with open(COMPANY_PROFILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            company_data = next(reader)  # Get the current data as a dictionary
    
    except FileNotFoundError:
        print("No company profile found. Restart application to create a new one.")
    
    except Exception as e:
        print(f"Error reading the file: {str(e)}")
        return

    
    # Extract the fields from the company data
    company_name = company_data['Company Name']
    company_email = company_data['Email']
    company_phone = company_data['Phone']
    company_address = company_data['Address']
    company_payment_details = company_data['Payment Details']

    # Call the profile_screen function with the extracted fields
    profile_screen(company_name, company_email, company_phone, company_address, company_payment_details)

    fieldnames = company_data.keys()

    # Interactive update of company details
    while True:
        user_input = input("Enter detail number or 'back': ")
        if user_input.lower() == 'back':
            break

        # Validate input and update data
        if user_input.isdigit():
            choice_index = int(user_input) - 1  # Convert to zero-based index
            if 0 <= choice_index < len(fieldnames):
                key_to_update = list(fieldnames)[choice_index]
                clear_terminal()
                profile_screen(company_name, company_email, company_phone, company_address, company_payment_details)
                new_value = input(f"Enter new value for {key_to_update}: ")
                company_data[key_to_update] = new_value

                # Update the corresponding variable
                if key_to_update == 'Company Name':
                    company_name = new_value
                elif key_to_update == 'Company Email':
                    company_email = new_value
                elif key_to_update == 'Company Phone':
                    company_phone = new_value
                elif key_to_update == 'Company Address':
                    company_address = new_value
                elif key_to_update == 'Payment Details':
                    company_payment_details = new_value

                clear_terminal()
                profile_screen(company_name, company_email, company_phone, company_address, company_payment_details)
            else:
                clear_terminal()
                profile_screen(company_name, company_email, company_phone, company_address, company_payment_details)
                print("Invalid number, please enter a valid number or type 'back'.")
        else:
            clear_terminal()
            profile_screen(company_name, company_email, company_phone, company_address, company_payment_details)
            print("Please enter a number or type 'back'.")

    # Write the updated details back to the CSV file
    try:
        with open(COMPANY_PROFILE_PATH, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(company_data)
        print("\nCompany profile updated successfully.")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
       
       
# Main Application Logic
def main_app():
    # Check onboarding status at the start of the app
    clear_terminal()
    check_onboarding()

    # Menu loop
    while True:
        main_menu_screen()
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            create_new_invoice()
        elif choice == '2':
            view_past_invoices()
        elif choice == '3':
            view_and_update_company_profile()
        elif choice == '4':
            clear_terminal()
            exit_screen()
            
            confirm = input("Would you like to exit? (yes/no): ")
            
            if confirm.lower() == 'yes':
                clear_terminal()
                # Add execute permissions to the shut_down.sh script
                subprocess.run(['chmod', '+x', 'scripts/shut_down.sh'])

                # Call the shell script to deactivate and delete the virtual environment
                subprocess.run(['bash', 'scripts/shut_down.sh'])

                break
            
            elif confirm.lower() == 'no':
                clear_terminal()
                main_menu_screen()
                
            else:
                print("Invalid choice, please enter 'yes' or 'no'.")
            
        else:
            print("Invalid choice, please enter 1, 2, 3, or 4.")       
 
 
# Application entry point
if __name__ == "__main__":
    main_app()