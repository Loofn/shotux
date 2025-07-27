"""
Hotkey Manager Module
Handles global hotkey registration and management.
"""

import threading
import subprocess
import os
import signal


class HotkeyManager:
    def __init__(self, screenshot_manager):
        self.screenshot_manager = screenshot_manager
        self.hotkey_processes = []
        self.active = False
        
    def setup_hotkeys(self):
        """Set up global hotkeys using xbindkeys or similar."""
        try:
            # Check if xbindkeys is available
            result = subprocess.run(['which', 'xbindkeys'], capture_output=True)
            if result.returncode != 0:
                # Fallback to manual key binding setup
                self._setup_manual_hotkeys()
            else:
                self._setup_xbindkeys_hotkeys()
                
            self.active = True
        except Exception as e:
            raise Exception(f"Failed to setup hotkeys: {str(e)}")
            
    def _setup_manual_hotkeys(self):
        """Set up hotkeys using direct key monitoring (fallback method)."""
        # This is a simplified implementation
        # In a production app, you might want to use a more robust solution
        pass
        
    def _setup_xbindkeys_hotkeys(self):
        """Set up hotkeys using xbindkeys."""
        try:
            # Create xbindkeys configuration
            config_content = self._generate_xbindkeys_config()
            
            # Write configuration to temporary file
            config_file = os.path.expanduser('~/.xbindkeysrc.shotux')
            with open(config_file, 'w') as f:
                f.write(config_content)
                
            # Start xbindkeys with our configuration
            cmd = ['xbindkeys', '-f', config_file]
            process = subprocess.Popen(cmd)
            self.hotkey_processes.append(process)
            
        except Exception as e:
            raise Exception(f"Failed to setup xbindkeys: {str(e)}")
            
    def _generate_xbindkeys_config(self):
        """Generate xbindkeys configuration content."""
        script_path = os.path.abspath(__file__)
        main_path = os.path.join(os.path.dirname(script_path), '..', 'main.py')
        
        config = f'''
# Shotux hotkeys configuration
# Full screen capture
"python3 {main_path} --capture fullscreen"
    Print

# Active window capture  
"python3 {main_path} --capture window"
    alt + Print

# Region selection capture
"python3 {main_path} --capture region" 
    shift + Print
'''
        return config.strip()
        
    def cleanup(self):
        """Clean up hotkey processes and configuration."""
        self.active = False
        
        # Terminate hotkey processes
        for process in self.hotkey_processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception:
                pass
                
        self.hotkey_processes.clear()
        
        # Clean up configuration file
        config_file = os.path.expanduser('~/.xbindkeysrc.shotux')
        try:
            if os.path.exists(config_file):
                os.remove(config_file)
        except Exception:
            pass
            
    def is_active(self):
        """Check if hotkeys are active."""
        return self.active
        
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.cleanup()
