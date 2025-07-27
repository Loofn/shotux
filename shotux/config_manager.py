"""
Configuration Manager Module
Handles application configuration and settings.
"""

import json
import os
from pathlib import Path


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'shotux'
        self.config_file = self.config_dir / 'config.json'
        self.default_config = {
            'delay': 0,
            'auto_save': False,
            'copy_clipboard': True,
            'save_directory': str(Path.home() / 'Pictures' / 'Screenshots'),
            'image_format': 'PNG',
            'image_quality': 95,
            'hotkeys': {
                'fullscreen': 'Print',
                'window': 'alt+Print', 
                'region': 'shift+Print'
            },
            'ui': {
                'theme': 'default',
                'minimize_to_tray': True,
                'show_notifications': True
            }
        }
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_config(self.default_config, config)
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Warning: Failed to load config: {e}")
            return self.default_config.copy()
            
    def save_config(self, config_updates=None):
        """Save configuration to file."""
        try:
            # Update config with provided updates
            if config_updates:
                self.config.update(config_updates)
                
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Save configuration
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Failed to save config: {e}")
            
    def get(self, key, default=None):
        """Get configuration value."""
        try:
            # Support nested keys like 'ui.theme'
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key, value):
        """Set configuration value."""
        try:
            # Support nested keys like 'ui.theme'
            keys = key.split('.')
            config = self.config
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            config[keys[-1]] = value
        except Exception as e:
            print(f"Warning: Failed to set config value: {e}")
            
    def _merge_config(self, default, user):
        """Recursively merge user config with defaults."""
        merged = default.copy()
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_config(merged[key], value)
            else:
                merged[key] = value
        return merged
        
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = self.default_config.copy()
        self.save_config()
        
    def export_config(self, filepath):
        """Export configuration to a file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to export config: {e}")
            
    def import_config(self, filepath):
        """Import configuration from a file."""
        try:
            with open(filepath, 'r') as f:
                imported_config = json.load(f)
                self.config = self._merge_config(self.default_config, imported_config)
                self.save_config()
        except Exception as e:
            raise Exception(f"Failed to import config: {e}")
            
    def get_config_path(self):
        """Get the path to the configuration file."""
        return str(self.config_file)
