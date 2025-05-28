# public/services.py

# Supondo que estas importações já existem ou são necessárias:
# from datetime import datetime, timedelta # Se get_recent_locations estiver aqui
from .location_store import get_recent_locations
from .bus_stops_data import BUS_STOPS, \
    haversine_distance  # Assegure que haversine_distance está aqui ou importada corretamente


# Remova (se não forem mais usados em nenhum outro lugar):
# import numpy as np
# from sklearn.cluster import KMeans


def determine_fantasminha_locations():
    """
    Determina as localizações dos Fantasminhas baseando-se na proximidade dos usuários
    aos pontos de ônibus pré-definidos. Usuários a mais de 300m de qualquer ponto são
    descartados. Exibe até 3 pontos com mais usuários.
    """
    recent_user_coords_data = get_recent_locations()
    num_total_active_users = len(recent_user_coords_data)
    num_discarded_users_too_far = 0
    warning_message = None  # Inicializa a mensagem de aviso

    if num_total_active_users == 0:
        return {
            "status_message": "Não há dados de localização recentes.",
            "bus_details": [],
            "warning_message": None
        }

    if not BUS_STOPS:  # Verifica se a lista de pontos de ônibus está vazia
        if num_total_active_users > 0:
            # Todos os usuários são "descartados" porque não há pontos para associá-los
            pessoa_texto_disc = "usuário" if num_total_active_users == 1 else "usuários"
            warning_message = (
                f"Aviso: {num_total_active_users} {pessoa_texto_disc} não puderam ser associados "
                f"(nenhum ponto de ônibus cadastrado)."
            )
        return {
            "status_message": "Nenhum ponto de ônibus cadastrado para referência.",
            "bus_details": [],
            "warning_message": warning_message
        }

    # Inicializa dados para cada ponto de ônibus para contagem de usuários
    # A chave será o 'id' do ponto de ônibus
    fantasminha_at_stops = {
        stop['id']: {
            'id': stop['id'],
            'name': stop['name'],
            'latitude': stop['latitude'],
            'longitude': stop['longitude'],
            'user_count': 0
        } for stop in BUS_STOPS
    }

    # Processa cada localização de usuário
    for user_loc in recent_user_coords_data:
        min_dist_to_any_stop_m = float('inf')
        closest_stop_id_for_user = None

        # Encontra o ponto de ônibus mais próximo para este usuário
        for stop_id, stop_data in fantasminha_at_stops.items():
            dist_m = haversine_distance(
                user_loc['latitude'], user_loc['longitude'],
                stop_data['latitude'], stop_data['longitude']
            ) * 1000  # Convertendo para metros

            if dist_m < min_dist_to_any_stop_m:
                min_dist_to_any_stop_m = dist_m
                closest_stop_id_for_user = stop_id

        # Verifica se o ponto mais próximo está dentro do limite de 300m
        if closest_stop_id_for_user is not None and min_dist_to_any_stop_m <= 300:
            fantasminha_at_stops[closest_stop_id_for_user]['user_count'] += 1
        else:
            # Usuário está muito longe do ponto mais próximo (ou não há pontos)
            num_discarded_users_too_far += 1

    # Filtra os pontos que têm pelo menos um usuário associado
    potential_fantasminhas = [
        data for data in fantasminha_at_stops.values() if data['user_count'] > 0
    ]

    # Ordena os "Fantasminhas" (pontos de ônibus) pela contagem de usuários, em ordem decrescente
    sorted_fantasminhas = sorted(potential_fantasminhas, key=lambda x: x['user_count'], reverse=True)

    # Seleciona os top 3 (ou menos, se houver menos)
    top_fantasminhas = sorted_fantasminhas[:3]

    # Prepara a lista de detalhes dos ônibus para o frontend
    bus_details_for_frontend = []
    for fantasminha_data in top_fantasminhas:
        bus_details_for_frontend.append({
            'id': fantasminha_data['id'],  # ID do ponto de ônibus
            'latitude': fantasminha_data['latitude'],  # Coordenadas do ponto
            'longitude': fantasminha_data['longitude'],
            'nearest_stop_name': fantasminha_data['name'],  # Nome do ponto é o nome do "Fantasminha"
            'user_count': fantasminha_data['user_count']
        })

    # Constrói a mensagem de status principal
    status_message = "Nenhum Fantasminha ativo no momento."
    if len(bus_details_for_frontend) == 1:
        status_message = "1 Fantasminha localizado."
    elif len(bus_details_for_frontend) > 1:
        status_message = f"{len(bus_details_for_frontend)} Fantasminhas localizados."

    # Constrói a mensagem de aviso sobre usuários descartados
    if num_discarded_users_too_far > 0:
        pessoa_texto_warn = "usuário não foi contabilizado por estar" if num_discarded_users_too_far == 1 else \
            "usuários não foram contabilizados por estarem"
        warning_message = (
            f"Aviso: {num_discarded_users_too_far} {pessoa_texto_warn} a mais de 300m de qualquer ponto."
        )

    return {
        "status_message": status_message,
        "bus_details": bus_details_for_frontend,
        "warning_message": warning_message  # Pode ser None
    }