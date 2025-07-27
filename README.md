# Shotux - Screenshot Tool for Linux

A comprehensive screenshot application for Linux with GUI support, built using Python and Tkinter.

## Features

- **Multiple Capture Modes**
  - Full screen capture
  - Active window capture
  - Region selection capture

- **User-Friendly GUI**
  - Clean and intuitive interface
  - Configurable capture delay
  - Auto-save functionality
  - Copy to clipboard support

- **Flexible Configuration**
  - Customizable save directory
  - Multiple image formats support
  - Persistent settings

- **System Integration**
  - Global hotkeys support
  - Command-line interface
  - System tray integration (planned)

## Requirements

### System Dependencies
The following system packages need to be installed:

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip scrot xclip

# Fedora/RHEL
sudo dnf install python3 python3-pip scrot xclip

# Arch Linux
sudo pacman -S python python-pip scrot xclip
```

### Python Dependencies
Install Python dependencies using pip:

```bash
pip3 install -r requirements.txt
```

## Installation

### Method 1: Using the Installer (Recommended)
The easiest way to install Shotux:

```bash
git clone https://github.com/lofn/shotux.git
cd shotux
./install.sh
```

This will:
- Install system dependencies automatically
- Install Shotux for the current user
- Set up desktop integration
- Create an uninstaller

### Method 2: Using pip
If you have the system dependencies installed:

```bash
# Install system dependencies first:
sudo apt install python3-tk scrot xclip  # Ubuntu/Debian
# or
sudo dnf install python3-tkinter scrot xclip  # Fedora

# Then install Shotux:
pip install --user .
```

### Method 3: From Distribution Package
Download a pre-built package:

```bash
# Build the package
./build.sh

# Install from wheel
pip install dist/shotux-*.whl

# Or from source archive
pip install dist/shotux-*.tar.gz
```

### Method 4: Debian Package
For Debian/Ubuntu systems:

```bash
./build-deb.sh
sudo dpkg -i dist/shotux_*.deb
```

### Method 5: Development Installation
For development or testing:

```bash
pip install -e .  # Editable installation
```

## Uninstallation

- **If installed with installer**: Run `shotux-uninstall`
- **If installed with pip**: Run `pip uninstall shotux`
- **If installed as Debian package**: Run `sudo dpkg -r shotux`

## Usage

### 🎯 Quick Start

1. **Install with one command:**
   ```bash
   ./install.sh
   ```

2. **Start using:**
   ```bash
   shotux-gui      # Launch GUI
   shotux-cli --capture fullscreen  # Take screenshot via CLI
   ```

3. **Find in applications menu** or use global hotkeys when GUI is running

### GUI Mode
After installation, run:
```bash
shotux-gui
```
Or find "Shotux Screenshot Tool" in your applications menu.

### Command Line Mode
Use the CLI for automated screenshots:

```bash
# Full screen capture
shotux-cli --capture fullscreen

# Window capture with delay
shotux-cli --capture window --delay 3

# Region capture and copy to clipboard
shotux-cli --capture region --clipboard

# Save to specific file
shotux-cli --capture fullscreen --output ~/my_screenshot.png
```

### Global Hotkeys
When the application is running, you can use these hotkeys:

- **Print Screen** - Full screen capture
- **Alt + Print Screen** - Active window capture
- **Shift + Print Screen** - Region selection capture

## Configuration

The application stores its configuration in `~/.config/shotux/config.json`. You can modify settings through the GUI or by editing this file directly.

### Default Configuration
```json
{
  "delay": 0,
  "auto_save": false,
  "copy_clipboard": true,
  "save_directory": "~/Pictures/Screenshots",
  "image_format": "PNG",
  "image_quality": 95
}
```

## File Structure

```
Shotux/
├── shotux/                    # Main Python package
│   ├── __init__.py           # Package initialization
│   ├── main.py               # GUI application
│   ├── cli.py                # Command-line interface
│   ├── screenshot_manager.py # Screenshot capture logic
│   ├── hotkey_manager.py     # Global hotkey handling
│   └── config_manager.py     # Configuration management
├── data/
│   ├── shotux.desktop        # Desktop entry file
│   └── shotux.png            # Application icon
├── .github/
│   └── copilot-instructions.md # AI assistant instructions
├── install.sh                # Universal installer script
├── build.sh                  # Build distribution packages
├── build-deb.sh              # Build Debian package
├── setup.py                  # Python package configuration
├── requirements.txt          # Python dependencies
├── MANIFEST.in               # Package manifest
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## Development

### Adding New Features
1. For UI changes, modify `main.py`
2. For capture functionality, edit `src/screenshot_manager.py`
3. For configuration options, update `src/config_manager.py`

### Testing
Test the application on different Linux distributions and desktop environments:
- GNOME
- KDE Plasma
- XFCE
- i3/dwm

## Troubleshooting

### Common Issues

1. **"scrot: command not found"**
   - Install scrot: `sudo apt install scrot`

2. **"xclip: command not found"**
   - Install xclip: `sudo apt install xclip`

3. **Hotkeys not working**
   - Install xbindkeys: `sudo apt install xbindkeys`
   - Check if another application is using the same hotkeys

4. **Permission denied errors**
   - Make sure the application has read/write permissions to the save directory
   - Check if the temp directory is writable

### Wayland Support
This application is primarily designed for X11. For Wayland support:
- Use `grim` instead of `scrot` for screenshots
- Use `wl-clipboard` instead of `xclip` for clipboard operations

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Roadmap

- [ ] System tray integration
- [ ] More image formats support  
- [ ] Advanced editing features
- [ ] Wayland native support
- [ ] Plugin system
- [ ] OCR text extraction
- [ ] Cloud upload integration
