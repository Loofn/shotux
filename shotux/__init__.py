"""
Shotux - Screenshot Tool for Linux
A comprehensive screenshot application with GUI support.

This package provides both GUI and CLI interfaces for taking screenshots on Linux.
"""

__version__ = "1.0.0"
__author__ = "Shotux Developer"
__email__ = "developer@example.com"

from .main import ShotuxApp
from .screenshot_manager import ScreenshotManager
from .config_manager import ConfigManager
from .hotkey_manager import HotkeyManager

__all__ = [
    "ShotuxApp",
    "ScreenshotManager", 
    "ConfigManager",
    "HotkeyManager",
]
