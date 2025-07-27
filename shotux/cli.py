#!/usr/bin/env python3
"""
Command-line interface for Shotux screenshot tool.
Allows for direct screenshot capture without GUI.
"""

import sys
import argparse
import os

from .screenshot_manager import ScreenshotManager
from .config_manager import ConfigManager


def main():
    parser = argparse.ArgumentParser(description='Shotux Screenshot Tool CLI')
    parser.add_argument('--capture', choices=['fullscreen', 'window', 'region'],
                       help='Capture mode')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--delay', '-d', type=int, default=0,
                       help='Delay in seconds before capture')
    parser.add_argument('--clipboard', '-c', action='store_true',
                       help='Copy to clipboard')
    
    args = parser.parse_args()
    
    if not args.capture:
        parser.print_help()
        return
        
    # Initialize managers
    config_manager = ConfigManager()
    screenshot_manager = ScreenshotManager(config_manager)
    
    try:
        # Apply delay
        if args.delay > 0:
            import time
            time.sleep(args.delay)
            
        # Capture screenshot
        if args.capture == 'fullscreen':
            screenshot = screenshot_manager.capture_fullscreen()
        elif args.capture == 'window':
            screenshot = screenshot_manager.capture_window()
        elif args.capture == 'region':
            screenshot = screenshot_manager.capture_region()
            
        if not screenshot:
            print("Screenshot capture failed or was cancelled")
            return
            
        # Process screenshot
        if args.output:
            screenshot.save(args.output)
            print(f"Screenshot saved to: {args.output}")
            
        if args.clipboard:
            screenshot_manager.copy_to_clipboard(screenshot)
            print("Screenshot copied to clipboard")
            
        if not args.output and not args.clipboard:
            # Default: save to default directory
            from datetime import datetime
            save_dir = config_manager.get('save_directory')
            os.makedirs(save_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(save_dir, filename)
            
            screenshot.save(filepath)
            print(f"Screenshot saved to: {filepath}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
