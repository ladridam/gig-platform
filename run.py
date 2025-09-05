#!/usr/bin/env python3
"""
Main entry point for the Gig Platform application.
"""
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gig_platform import create_app
from gig_platform.utils.helpers import find_available_port, get_debug_flag

def main():
    """Run the application."""
    app = create_app()
    
    port = int(os.environ.get("PORT", find_available_port()))
    debug = get_debug_flag()
    
    print(f"Starting Gig Platform on port {port} (debug: {debug})")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    main()