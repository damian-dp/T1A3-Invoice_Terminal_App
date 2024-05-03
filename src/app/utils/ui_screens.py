import os
import re
import time
from colored import Fore, Back, Style     # type: ignore
from pyfiglet import Figlet               # type: ignore

def centre_align_text(text):
    # Function to remove ANSI escape sequences to get the visible length of the text
    def get_visible_length(text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return len(ansi_escape.sub('', text))
    
    # Get the terminal width
    terminal_width = os.get_terminal_size().columns
    # Calculate the visible length of the text
    visible_length = get_visible_length(text)
    # Calculate the padding needed
    padding = (terminal_width - visible_length) // 2
    # Apply padding and return centred text
    return ' ' * padding + text

def right_align_text(text):
    # Get the current width of the terminal
    terminal_width = os.get_terminal_size().columns
    # Calculate the right-aligned text by determining the needed spaces
    right_aligned_text = text.rjust(terminal_width)
    return right_aligned_text

def mixed_align_text(left_text, centre_text, right_text, left_colour, centre_colour, right_colour):
    # Get the current width of the terminal
    terminal_width = os.get_terminal_size().columns
    
    # Calculate the width for each part of the line
    quarter_width = terminal_width // 4
    half_width = terminal_width // 2
    
    # Format each part of the line with custom colours
    left_piece = f"{left_colour}{left_text.ljust(quarter_width)}{Style.reset}"
    centre_piece = f"{centre_colour}{centre_text.center(half_width)}{Style.reset}"
    right_piece = f"{right_colour}{right_text.rjust(quarter_width)}{Style.reset}"
    
    # Combine the parts into one line, ensuring alignment
    full_line = left_piece + centre_piece + right_piece

    print(full_line)
    
def centre_figlet_text(text, font='standard'):
    # Create a Figlet object with the specified font
    figlet = Figlet(font=font)
    
    # Generate figlet text
    figlet_text = figlet.renderText(text)
    
    # Get the terminal width
    terminal_width = os.get_terminal_size().columns
    
    # Centre each line of the figlet text
    centred_figlet_text = '\n'.join(line.center(terminal_width) for line in figlet_text.split('\n'))
    
    return centred_figlet_text

def print_full_width_line(color=Fore.WHITE):
    # Get the terminal width
    terminal_width = os.get_terminal_size().columns
    
    # Create the full-width line using the Unicode character '─'
    line = '─' * terminal_width
    
    # Apply color using the colored library
    colored_line = color + line + Style.RESET
    
    # Print the colored line
    print(colored_line)



# Screens

def onbaording_screen(company_name=None, company_email=None, company_phone=None, company_address=None, company_payment_details=None):
    mixed_align_text(
        "", "Onboarding", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n")
    
    # print(Figlet(font='big').renderText('NEW INVOICE'))
    print(centre_figlet_text("Welcome", 'big'))  #doh big
    
    print("\n")
    
    print(centre_align_text(f"To get started we need to create your company profile."))
    print('\n')
    print(centre_align_text(f"{Fore.dark_gray}This information will be used to populate invoices automatically with your {Style.reset}"))
    print(centre_align_text(f"{Fore.dark_gray}company details. You can edit your company profile anytime via the main menu.{Style.reset}"))

    print("\n\n\n")

    print(centre_align_text(f"{Fore.dark_gray}─────────────────────────────{Style.reset} Company Profile {Fore.dark_gray}─────────────────────────────{Style.reset}\n"))
    print(f"                        {Style.BOLD}{Fore.dark_gray}{'Company Name: '}{Style.reset}{company_name if company_name is not None else '':<21}     {Style.BOLD}{Fore.dark_gray}{'Company email: '}{Style.reset}{company_email if company_email is not None else '':<30}")
    print(f"                        {Style.BOLD}{Fore.dark_gray}{'Company Phone: '}{Style.reset}{company_phone if company_phone is not None else '':<20}     {Style.BOLD}{Fore.dark_gray}{'Company Address: '}{Style.reset}{company_address if company_address is not None else '':<30}")
    print(f"                        {Style.BOLD}{Fore.dark_gray}{'Payment Details: '}{Style.reset}{company_payment_details if company_payment_details is not None else '':<40}")
    print("\n\n")

    print_full_width_line(Fore.dark_gray)

def onboarding_success_screen():
    
    mixed_align_text(
        "", "Company Profile Created", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"{Fore.green}Company profile created successfully!{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"You can update your company profile"))
    print(centre_align_text(f"at any time via the main menu."))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Redirecting you to the main menu in 10 seconds..."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)

    time.sleep(10)

def onboarding_failure_screen(error_code=None):
    
    mixed_align_text(
        "", "Failed to Create Company Profile", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"{Fore.red}An error occurred while creating your company profile.{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"Failed to save company profile: {str(error_code)}"))
    print(centre_align_text(f"Please try again."))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Redirecting you to the main menu in 10 seconds..."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)

    time.sleep(10)



def main_menu_screen():
    mixed_align_text(
        "", "Main Menu", "Onboarding complete",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n")
    
    print(centre_figlet_text("INVOICE APP", 'big'))  #doh big
    
    print("\n")
    
    print(centre_align_text(f"{Style.BOLD}1) Create Invoice       2) View Past Invoices       3) View Company Profile{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Style.BOLD}{Fore.white}{Back.red}  4) Exit   {Style.reset}"))
    
    print("\n\n\n\n\n\n")
    
    print_full_width_line(Fore.dark_gray)

def exit_screen():
    
    mixed_align_text(
        "", "Exit App", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"You're about to close the app.{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Fore.white}{Back.red} Please confirm you would like to exit the app. {Style.reset}"))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Enter {Fore.red}'yes'{Style.reset} to exit or {Fore.green}'no'{Style.reset} to return to the main menu."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)


def create_invoice_screen_header():
    
    mixed_align_text(
        "", "Create New Invoice", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n")
    
    # print(Figlet(font='big').renderText('NEW INVOICE'))
    print(centre_figlet_text("NEW INVOICE", 'big'))  #doh big
    
def create_invoice_screen_body(customer_company_name=None, customer_contact_name=None, customer_phone=None, customer_email=None, customer_address=None, invoice_number=None, invoice_due=None, items=None):
    print(centre_align_text(f"{Fore.dark_gray}─────────────────────────{Style.reset} Customer Details {Fore.dark_gray}─────────────────────────{Style.reset}\n"))
    print(f"                            {Style.BOLD}{Fore.dark_gray}{'Customer Company: '}{Style.reset}{customer_company_name if customer_company_name is not None else '':<13}     {Style.BOLD}{Fore.dark_gray}{'Contact Name: '}{Style.reset}{customer_contact_name if customer_contact_name is not None else '':<30}")
    print(f"                            {Style.BOLD}{Fore.dark_gray}{'Customer Phone: '}{Style.reset}{customer_phone if customer_phone is not None else '':<15}     {Style.BOLD}{Fore.dark_gray}{'Contact Email: '}{Style.reset}{customer_email if customer_email is not None else '':<30}")
    print(f"                            {Style.BOLD}{Fore.dark_gray}{'Customer Address: '}{Style.reset}{customer_address if customer_address is not None else '':<30}")
    print("\n\n")

    print(centre_align_text(f"{Fore.dark_gray}─────────────────────────{Style.reset} Invoice Details {Fore.dark_gray}──────────────────────────{Style.reset}\n"))
    print(f"                            {Style.BOLD}{Fore.dark_gray}{'Invoice Number: '}{Style.reset}{invoice_number if invoice_number is not None else '':<15}     {Style.BOLD}{Fore.dark_gray}{'Due Date: '}{Style.reset}{invoice_due if invoice_due is not None else '':<30}")
    print("\n\n")

    print(centre_align_text(f"{Fore.dark_gray}──────────────────────────{Style.reset} Invoice Items {Fore.dark_gray}───────────────────────────{Style.reset}\n"))
    
    if items is None or not items:
        items = [{'name': '', 'price': ''}]
    for item in items:
        print(f"                            {Style.BOLD}{Fore.dark_gray}{'Item: '}{Style.reset}{item['name'] if item['name'] is not None else '':<25}     {Style.BOLD}{Fore.dark_gray}{'Price: '}{Style.reset}{item['price'] if item['price'] is not None else '':<30}")

    print("\n\n")
    print_full_width_line(Fore.dark_gray)

def export_success_screen(pdf_filename=None, return_menu="main"):
    
    mixed_align_text(
        "", "Export Successful", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"{Fore.green}Invoice created successfully!{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Fore.dark_gray}The PDF has been saved as {Style.reset}{Fore.green}{pdf_filename}{Style.reset}"))
    print(centre_align_text(f"{Fore.dark_gray}in the Invoice Exports folder.{Style.reset}"))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Returning you to the {return_menu} menu in 5 seconds..."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)

    time.sleep(8)
    
def export_failure_screen():
        
    mixed_align_text(
        "", "Export Failed", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"{Fore.red}An error occurred while creating the invoice.{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Fore.dark_gray}Please try to create the invoice again via the main menu.{Style.reset}"))
    print(centre_align_text(f"{Fore.dark_gray}If the issue continues please re-install the app and try again.{Style.reset}"))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Returning you to the main menu in 10 seconds..."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)

    time.sleep(10)



def past_invoice_screen_header():
    mixed_align_text(
        "", "Past Invoices", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n")
    
    # print(Figlet(font='big').renderText('NEW INVOICE'))
    print(centre_figlet_text("PAST INVOICES", 'big'))  #doh big
    
def deletion_success_screen():
    
    mixed_align_text(
        "", "Deletion Successful", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"{Fore.green}Invoice record deleted successfully!{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Style.reset}The Invoice record has been deleted.{Style.reset}"))
    print(centre_align_text(f"{Fore.dark_gray}You are no longer able to re-export or view this invoice.{Style.reset}"))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Returning you to the past invoice menu in 5 seconds..."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)

    time.sleep(8)

def no_past_invoices_screen():
    
    mixed_align_text(
        "", "No Past Invoices Found", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"{Fore.yellow}No past invoices found.{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Fore.dark_gray}You need to create a new invoice via the{Style.reset}"))
    print(centre_align_text(f"{Fore.dark_gray}main menu before you can manage them here.{Style.reset}"))
    
    print("\n\n\n\n\n\n\n\n\n\n")
    
    print(centre_align_text(f"Returning you to the main menu in 5 seconds..."))
    
    print("\n")

    print_full_width_line(Fore.dark_gray)

    time.sleep(8)



def profile_screen(company_name, company_email, company_phone, company_address, company_payment_details):
    mixed_align_text(
        "", "Company Profile", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n")
    
    # print(Figlet(font='big').renderText('NEW INVOICE'))
    print(centre_figlet_text("COMPANY PROFILE", 'big'))  #doh big
    
    print(centre_align_text(f"{Fore.dark_gray}─────────────────────────────{Style.reset} Company Profile {Fore.dark_gray}─────────────────────────────{Style.reset}\n"))
    print(f"                        {Style.BOLD}{Fore.dark_gray}{'1. Company Name: '}{Style.reset}{company_name if company_name is not None else '':<21}     {Style.BOLD}{Fore.dark_gray}{'2. Company email: '}{Style.reset}{company_email if company_email is not None else '':<30}")
    print(f"                        {Style.BOLD}{Fore.dark_gray}{'3. Company Phone: '}{Style.reset}{company_phone if company_phone is not None else '':<20}     {Style.BOLD}{Fore.dark_gray}{'4. Company Address: '}{Style.reset}{company_address if company_address is not None else '':<30}")
    print(f"                        {Style.BOLD}{Fore.dark_gray}{'5. Payment Details: '}{Style.reset}{company_payment_details if company_payment_details is not None else '':<40}")
    print("\n\n\n")

    print(centre_align_text(f"{Fore.dark_gray}Enter the number of the detail to update or type 'back'.{Style.reset}"))
    print("")
    print_full_width_line(Fore.dark_gray)