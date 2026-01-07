#!/usr/bin/env python3
"""
gghelper - Git Workflow Mentor & Assistant
Version: 2.1.0 (with config support)
"""

import os
import sys
import subprocess
import tempfile
import argparse
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

def get_config_path():
    """Get path to config file."""
    config_dir = Path.home() / ".config" / "gghelper"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"

def read_config():
    """Read config file."""
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def write_config(config):
    """Write config file."""
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def set_language_in_config(lang):
    """Set language in config file."""
    config = read_config()
    config['language'] = lang
    write_config(config)
    return config

def set_level_in_config(level):
    """Set learning level in config file."""
    config = read_config()
    config['level'] = level
    write_config(config)
    return config

def detect_language(args):
    """Detect language with priority order."""
    # 1. Command line argument (highest priority)
    if args.lang:
        return args.lang
    
    # 2. Environment variable
    env_lang = os.getenv('GITHELPER_LANG')
    if env_lang in ['hu', 'en']:
        return env_lang
    
    # 3. Config file
    config = read_config()
    if config and 'language' in config:
        return config['language']
    
    # 4. System LANG environment variable
    sys_lang = os.getenv("LANG", "en_US.UTF-8").split('_')[0].lower()
    return "hu" if sys_lang == "hu" else "en"

# ============================================================================
# ARGUMENT PARSING WITH --set-lang AND --set-level
# ============================================================================

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="gghelper - Git Workflow Mentor",
        add_help=False
    )
    
    # Operation modes
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done")
    parser.add_argument("--resolve-only", action="store_true", 
                       help="Only resolve conflicts")
    parser.add_argument("--safe", action="store_true", 
                       help="Use merge instead of rebase")
    
    # Language and learning settings
    parser.add_argument("--lang", choices=["en", "hu"], 
                       help="Force language (en/hu)")
    parser.add_argument("--level", choices=["novice", "intermediate", "expert", "auto"],
                       help="Learning level (auto = detect from git history)")
    
    # Config management (NEW!)
    parser.add_argument("--set-lang", choices=["en", "hu"],
                       help="Set default language permanently")
    parser.add_argument("--set-level", choices=["novice", "intermediate", "expert", "auto"],
                       help="Set default learning level permanently")
    
    # Information and help
    parser.add_argument("--help", "-h", action="store_true", 
                       help="Show contextual help")
    parser.add_argument("--smart-help", action="store_true",
                       help="Show smart help based on current situation")
    parser.add_argument("--stats", action="store_true",
                       help="Show your usage statistics")
    parser.add_argument("--version", "-v", action="store_true", 
                       help="Show version")
    
    return parser.parse_args()

# ============================================================================
# MAIN FUNCTION WITH CONFIG SUPPORT
# ============================================================================

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Handle config setting commands FIRST
    if args.set_lang or args.set_level:
        config = read_config()
        
        if args.set_lang:
            config['language'] = args.set_lang
            print(f"✅ Language set to: {args.set_lang}")
            print(f"   Config file: {get_config_path()}")
        
        if args.set_level:
            config['level'] = args.set_level
            print(f"✅ Learning level set to: {args.set_level}")
        
        write_config(config)
        
        # Show current config
        print("\n📋 Current configuration:")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        # Helpful tips
        if args.set_lang == 'hu':
            print("\n💡 Tipp: Mostantól a gghelper automatikusan magyarul fog indulni!")
            print("   Használd: gghelper")
        elif args.set_lang == 'en':
            print("\n💡 Tip: gghelper will now automatically start in English!")
            print("   Use: gghelper")
        
        return 0
    
    # Handle other special commands
    if args.help:
        # Show help in detected language
        lang = detect_language(args)
        show_help(lang)
        return 0
    
    if args.version:
        print("gghelper v2.1.0 - Git Workflow Mentor")
        print("Config support: --set-lang hu/en, --set-level novice/intermediate/expert/auto")
        return 0
    
    # ... rest of the main function continues as before ...
    # (Workflow, learning system, etc.)
    
    # Example workflow start:
    lang = detect_language(args)
    print(f"\n🌐 Language: {lang}")
    
    # Continue with normal workflow...
    # ...

def show_help(lang):
    """Show help message."""
    if lang == "hu":
        print("""
gghelper v2.1.0 - Git Workflow Mentor

HASZNÁLAT:
  gghelper                    # Interaktív commit és push
  gghelper --resolve-only     # Csak konfliktusok feloldása
  gghelper --safe            # Használj merge-t rebase helyett
  
  # NYELV BEÁLLÍTÁS:
  gghelper --set-lang hu     # Állítsd be magyarra (tartósan!)
  gghelper --set-lang en     # Állítsd be angolra (tartósan!)
  
  # TANULÁSI SZINT:
  gghelper --set-level novice      # Részletes magyarázatok
  gghelper --set-level intermediate # Közepes magyarázatok
  gghelper --set-level expert      # Minimális magyarázatok
  gghelper --set-level auto        # Automatikus detektálás

  # EGYSZERI NYELVVÁLASZTÁS:
  gghelper --lang hu         # Most magyarul (nem menti)
  gghelper --lang en         # Most angolul (nem menti)

KONFIGURÁCIÓ:
  A beállítások itt vannak: ~/.config/gghelper/config.json
  Törlés: rm -rf ~/.config/gghelper
        """)
    else:
        print("""
gghelper v2.1.0 - Git Workflow Mentor

USAGE:
  gghelper                    # Interactive commit and push
  gghelper --resolve-only     # Only resolve conflicts
  gghelper --safe            # Use merge instead of rebase
  
  # LANGUAGE SETTING:
  gghelper --set-lang hu     # Set to Hungarian (permanently!)
  gghelper --set-lang en     # Set to English (permanently!)
  
  # LEARNING LEVEL:
  gghelper --set-level novice      # Detailed explanations
  gghelper --set-level intermediate # Moderate explanations
  gghelper --set-level expert      # Minimal explanations
  gghelper --set-level auto        # Auto-detect

  # ONE-TIME LANGUAGE:
  gghelper --lang hu         # Hungarian for this run only
  gghelper --lang en         # English for this run only

CONFIGURATION:
  Config file: ~/.config/gghelper/config.json
  Reset: rm -rf ~/.config/gghelper
        """)

if __name__ == "__main__":
    sys.exit(main())