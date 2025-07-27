#!/bin/bash

# Shotux Setup Script
# Installs system dependencies for Linux screenshot tool

echo "Setting up Shotux Screenshot Tool..."

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: This tool is designed for Linux systems."
    exit 1
fi

# Detect package manager and install dependencies
if command -v apt-get &> /dev/null; then
    echo "Detected APT package manager (Ubuntu/Debian)"
    echo "Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv scrot xclip xbindkeys
    
elif command -v dnf &> /dev/null; then
    echo "Detected DNF package manager (Fedora/RHEL)"
    echo "Installing system dependencies..."
    sudo dnf install -y python3 python3-pip scrot xclip xbindkeys
    
elif command -v pacman &> /dev/null; then
    echo "Detected Pacman package manager (Arch Linux)"
    echo "Installing system dependencies..."
    sudo pacman -S --noconfirm python python-pip scrot xclip xbindkeys
    
elif command -v zypper &> /dev/null; then
    echo "Detected Zypper package manager (openSUSE)"
    echo "Installing system dependencies..."
    sudo zypper install -y python3 python3-pip scrot xclip xbindkeys
    
else
    echo "Warning: Could not detect package manager."
    echo "Please manually install the following packages:"
    echo "  - python3 and python3-pip"
    echo "  - scrot (for screenshot capture)"
    echo "  - xclip (for clipboard support)"
    echo "  - xbindkeys (for global hotkeys)"
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install Python dependencies
echo "Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
echo "Making scripts executable..."
chmod +x main.py
chmod +x shotux_cli.py

# Create desktop entry
echo "Creating desktop entry..."
cat > ~/.local/share/applications/shotux.desktop << EOF
[Desktop Entry]
Name=Shotux Screenshot Tool
Comment=Screenshot tool for Linux with GUI
Exec=$(pwd)/.venv/bin/python $(pwd)/main.py
Icon=applets-screenshooter
Terminal=false
Type=Application
Categories=Graphics;Photography;
EOF

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications/
fi

echo ""
echo "Setup complete! 🎉"
echo ""
echo "You can now run Shotux in the following ways:"
echo "  1. GUI mode: python3 main.py"
echo "  2. CLI mode: python3 shotux_cli.py --help"
echo "  3. From applications menu: Search for 'Shotux'"
echo ""
echo "Note: Make sure you have X11 running for full functionality."
echo "      For Wayland, some features may have limited support."
