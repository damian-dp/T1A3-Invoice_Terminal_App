#!/bin/bash

# Desired dimensions
HEIGHT=35
WIDTH=125

# Function to resize using 'resize' command
resize_terminal() {
  if command -v resize >/dev/null; then
    resize -s $HEIGHT $WIDTH
    return 0
  fi
  return 1
}

# Function to resize using 'printf' with escape sequences
printf_resize() {
  if printf '\e[8;%d;%dt' $HEIGHT $WIDTH; then
    return 0
  fi
  return 1
}

# Function to resize using 'echo' for xterm-compatible terminals
xterm_resize() {
  if echo -ne "\033[8;${HEIGHT};${WIDTH}t"; then
    return 0
  fi
  return 1
}

# Try to resize terminal using different methods
if ! resize_terminal && ! printf_resize && ! xterm_resize; then
  echo "Failed to resize terminal. Please manually resize your window if you can not see all the content."
fi

clear
 
# Make the check_python.sh script executable
chmod +x scripts/check_python.sh

# Run the check python script
scripts/check_python.sh