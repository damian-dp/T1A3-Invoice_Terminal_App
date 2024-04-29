import os
import csv
import subprocess
import datetime
from jinja2 import Template                 # type: ignore
from xhtml2pdf import pisa                  # type: ignore

COMPANY_PROFILE_PATH = 'util/data/company_profile.csv'
PAST_INVOICES_PATH = 'util/data/past_invoices.csv'

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
            
def skip_onboarding():
    if os.path.exists(COMPANY_PROFILE_PATH):
        print("Onboarding already completed.")
        with open(COMPANY_PROFILE_PATH, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return next(reader)
    else:
        return onboarding()
    
def onboarding():
    company_name = input("Enter your company name: ")
    company_address = input("Enter your company address: ")
    company_phone = input("Enter your company phone number: ")
    company_email = input("Enter your company email: ")
    company_payment_details = input("Enter payment details and instructions that will be displayed on your invoices: ")
    
    try:
        with open(COMPANY_PROFILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name', 'Address', 'Phone', 'Email', 'Payment Details'])
            writer.writerow([company_name, company_address, company_phone, company_email, company_payment_details])
        
        print("Company profile saved.")
        
    except IOError as e:
        print(f"Failed to save company profile: {str(e)}")   
        
def collect_input_invoice():
    clear_terminal()
    print("\n========== Customer Details ==========")
    customer_company_name = input("Enter customer company name: ")
    customer_contact_name = input("Enter customer contact name: ")
    customer_phone = input("Enter customer phone number: ")
    customer_email = input("Enter customer email: ")
    customer_address = input("Enter customer address: ")
    
    print("\n========== Invoice Details ==========")
    invoice_number = input("Enter invoice number: ")
    invoice_due = input("Enter invoice due date (DD/MM/YY): ")

    print("\n========== Invoice Items ==========")
    items = []
    while True:
        print("\nItem details:")
        item_name = input("Enter item name (or 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        item_description = input("Enter item description: ")
        try:
            item_price = float(input("Enter item price: "))
        except ValueError:
            print("Invalid price. Please enter a valid number.")
            continue
        items.append({'name': item_name, 'description': item_description, 'price': item_price})
    
    return customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items

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

def create_new_invoice():
    
    company_profile = read_company_profile()
    
    if company_profile is None:
        onboarding()
        company_profile = read_company_profile()

        
    company_name, company_address, company_phone, company_email, company_payment_details = read_company_profile()
            
    customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items = collect_input_invoice()
    
    html_content = create_html_invoice(
        company_name, company_address, company_phone, company_email, company_payment_details,
        customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address,
        invoice_number, invoice_due, items
    )
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_company_name = "".join(c for c in customer_company_name if c.isalnum() or c in (' ', '_')).rstrip()
    pdf_filename = f"{invoice_number}_{safe_company_name}_{current_date}.pdf"
    
    save_html_to_file("temp_invoice.html", html_content)
    
    if convert_html_to_pdf("temp_invoice.html", pdf_filename):
        print(f"\nInvoice created successfully! The PDF has been saved as {pdf_filename}")
        save_invoice_record(customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items)
    else:
        print("\nFailed to create PDF. Check the HTML file for errors.")

def create_html_invoice(company_name, company_address, company_phone, company_email, company_payment_details, customer_company_name, customer_contact_name, customer_phone, customer_email, customer_address, invoice_number, invoice_due, items):
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice</title>
        <style>
            /* Add your CSS styles here */
            /* Example: body { font-family: Arial, sans-serif; } */
        </style>
    </head>
    <body>
        <div class="invoice">
            <h1>{{ invoice_number }} Invoice. Due {{ invoice_due }}</h1>
            <p>From: {{ company_name }}</p>
            <p>{{ company_address }}</p>
            <p>{{ company_phone }}</p>
            <p>{{ company_email }}</p>
            <p>{{ company_payment_details }}</p>

            <p>To: {{ customer_company_name }}</p>
            <p>{{ customer_contact_name }}</p>
            <p>{{ customer_phone }}</p>
            <p>{{ customer_email }}</p>
            <p>{{ customer_address }}</p>

            <table>
                <tr>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Price</th>
                </tr>
                {% for item in items %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.description }}</td>
                    <td>${{ item.price }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """)
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
        items=items
    )

def save_html_to_file(html_filename, html_content):
    with open(html_filename, "w") as html_file:
        html_file.write(html_content)

def convert_html_to_pdf(html_filename, pdf_filename):
    try:
        # Check if the directory exists, if not, create it
        output_dir = "Invoice Exports"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Join the output directory with the PDF filename
        pdf_path = os.path.join(output_dir, pdf_filename)

        with open(html_filename, "r") as html_file, open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_file, dest=pdf_file)
            return pisa_status.err == 0
    except Exception as e:
        print(f"Error during PDF conversion: {str(e)}")
        return False
    finally:
        os.remove(html_filename)