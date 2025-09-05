from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import logging

logger = logging.getLogger(__name__)


class GeocodingService:
    """Service for handling geocoding operations."""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="gig_platform")
        self.cache = {}  # Simple in-memory cache
    
    def geocode_location(self, location_name: str) -> Optional[Tuple[float, float]]:
        """
        Convert location name to coordinates.
        
        Args:
            location_name: The location name to geocode
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        # Check cache first
        if location_name in self.cache:
            return self.cache[location_name]
        
        try:
            location = self.geolocator.geocode(location_name)
            if location:
                coords = (location.latitude, location.longitude)
                self.cache[location_name] = coords  # Cache the result
                return coords
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error("Geocoding error for %s: %s", location_name, str(e))
            return None
    
    def clear_cache(self) -> None:
        """Clear the geocoding cache."""
        self.cache.clear()


# Singleton instance
geocoding_service = GeocodingService()