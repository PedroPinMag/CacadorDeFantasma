# public/bus_stops_data.py

BUS_STOPS = [
    {'id': 'p1', 'name': 'P1 - Principal', 'latitude': -22.7581, 'longitude': -43.6895},
    {'id': 'pgr', 'name': 'PGR - Pós-Graduação', 'latitude': -22.7595, 'longitude': -43.6853},
    {'id': 'icbs', 'name': 'ICBS - Instituto de Ciências Biológicas e da Saúde', 'latitude': -22.7612, 'longitude': -43.6877},
    # Add all other relevant UFRRJ bus stops here
    # Example: {'id': 'iv', 'name': 'IV - Instituto de Veterinária', 'latitude': ..., 'longitude': ...},
]

# Helper function to calculate distance (you'll need this later)
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance # in kilometers