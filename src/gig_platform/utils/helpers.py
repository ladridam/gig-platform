import os
import socket
from contextlib import closing
from typing import Optional


def find_available_port(start_port: int = 5000, max_port: int = 5050) -> int:
    """
    Find an available port in the given range.
    
    Args:
        start_port: Starting port number
        max_port: Maximum port number to check
        
    Returns:
        Available port number or start_port if none found
    """
    for port in range(start_port, max_port + 1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    return start_port  # Fallback


def get_debug_flag() -> bool:
    """
    Get debug flag from environment.
    
    Returns:
        True if debug mode should be enabled
    """
    debug_env = os.environ.get("FLASK_DEBUG", "False").lower()
    render_env = os.environ.get("RENDER")
    return debug_env == "true" and render_env is None


def ensure_directories() -> None:
    """Ensure required directories exist."""
    os.makedirs("instance", exist_ok=True)
    os.makedirs("migrations/versions", exist_ok=True)