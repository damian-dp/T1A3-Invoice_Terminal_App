import os
import re
from colored import Fore, Back, Style, attr     # type: ignore
from pyfiglet import Figlet                     # type: ignore

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
def main_menu_screen():
    mixed_align_text(
        "", "Main Menu", "Onboarding complete",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    print_full_width_line(Fore.dark_gray)
    
    print("\n\n\n\n\n\n\n\n")
    
    print(centre_figlet_text("INVOICE APP", 'big'))  #doh big
    
    print("\n")
    
    print(centre_align_text(f"{Style.BOLD}{Fore.white}1) Create Invoice       2) View Past Invoices       3) View Company Profile{Style.reset}"))
    
    print("\n")
    
    print(centre_align_text(f"{Style.BOLD}{Fore.dark_gray}4) Exit       5) Help{Style.reset}"))
    
    print("\n\n\n\n\n\n")
    
    print_full_width_line(Fore.dark_gray)

def create_invoice_screen():
    
    mixed_align_text(
        "", "Create New Invoice", "",
        Fore.RED, Fore.white, Fore.dark_gray
    )
    
    print(Figlet(font='big').renderText('NEW INVOICE'))


def past_invoice_screen():
    pass

def profile_screen():
    pass

