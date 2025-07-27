#!/usr/bin/env python3
"""
Shotux - Screenshot Tool for Linux
A comprehensive screenshot application with GUI support.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from datetime import datetime
import threading
import time

from .screenshot_manager import ScreenshotManager
from .hotkey_manager import HotkeyManager
from .config_manager import ConfigManager


class ShotuxApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shotux - Screenshot Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.screenshot_manager = ScreenshotManager(self.config_manager)
        self.hotkey_manager = HotkeyManager(self.screenshot_manager)
        
        # Initialize UI
        self.setup_ui()
        self.setup_hotkeys()
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the application window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Set up the main user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Shotux Screenshot Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Screenshot modes frame
        modes_frame = ttk.LabelFrame(main_frame, text="Screenshot Modes", padding="10")
        modes_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        modes_frame.columnconfigure(0, weight=1)
        
        # Mode buttons
        self.create_mode_buttons(modes_frame)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create options
        self.create_options(options_frame)
        
        # Actions frame
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        actions_frame.columnconfigure(0, weight=1)
        
        # Action buttons
        self.create_action_buttons(actions_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_mode_buttons(self, parent):
        """Create screenshot mode buttons."""
        # Full screen button
        fullscreen_btn = ttk.Button(parent, text="📺 Full Screen", 
                                   command=self.capture_fullscreen,
                                   width=20)
        fullscreen_btn.grid(row=0, column=0, padx=(0, 5), pady=2, sticky=tk.W+tk.E)
        
        # Active window button
        window_btn = ttk.Button(parent, text="🖼️ Active Window", 
                               command=self.capture_window,
                               width=20)
        window_btn.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W+tk.E)
        
        # Region selection button
        region_btn = ttk.Button(parent, text="✂️ Select Region", 
                               command=self.capture_region,
                               width=20)
        region_btn.grid(row=0, column=2, padx=(5, 0), pady=2, sticky=tk.W+tk.E)
        
        # Configure column weights
        for i in range(3):
            parent.columnconfigure(i, weight=1)
            
    def create_options(self, parent):
        """Create option controls."""
        # Delay option
        ttk.Label(parent, text="Delay (seconds):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.delay_var = tk.StringVar(value=str(self.config_manager.get('delay', 0)))
        delay_spinbox = ttk.Spinbox(parent, from_=0, to=10, width=5, 
                                   textvariable=self.delay_var)
        delay_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Auto-save option
        self.auto_save_var = tk.BooleanVar(value=self.config_manager.get('auto_save', False))
        auto_save_check = ttk.Checkbutton(parent, text="Auto-save screenshots", 
                                         variable=self.auto_save_var)
        auto_save_check.grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        # Copy to clipboard option
        self.copy_clipboard_var = tk.BooleanVar(value=self.config_manager.get('copy_clipboard', True))
        clipboard_check = ttk.Checkbutton(parent, text="Copy to clipboard", 
                                         variable=self.copy_clipboard_var)
        clipboard_check.grid(row=0, column=3, sticky=tk.W)
        
        # Save directory
        ttk.Label(parent, text="Save Directory:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.save_dir_var = tk.StringVar(value=self.config_manager.get('save_directory', 
                                                                      os.path.expanduser('~/Pictures/Screenshots')))
        save_dir_entry = ttk.Entry(parent, textvariable=self.save_dir_var, width=40)
        save_dir_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), 
                           pady=(10, 0), padx=(0, 5))
        
        browse_btn = ttk.Button(parent, text="Browse...", command=self.browse_directory)
        browse_btn.grid(row=1, column=3, pady=(10, 0))
        
        # Configure column weights
        parent.columnconfigure(1, weight=1)
        
    def create_action_buttons(self, parent):
        """Create action buttons."""
        # Settings button
        settings_btn = ttk.Button(parent, text="⚙️ Settings", command=self.open_settings)
        settings_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Help button
        help_btn = ttk.Button(parent, text="❓ Help", command=self.show_help)
        help_btn.grid(row=0, column=1, padx=5)
        
        # Minimize to tray button
        minimize_btn = ttk.Button(parent, text="🔽 Minimize to Tray", command=self.minimize_to_tray)
        minimize_btn.grid(row=0, column=2, padx=5)
        
        # Exit button
        exit_btn = ttk.Button(parent, text="❌ Exit", command=self.on_closing)
        exit_btn.grid(row=0, column=3, padx=(5, 0))
        
    def setup_hotkeys(self):
        """Set up global hotkeys."""
        try:
            self.hotkey_manager.setup_hotkeys()
            self.update_status("Hotkeys registered successfully")
        except Exception as e:
            self.update_status(f"Warning: Could not register hotkeys - {str(e)}")
            
    def update_status(self, message):
        """Update the status bar."""
        self.status_var.set(message)
        self.root.update_idletasks()
        
        # Clear status after 3 seconds
        def clear_status():
            time.sleep(3)
            self.status_var.set("Ready")
            
        threading.Thread(target=clear_status, daemon=True).start()
        
    def capture_fullscreen(self):
        """Capture full screen screenshot."""
        self.update_status("Capturing full screen...")
        delay = int(self.delay_var.get())
        
        def capture():
            try:
                if delay > 0:
                    self.root.withdraw()  # Hide window during capture
                    time.sleep(delay)
                    
                screenshot = self.screenshot_manager.capture_fullscreen()
                self.process_screenshot(screenshot)
                
                if delay > 0:
                    self.root.deiconify()  # Show window again
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to capture screenshot: {str(e)}")
                if delay > 0:
                    self.root.deiconify()
                    
        threading.Thread(target=capture, daemon=True).start()
        
    def capture_window(self):
        """Capture active window screenshot."""
        self.update_status("Capturing active window...")
        delay = int(self.delay_var.get())
        
        def capture():
            try:
                if delay > 0:
                    time.sleep(delay)
                    
                screenshot = self.screenshot_manager.capture_window()
                self.process_screenshot(screenshot)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to capture window: {str(e)}")
                
        threading.Thread(target=capture, daemon=True).start()
        
    def capture_region(self):
        """Capture selected region screenshot."""
        self.update_status("Select region to capture...")
        delay = int(self.delay_var.get())
        
        def capture():
            try:
                if delay > 0:
                    time.sleep(delay)
                    
                screenshot = self.screenshot_manager.capture_region()
                if screenshot:
                    self.process_screenshot(screenshot)
                else:
                    self.update_status("Region capture cancelled")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to capture region: {str(e)}")
                
        threading.Thread(target=capture, daemon=True).start()
        
    def process_screenshot(self, screenshot):
        """Process and save/copy screenshot."""
        if not screenshot:
            return
            
        try:
            # Copy to clipboard if enabled
            if self.copy_clipboard_var.get():
                self.screenshot_manager.copy_to_clipboard(screenshot)
                self.update_status("Screenshot copied to clipboard")
                
            # Auto-save if enabled
            if self.auto_save_var.get():
                save_dir = self.save_dir_var.get()
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir, exist_ok=True)
                    
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(save_dir, filename)
                
                screenshot.save(filepath, "PNG")
                self.update_status(f"Screenshot saved to {filepath}")
            elif not self.copy_clipboard_var.get():
                # If neither auto-save nor clipboard, ask user where to save
                self.save_screenshot_as(screenshot)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process screenshot: {str(e)}")
            
    def save_screenshot_as(self, screenshot):
        """Show save dialog for screenshot."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialname=f"screenshot_{timestamp}.png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            screenshot.save(filename)
            self.update_status(f"Screenshot saved to {filename}")
            
    def browse_directory(self):
        """Browse for save directory."""
        directory = filedialog.askdirectory(initialdir=self.save_dir_var.get())
        if directory:
            self.save_dir_var.set(directory)
            
    def open_settings(self):
        """Open settings dialog."""
        # TODO: Implement settings dialog
        messagebox.showinfo("Settings", "Settings dialog will be implemented in future version.")
        
    def show_help(self):
        """Show help dialog."""
        help_text = """
Shotux Screenshot Tool

Keyboard Shortcuts:
• Print Screen - Full screen capture
• Alt + Print Screen - Active window capture  
• Shift + Print Screen - Region selection

Features:
• Multiple capture modes
• Configurable delay
• Auto-save option
• Copy to clipboard
• System tray integration

For more information, visit the project repository.
        """
        messagebox.showinfo("Help", help_text.strip())
        
    def minimize_to_tray(self):
        """Minimize application to system tray."""
        # TODO: Implement system tray functionality
        self.root.withdraw()
        self.update_status("Minimized to tray (restore not yet implemented)")
        
    def on_closing(self):
        """Handle application closing."""
        # Save configuration
        config = {
            'delay': int(self.delay_var.get()),
            'auto_save': self.auto_save_var.get(),
            'copy_clipboard': self.copy_clipboard_var.get(),
            'save_directory': self.save_dir_var.get()
        }
        self.config_manager.save_config(config)
        
        # Cleanup hotkeys
        self.hotkey_manager.cleanup()
        
        # Close application
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """Start the application."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main entry point."""
    app = ShotuxApp()
    app.run()


if __name__ == "__main__":
    main()
