# public/services.py (or part of views.py)
import numpy as np
from sklearn.cluster import KMeans
from .location_store import get_recent_locations
from .bus_stops_data import BUS_STOPS, haversine_distance  # Import your bus stops and distance function


def determine_fantasminha_locations():
    """
    Processes recent user locations to determine Fantasminha positions
    using K-Means and associates them with the nearest bus stop.
    """
    recent_user_coords_data = get_recent_locations()  # [{'latitude': ..., 'longitude': ..., 'device_id': ...}, ...]

    if not recent_user_coords_data:
        return {"status_message": "Não há dados de localização recentes.", "bus_details": []}

    # Extract just (lat, lon) for K-Means
    points_for_kmeans = np.array([[data['latitude'], data['longitude']] for data in recent_user_coords_data])

    num_active_users = len(points_for_kmeans)
    estimated_bus_coords = []  # Raw GPS coordinates of detected buses

    if num_active_users == 0:  # Should be caught by the first check, but good for clarity
        return {"status_message": "Não há dados de localização recentes.", "bus_details": []}
    elif num_active_users == 1:
        # If only one user, that's one bus
        estimated_bus_coords.append(points_for_kmeans[0])
    elif num_active_users == 2:
        # If two users, assume two buses at their locations
        estimated_bus_coords.append(points_for_kmeans[0])
        estimated_bus_coords.append(points_for_kmeans[1])
    else:  # 3 or more users, run K-Means
        # Determine number of clusters (max 3, but not more than active users)
        n_clusters_to_find = min(3, num_active_users)

        # K-Means can't have more clusters than samples
        if n_clusters_to_find > 0:
            try:
                kmeans = KMeans(n_clusters=n_clusters_to_find, random_state=0, n_init='auto').fit(points_for_kmeans)
                estimated_bus_coords = kmeans.cluster_centers_  # These are [lat, lon]
            except ValueError as e:  # Handles cases like n_samples < n_clusters if logic above had a flaw
                # Fallback if K-Means fails for some reason (e.g. all points are identical)
                # Use unique points up to min(3, num_active_users)
                unique_points = np.unique(points_for_kmeans, axis=0)
                estimated_bus_coords = unique_points[:min(3, len(unique_points))]

    bus_details_for_frontend = []
    if not BUS_STOPS:  # Handle case where bus stops are not defined
        for i, coord_pair in enumerate(estimated_bus_coords):
            bus_details_for_frontend.append({
                'id': f'bus_{i + 1}',
                'title': f"Fantasminha {i + 1} (Ponto Desconhecido)",
                'latitude': coord_pair[0],  # For map marker
                'longitude': coord_pair[1],  # For map marker
                'nearest_stop_name': "N/A (Pontos não definidos)"
            })
        status_msg = f"{len(estimated_bus_coords)} Fantasminha(s) detectado(s)." if estimated_bus_coords else "Nenhum Fantasminha detectado."
        return {"status_message": status_msg, "bus_details": bus_details_for_frontend}

    for i, bus_center_coord in enumerate(estimated_bus_coords):
        min_dist = float('inf')
        nearest_stop_info = None

        for stop in BUS_STOPS:
            dist = haversine_distance(bus_center_coord[0], bus_center_coord[1], stop['latitude'], stop['longitude'])
            if dist < min_dist:
                min_dist = dist
                nearest_stop_info = stop

        if nearest_stop_info:
            bus_details_for_frontend.append({
                'id': f'bus_{i + 1}',  # Unique ID for frontend updates
                'title': f"Fantasminha perto de: {nearest_stop_info['name']}",
                'latitude': bus_center_coord[0],  # Actual K-Means center for map marker
                'longitude': bus_center_coord[1],  # Actual K-Means center for map marker
                'nearest_stop_name': nearest_stop_info['name']
            })
        else:  # Should not happen if BUS_STOPS is populated
            bus_details_for_frontend.append({
                'id': f'bus_{i + 1}',
                'title': f"Fantasminha {i + 1} (Ponto não encontrado)",
                'latitude': bus_center_coord[0],
                'longitude': bus_center_coord[1],
                'nearest_stop_name': "N/A"
            })

    status_msg = f"{len(bus_details_for_frontend)} Fantasminha(s) localizado(s)." if bus_details_for_frontend else "Nenhum Fantasminha ativo no momento."

    return {"status_message": status_msg, "bus_details": bus_details_for_frontend}