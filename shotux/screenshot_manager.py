"""
Screenshot Manager Module
Handles all screenshot capture operations.
"""

import subprocess
import tempfile
import os
from PIL import Image, ImageGrab
from io import BytesIO
import tkinter as tk


class ScreenshotManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.temp_files = []
        
    def capture_fullscreen(self):
        """Capture full screen using available methods."""
        try:
            # Try using PIL ImageGrab first (works with X11)
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception:
            # Fallback to scrot command
            return self._capture_with_scrot("fullscreen")
            
    def capture_window(self):
        """Capture active window."""
        try:
            # Use scrot to capture active window
            return self._capture_with_scrot("window")
        except Exception as e:
            raise Exception(f"Failed to capture window: {str(e)}")
            
    def capture_region(self):
        """Capture selected region using scrot's selection mode."""
        try:
            return self._capture_with_scrot("region")
        except Exception as e:
            raise Exception(f"Failed to capture region: {str(e)}")
            
    def _capture_with_scrot(self, mode):
        """Capture screenshot using scrot command."""
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        
        try:
            if mode == "fullscreen":
                # Capture full screen
                cmd = ['scrot', temp_file.name]
            elif mode == "window":
                # Capture active window
                cmd = ['scrot', '-s', temp_file.name]
            elif mode == "region":
                # Capture selected region
                cmd = ['scrot', '-s', temp_file.name]
            else:
                raise ValueError(f"Unknown capture mode: {mode}")
                
            # Execute scrot command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                if "scrot: command not found" in result.stderr:
                    raise Exception("scrot is not installed. Please install it using: sudo apt install scrot")
                else:
                    raise Exception(f"scrot failed: {result.stderr}")
                    
            # Load the captured image
            if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
                screenshot = Image.open(temp_file.name)
                # Create a copy to avoid file handle issues
                screenshot_copy = screenshot.copy()
                screenshot.close()
                return screenshot_copy
            else:
                return None
                
        except subprocess.TimeoutExpired:
            raise Exception("Screenshot capture timed out")
        except FileNotFoundError:
            raise Exception("scrot is not installed. Please install it using: sudo apt install scrot")
        except Exception as e:
            raise Exception(f"Screenshot capture failed: {str(e)}")
            
    def copy_to_clipboard(self, image):
        """Copy image to clipboard using xclip."""
        try:
            # Save image to temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            image.save(temp_file.name, 'PNG')
            temp_file.close()
            self.temp_files.append(temp_file.name)
            
            # Copy to clipboard using xclip
            cmd = ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp_file.name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                if "xclip: command not found" in result.stderr:
                    raise Exception("xclip is not installed. Please install it using: sudo apt install xclip")
                else:
                    raise Exception(f"Failed to copy to clipboard: {result.stderr}")
                    
        except FileNotFoundError:
            raise Exception("xclip is not installed. Please install it using: sudo apt install xclip")
        except Exception as e:
            raise Exception(f"Failed to copy to clipboard: {str(e)}")
            
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception:
                pass  # Ignore cleanup errors
        self.temp_files.clear()
        
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.cleanup_temp_files()
