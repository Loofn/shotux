<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Shotux Screenshot Tool - Copilot Instructions

This is a Python desktop application for Linux screenshot capture with GUI support.

## Project Context
- **Language**: Python 3
- **GUI Framework**: Tkinter (built-in Python GUI library)
- **Image Processing**: PIL (Pillow)
- **Target Platform**: Linux (X11 and Wayland)
- **Architecture**: Modular design with separate managers for different concerns

## Key Components
1. **main.py** - Main GUI application using Tkinter
2. **src/screenshot_manager.py** - Handles screenshot capture using scrot and PIL
3. **src/config_manager.py** - Manages application configuration and settings
4. **src/hotkey_manager.py** - Global hotkey registration and handling
5. **shotux_cli.py** - Command-line interface for headless operation

## Coding Standards
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Include comprehensive docstrings for classes and methods
- Handle exceptions gracefully with user-friendly error messages
- Use pathlib for path operations when possible

## Dependencies and System Integration
- Uses `scrot` for screenshot capture (fallback to PIL ImageGrab)
- Uses `xclip` for clipboard operations
- Supports `xbindkeys` for global hotkeys
- Configuration stored in `~/.config/shotux/config.json`

## GUI Design Principles
- Clean, intuitive interface using Tkinter
- Responsive layout with proper grid management
- Status updates and user feedback
- Error handling with message boxes
- Threading for non-blocking operations

## Development Preferences
- Prefer system-native tools over heavy dependencies  
- Maintain compatibility across different Linux distributions
- Include proper cleanup for temporary files and processes
- Support both GUI and CLI usage patterns
- Configuration should be persistent and user-configurable

## Testing Considerations
- Test on different desktop environments (GNOME, KDE, XFCE)
- Verify hotkey functionality doesn't conflict with system shortcuts
- Ensure proper handling of missing system dependencies
- Test clipboard operations across different applications
