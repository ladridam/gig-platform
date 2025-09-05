from typing import Union, Tuple, Optional
from flask import request


def get_coordinates_from_request() -> Optional[Tuple[float, float]]:
    """
    Extract coordinates from request form data.
    
    Returns:
        Tuple of (lat, lng) or None if invalid/missing
    """
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    
    if lat and lng:
        try:
            return (float(lat), float(lng))
        except (ValueError, TypeError):
            return None
    return None


def normalize_data(data) -> list:
    """
    Convert database objects to dicts with list locations.
    
    Args:
        data: List of database objects or dictionaries
        
    Returns:
        List of normalized dictionaries
    """
    normalized = []
    for item in data:
        if hasattr(item, "to_dict"):
            normalized.append(item.to_dict())
        else:
            new_item = item.copy()
            if "location" in new_item and isinstance(new_item["location"], tuple):
                new_item["location"] = list(new_item["location"])
            normalized.append(new_item)
    return normalized