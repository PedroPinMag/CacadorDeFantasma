# public/location_store.py
from datetime import datetime, timedelta
import threading

# This dictionary will store {device_id: {'latitude': float, 'longitude': float, 'timestamp': datetime}}
_active_user_locations = {}
_lock = threading.Lock()  # To handle concurrent updates safely


def update_user_location(device_id, latitude, longitude):
    """Stores or updates the location for a given device."""
    with _lock:
        _active_user_locations[device_id] = {
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': datetime.now()
        }
    # print(f"Updated location for {device_id}: {_active_user_locations[device_id]}") # For debugging


def get_recent_locations():
    """
    Returns a list of locations updated within the last minute.
    Also prunes locations older than 5 minute.
    """
    with _lock:
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=5)

        # Iterate over a copy of items for safe removal
        for device_id, data in list(_active_user_locations.items()):
            if data['timestamp'] < one_minute_ago:
                del _active_user_locations[device_id]

        # Return only the coordinates and device_id of still-active users
        recent_coords = [
            {'latitude': data['latitude'], 'longitude': data['longitude'], 'device_id': device_id}
            for device_id, data in _active_user_locations.items()
        ]
        # print(f"Recent locations: {recent_coords}") # For debugging
        return recent_coords