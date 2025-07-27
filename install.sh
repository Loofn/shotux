#!/bin/bash

# Shotux Installation Script
# Makes Shotux installable as a system package

set -e

echo "🚀 Installing Shotux Screenshot Tool..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Error: This tool is designed for Linux systems.${NC}"
    exit 1
fi

# Check for Python 3.8+
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null || echo "0.0")
required_version="3.8"

if [[ "$(echo -e "$python_version\n$required_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo -e "${RED}Error: Python 3.8 or higher is required. Found: $python_version${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $python_version found${NC}"

# Function to install system dependencies
install_system_deps() {
    echo -e "${BLUE}Installing system dependencies...${NC}"
    
    if command -v apt-get &> /dev/null; then
        echo "Detected APT package manager (Ubuntu/Debian)"
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-venv python3-tk scrot xclip xbindkeys
        
    elif command -v dnf &> /dev/null; then
        echo "Detected DNF package manager (Fedora/RHEL)"
        sudo dnf install -y python3-pip python3-tkinter scrot xclip xbindkeys
        
    elif command -v pacman &> /dev/null; then
        echo "Detected Pacman package manager (Arch Linux)"
        sudo pacman -S --noconfirm python-pip tk scrot xclip xbindkeys
        
    elif command -v zypper &> /dev/null; then
        echo "Detected Zypper package manager (openSUSE)"
        sudo zypper install -y python3-pip python3-tk scrot xclip xbindkeys
        
    else
        echo -e "${YELLOW}Warning: Could not detect package manager.${NC}"
        echo "Please manually install: python3-pip python3-tk scrot xclip xbindkeys"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Function to install Shotux
install_shotux() {
    echo -e "${BLUE}Installing Shotux...${NC}"
    
    # Install in user mode by default
    if [[ "$1" == "--system" ]]; then
        echo "Installing system-wide..."
        sudo pip3 install --upgrade .
    else
        echo "Installing for current user..."
        pip3 install --user --upgrade .
        
        # Add user bin to PATH if not already there
        USER_BIN="$HOME/.local/bin"
        if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
            echo -e "${YELLOW}Adding $USER_BIN to PATH${NC}"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
            echo "Please run: source ~/.bashrc"
        fi
    fi
}

# Function to create desktop integration
setup_desktop_integration() {
    echo -e "${BLUE}Setting up desktop integration...${NC}"
    
    # Install desktop file
    mkdir -p ~/.local/share/applications
    cp data/shotux.desktop ~/.local/share/applications/
    
    # Install icon
    mkdir -p ~/.local/share/pixmaps
    cp data/shotux.png ~/.local/share/pixmaps/ 2>/dev/null || echo "Icon file not found, skipping..."
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database ~/.local/share/applications/
    fi
    
    echo -e "${GREEN}✓ Desktop integration installed${NC}"
}

# Function to create uninstaller
create_uninstaller() {
    cat > ~/.local/bin/shotux-uninstall << 'EOF'
#!/bin/bash
echo "Uninstalling Shotux..."
pip3 uninstall shotux -y
rm -f ~/.local/share/applications/shotux.desktop
rm -f ~/.local/share/pixmaps/shotux.png
rm -f ~/.local/bin/shotux-uninstall
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
echo "✓ Shotux uninstalled successfully"
EOF
    chmod +x ~/.local/bin/shotux-uninstall
    echo -e "${GREEN}✓ Uninstaller created at ~/.local/bin/shotux-uninstall${NC}"
}

# Main installation process
main() {
    echo -e "${BLUE}Shotux Screenshot Tool Installer${NC}"
    echo "================================="
    
    # Check if we should install system dependencies
    if [[ "$1" == "--skip-deps" ]]; then
        echo -e "${YELLOW}Skipping system dependencies installation${NC}"
    else
        install_system_deps
    fi
    
    # Install Shotux
    install_shotux "$@"
    
    # Setup desktop integration
    setup_desktop_integration
    
    # Create uninstaller
    create_uninstaller
    
    echo ""
    echo -e "${GREEN}🎉 Installation complete!${NC}"
    echo ""
    echo "You can now run Shotux in the following ways:"
    echo -e "  ${BLUE}1. GUI mode:${NC} shotux-gui"
    echo -e "  ${BLUE}2. CLI mode:${NC} shotux-cli --help"
    echo -e "  ${BLUE}3. From applications menu:${NC} Search for 'Shotux'"
    echo ""
    echo -e "${YELLOW}Note: If commands are not found, restart your terminal or run:${NC}"
    echo "      source ~/.bashrc"
    echo ""
    echo -e "${BLUE}To uninstall:${NC} shotux-uninstall"
}

# Parse command line arguments
case "$1" in
    --help|-h)
        echo "Shotux Installation Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --system      Install system-wide (requires sudo)"
        echo "  --skip-deps   Skip system dependency installation"
        echo "  --help        Show this help message"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
